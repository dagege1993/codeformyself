# coding: utf8

import random
import logging
import requests

from typing import List

import oss2

from yarl import URL

from tasks import settings
from tasks.application import app
from tasks.utils.notifiers import DingtalkMessage, DingtalkNotifier
from tasks.errors import NotifyFailed, UploadFailed
from celery.utils.log import get_task_logger


class ImageSaver:
    logger = logging.getLogger(__name__)

    def __init__(self, supplier: str) -> None:
        self.supplier = supplier

    def save(self, url: str) -> str:
        if not isinstance(url, str):
            url = str(url)
        ori_url = URL(url)
        if not ori_url.is_absolute():
            ori_url = URL(''.join(['http://', url]))
        url = str(ori_url.with_path(f'agents/{self.supplier}{ori_url.path}')
                  .with_host('img%s.weegotr.com' % random.randint(3, 4))
                  .with_scheme('https'))
        upload_image.apply_async(
            kwargs={
                'ori_url': str(ori_url),
                'url': url
            },
            link_error=on_upload_failure.s()
        )
        return url

    def upload_images(self, images: List[str], ori_images) -> List[str]:
        if not images:
            images = []
        _images = images.copy() if images else []
        for image_url in images:
            for ori_image in ori_images:
                _image_url = URL(image_url)
                if not _image_url.is_absolute():
                    _image_url = URL(''.join(['http://', image_url]))
                if _image_url.path in ori_image and 'weegotr.com' in ori_image:
                    new_url = ori_image
                    break
            else:
                new_url = self.save(image_url)
            _images.remove(image_url)
            _images.append(new_url)
        return _images


@app.task(autoretry_for=(Exception, ), retry_kwargs={'max_retries': 1})
def upload_image(ori_url: str, url: str):
    logger = get_task_logger('tasks')
    auth = oss2.Auth(
        settings.OSS_ACCESS_KEY_ID,
        settings.OSS_SECRET_ACCESS_KEY
    )
    oss = oss2.Bucket(auth, settings.OSS_ENDPOINT, settings.OSS_BUCKET)
    try:
        resp = requests.get(ori_url, proxies=settings.PROXIES)
    except Exception as exc:
        raise UploadFailed(ori_url) from exc
    body = resp.content
    if resp.status_code != 200 or not body:
        raise UploadFailed(
            ori_url, f'<{resp.status_code}>{resp.text}'
        )
    # if isinstance(body, str):
    #     body = body.encode('utf8')
    result = oss.put_object(URL(url).path[1:], body)
    logger.info({'headers': result.headers,
                 'status': result.status,
                 'etag': result.etag})


@app.task
def on_upload_failure(task_id):
    logger = logging.getLogger(__name__)
    result = app.AsyncResult(task_id)
    logger.warning(f'## [告警]上传CDN图片失败\n{result.result}')
    # result = app.AsyncResult(task_id)
    # text = f'## [告警]上传CDN图片失败\n{result.result}'
    # msg = DingtalkMessage(title='上传CDN图片失败', text=text)
    # try:
    #     DingtalkNotifier().send(msg, settings.DINGTALK_NOTIFY[''])
    # except NotifyFailed as exc:
    #     logger.error('钉钉告警失败', exc_info=exc)

if __name__ == '__main__':
    upload_image(
        "http://www.roomsxml.com/RXLImages/1001/09717hotel1.JPG",
        "agents/roomsxml/RXLImages/1001/09717hotel1.JPG"
    )
