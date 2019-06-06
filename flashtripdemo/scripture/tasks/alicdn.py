# coding: utf8
"""Module
"""

import re
import os
import gzip
import shutil
import tempfile
try:
    import ujson as json
except ImportError:
    import json

from typing import Tuple, Dict, List, Any   # pylint: disable=W0611
from datetime import datetime, timedelta

import redis
import celery
import requests

from yarl import URL
from celery import chord, signature
from celery.canvas import Signature
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
from celery.exceptions import Ignore

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcdn.request.v20141111 import DescribeDomainTopUrlVisitRequest \
    as UrlRequest
from aliyunsdkcdn.request.v20141111 import DescribeCdnDomainLogsRequest \
    as LogRequest

from tasks import settings
from tasks.application import app

client = AcsClient(
    settings.ALIYUN_CDN_ACCESS_KEY_ID,
    settings.ALIYUN_CDN_ACCESS_KEY_SECRET,
    'cn-beijing'
)

red = redis.Redis.from_url(settings.REDIS, db=2) # (host='', port=6379)

RE_LOG = re.compile(r'"(GET|HEAD|POST) (https?[^"]+)" '
                    r'(\d{3}) \d+ \d+ (HIT|MISS|-) "([^"]+)" "([^"]+)"')


@app.task
def query_top_url(domain: str = None, days: int = None) -> List[Dict]:
    """Query top urls of cdn
    """
    logger = get_task_logger('tasks')

    try:
        request = UrlRequest.DescribeDomainTopUrlVisitRequest()
        if domain:
            request.set_DomainName(domain)
        if days:
            key = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            request.set_StartTime(key)

        response = client.do_action_with_exception(request)

    except (ClientException, ServerException) as exc:
        logger.exception(exc)
        return []

    resp = json.loads(response.decode('utf8'))

    links = []  # type: List[Dict[str, str]]

    urls_must_ignored = ['/', '/favicon.ico']

    for url in resp['Url400List']['UrlList']:
        # if (int(url['VisitData']) < 2
        if url['UrlDetail'] in urls_must_ignored:
            continue
        links.append({"times": url['VisitData'], "link": url['UrlDetail']})

    return links


def handle_line(key, line, uris):
    logger = get_task_logger('tasks')
    _line = line.decode('utf8')
    _s = RE_LOG.search(_line)
    try:
        groups = _s.groups()
        method, url, status_code, state, ua, accept = groups
    except Exception:
        logger.error('RE not found: %s', _line)
        return
    if int(status_code) < 399:
        return
    if int(status_code) == 499:
        return
    if 'Alibaba.Security.Heimdall' in ua:
        return

    for uri in uris:
        if uri in url:
            red.lpush(key + uri, _line)
            break


@app.task
def uri_visited_history(logs: List[Dict[str, str]],
                        topuri_task_id: str,
                        days: int = 1) -> List:
    """Query visit history of image url
    """

    key = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d_')
    urls = AsyncResult(topuri_task_id).get(disable_sync_subtasks=False)
    uris = []
    for url in urls:
        if url['link'].startswith('/hotels/'):
            if not url['link'].rsplit('.', 1)[0].endswith('_w'):
                continue
            if requests.head(url['link']).status_code == 200:
                continue
        uris.append(URL(url['link']).path)

    for logname in logs:
        try:
            with gzip.open(logname, 'rb') as logfile:
                for line in logfile:
                    handle_line(key, line, uris)
        except celery.backends.base.IsADirectoryError as exc:
            return []
    return uris


@app.task
def download(log_path: str, log_name: str) -> str:
    """Download logfile
    """
    logger = get_task_logger('tasks')

    try:
        if (not log_path.startswith('http://') and
                not log_path.startswith('https://')):
            log_path = 'https://' + log_path
        resp = requests.get(log_path)
        with open(log_name, 'ab') as logfile:
            logfile.write(resp.content)
    except Exception as exc:
        logger.exception(exc)
        raise Ignore(None)

    return log_name


@app.task
def to_download(domain: str, callback: Signature, days: int = 1
                ) -> List[Dict[str, str]]:
    """Query urls to download
    """
    logs = []  # type: List[Dict[str, str]]

    tmpdir = tempfile.mkdtemp('.logs', '-'.join([str(days), 'scripture.']))
    yesterday = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    request = LogRequest.DescribeCdnDomainLogsRequest()
    request.set_DomainName(domain)
    request.set_LogDay(yesterday)
    request.set_PageSize(30)
    response = client.do_action_with_exception(request)  # type: str
    resp = json.loads(response)  # type: Dict
    domain_log_details = resp['DomainLogModel']['DomainLogDetails']
    for log_detail in domain_log_details['DomainLogDetail']:
        log_name = os.path.join(tmpdir, log_detail['LogName'])
        logs.append({
            'log_path': log_detail['LogPath'],
            'log_name': log_name
        })

    callback = signature(callback).clone(link=cleanup.s(tmpdir=tmpdir))
    jobs = chord(
        download.s(log['log_path'], log['log_name']) for log in logs
    )
    async_result = jobs(callback)
    return async_result.id


@app.task
def cleanup(result: Any, tmpdir: str) -> bool:
    """clean up temp dir
    """
    logger = get_task_logger('tasks')
    try:
        shutil.rmtree(tmpdir)
    except Exception as exc:
        logger.exception(exc)

    return result


@app.task
def audit_cdn_logs(days: int = 1) -> bool:
    """CDN logs
    """
    async_result = query_top_url.apply_async(args=(None, days))
    jobs = chord([
        to_download.s(
            'img1.weegotr.com',
            uri_visited_history.s(topuri_task_id=async_result.id, days=days),
            days=days
        ),
        to_download.s(
            'img2.weegotr.com',
            uri_visited_history.s(topuri_task_id=async_result.id, days=days),
            days=days
        ),
        to_download.s(
            'img3.weegotr.com',
            uri_visited_history.s(topuri_task_id=async_result.id, days=days),
            days=days
        ),
        to_download.s(
            'img4.weegotr.com',
            uri_visited_history.s(topuri_task_id=async_result.id, days=days),
            days=days
        ),
        to_download.s(
            'img5.weegotr.com',
            uri_visited_history.s(topuri_task_id=async_result.id, days=days),
            days=days
        )
    ])
    async_result = jobs(notify.s(days=days))
    return async_result.id


@app.task
def notify(jobs: List[str], days: int = 1) -> Tuple[int, str]:
    """Send message to DingTalk
    """

    try:
        [
            AsyncResult(job_id).get(disable_sync_subtasks=False)
            for job_id in jobs
        ]
    except:
        return 0, str(exc)

    key = yesterday = (
        datetime.now() - timedelta(days=days)
    ).strftime('%Y-%m-%d')

    keys = red.keys(f"{key}_*")
    expired_after = 1209600  # 60 * 60 * 24 * 7 * 2
    for _key in keys:
        red.expire(_key, expired_after)
    length = len(keys)

    params = {
        'access_token':
            'e794af17cbb02db3010d98bc832713f8935037622427e289c714868d880c56f9',
    }
    image_404 = 'http://img3.weegotr.com/cms/uploads/custom-error.png'
    viewlogs = 'http://scripture.weegotr.com/views/cdn/logs'

    if length == 0:
        return None

    payload = {
        'msgtype': 'actionCard',
        'actionCard': {
            "title": "CDN 4XX 日志",
            'text': (f"![4xx]({image_404})\n  "
                     f"### {yesterday} CDN 4XX 图片日志\n  "
                     f"{yesterday}有{length}个图片有问题"),
            'hideAvatar': 1,
            'singleTitle': '查看日志',
            'singleURL': f"{viewlogs}/{yesterday}",
        }
    }
    resp = requests.post(
        'https://oapi.dingtalk.com/robot/send',
        params=params,
        json=payload
    )

    return resp.status_code, resp.text


def ensure_unicode(arg: Any):
    """decode every things to unicode
    """
    if isinstance(arg, str):
        return arg
    if isinstance(arg, bytes):
        return arg.decode('utf8')
    if isinstance(arg, (list, tuple, set)):
        return (_arg.decode('utf8') for _arg in arg)

    return None
