# coding: utf8

import requests
from requests import exceptions as excs

from itertools import chain
from datetime import datetime, timedelta

from celery import group
from celery.utils.log import get_task_logger
from celery.exceptions import Ignore

from tasks import proxies
from tasks.utils.database import databases
from tasks.application import app

logger = get_task_logger('tasks')


def chunk(seq, size):
    """
    Returns an iterator over a series of lists of length size from iterable.
        >>> list(chunk([1,2,3,4], 2))
        [[1, 2], [3, 4]]
        >>> list(chunk([1,2,3,4,5], 2))
        [[1, 2], [3, 4], [5]]
    """
    def take(seq, n):
        for i in range(n):
            try:
                yield next(seq)
            except Exception:
                break

    if not hasattr(seq, 'next'):
        seq = iter(seq)
    while True:
        x = list(take(seq, size))
        if x:
            yield x
        else:
            break


@app.task
def update_proxies():

    _proxies = chain(
        proxies.IpAddressComProxyList(None).parse(),
        proxies.Api66IpCn(None).parse(),
        proxies.KuaiDaiLiComFree(None).parse(),
        proxies.XicidailiCom(None).parse()
    )

    for _p in chunk(_proxies, 20):
        group([
            validate.signature(
                args=(safe_dict(p), ),
                link=save.s(),
                expires=600
            )
            for p in _p
        ]) \
            .apply_async()


@app.task(rate_limit='100/m')
def validate_exists():

    db = databases('scripture')

    one_hours_ago = datetime.now() - timedelta(hours=1)

    db.cm_proxies.delete_many({'verified_at': {'$lt': one_hours_ago}})

    _proxies = db.cm_proxies.find()

    for _p in chunk(_proxies, 20):
        group([
            validate.signature(
                args=(safe_dict(p), ),
                link=save.s(),
                expires=600
            )
            for p in _p
        ]) \
            .apply_async()


def safe_dict(d):
    d.pop('_id', None)
    return d


@app.task
def save(proxy):
    if not proxy:
        raise Ignore()
    db = databases('scripture')
    now = datetime.now()
    proxy['verified_at'] = now
    if 'updated_at' not in proxy:
        proxy['updated_at'] = now
    proxy.pop('_id', None)
    result = db.cm_proxies.update_one(
        {
            'ip': proxy.get('ip'),
            'port': proxy.get('port')
        }, {
            '$set': proxy,
            '$setOnInsert': {'created_at': now},
        },
        upsert=True
    )
    logger.debug(
        'elapsed of Proxy(%s://%s:%s) %s, Upserted(%s), nModified(%s)',
        proxy.get('protocal', 'http'),
        proxy.get('ip'),
        proxy.get('port'),
        proxy.get('elapsed'),
        result.raw_result.get('upserted'),
        result.raw_result.get('nModified')
    )


@app.task(rate_limit='100/m')
def validate(proxy):
    if not proxy:
        raise Ignore()
    host = proxy.get('ip')
    port = proxy.get('port')
    # protocal = proxy.get('protocal', 'http')
    try:
        resp = requests.get(
            'https://www.booking.com',
            proxies={
                'http': 'http://{}:{}'.format(host, port),
                'https': 'http://{}:{}'.format(host, port)
            },
            timeout=5
        )
        if resp.status_code != 200:
            raise Ignore()
        # 增加可信度
        resp = requests.get(
            'https://www.booking.com',
            proxies={
                'http': 'http://{}:{}'.format(host, port),
                'https': 'http://{}:{}'.format(host, port)
            },
            timeout=5
        )
        if resp.status_code != 200:
            raise Ignore()
    except (excs.ProxyError, excs.SSLError, excs.ConnectionError,
            excs.Timeout, excs.ChunkedEncodingError):
        return
    elapsed = resp.elapsed.total_seconds()
    proxy['elapsed'] = elapsed
    return proxy


if __name__ == '__main__':
    update_proxies()
