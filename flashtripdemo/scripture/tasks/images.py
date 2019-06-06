# coding: utf8

import oss2
import requests

import random

from yarl import URL
from celery.utils.log import get_task_logger

from tasks.application import app

logger = get_task_logger('tasks')


def oss():
    oss2.defaults.connection_pool_size = 100

    endpoint = 'http://oss-cn-beijing.aliyuncs.com'
    auth = oss2.Auth('LTAIwHXVgRkPRxcw', 'PCm6kdpeyjAG2gJz4B4C2js3TIifrc')
    bucket = oss2.Bucket(auth, endpoint, 'weegotr-statics')
    return bucket


def request():
    session = requests.Session()
    session.mount(
        'http://',
        requests.adapters.HTTPAdapter(pool_connections=50, pool_maxsize=100)
    )
    session.mount(
        'https://',
        requests.adapters.HTTPAdapter(pool_connections=50, pool_maxsize=100)
    )
    return session


class Gallery(dict):

    domains = [
        'img3.weegotr.com',
        'img4.weegotr.com'
    ]

    postfixes = ['z', 'y', 'b', 'n', 'l', 't', 'd', 's', 'e', 'g']

    def __init__(self, url):

        host = random.choice(self.domains)
        url = str(URL(url).with_scheme('http').with_host(host))
        if self.handle(url):
            self['image_url'] = url
        self.bucket = oss()
        self.request = request()

    def _is_exists(self, uri):
        resp = self.request.head(
            uri,
            headers={'User-Agent': ''}
        )
        logger.debug('%s, %d', uri, resp.status_code)
        if resp.status_code != 200:
            return False
        return True

    def handle(self, url, to_try=postfixes, ori=None):
        if not self._is_exists(url):
            if not ori:
                ori = url
            prefix, postfix = url.rsplit('.', 1)
            return self.handle(
                prefix[:-1] + to_try[0] + '.' + postfix,
                to_try[1:],
                ori
            )
        fr = URL(url).path
        fr = fr[1:] if fr.startswith('/') else fr
        if not ori:
            return True
        to = URL(ori).path
        to = to[1:] if to.startswith('/') else to
        try:
            copy = self.bucket.copy_object('weegotr-statics', fr, to)
            if copy.status > 299:
                return self.handle(url, to_try, ori=None)
            logger.debug('Copy %s to %s %s', fr, to, copy.status)
            delete = self.bucket.delete_object(fr)
            logger.debug('Delete %s %s', fr, delete.status)
            logger.debug(
                'Set expires to None %s %s',
                to,
                self.bucket.update_object_meta(to, {'Expires': None}).status
            )
        except oss2.exceptions.NotFound as e:
            logger.exception(e)
            return False
        return True


@app.task
def gallery(url):
    return Gallery(url)
