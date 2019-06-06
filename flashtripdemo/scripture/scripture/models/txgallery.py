# coding: utf8

import random

import oss2

from yarl import URL
from twisted.logger import Logger
from twisted.internet import defer, threads
from tasks.upload_image import _upload_image

class TxOss(object):
    def __init__(self, ak, sk, bucket):
        endpoint = 'http://oss-cn-beijing-internal.aliyuncs.com'
        auth = oss2.Auth('LTAIwHXVgRkPRxcw', 'PCm6kdpeyjAG2gJz4B4C2js3TIifrc')
        self.bucket = oss2.Bucket(auth, endpoint, 'weegotr-statics')

    def head_object(self, path):
        return threads.deferToThread(self.bucket.head_object, path)

    def put_object(self, path, content):
        return threads.deferToThread(self.bucket.put_object, path, content)

    def object_exists(self, path):
        return threads.deferToThread(self.bucket.object_exists, path)


class TxGallery(dict):
    domains = [
        'img3.weegotr.com',
        'img4.weegotr.com'
    ]

    def __init__(self):
        self.logger = Logger(__name__)
        endpoint = 'http://oss-cn-beijing.aliyuncs.com'
        self.bucket = TxOss(
            'LTAIwHXVgRkPRxcw',
            'PCm6kdpeyjAG2gJz4B4C2js3TIifrc',
            endpoint
        )

    @defer.inlineCallbacks
    def get_image_url(self, url, to_try=None):
        state = yield self.handle(url, to_try)
        if state:
            host = random.choice(self.domains)
            url = str(URL(url).with_scheme('http').with_host(host))
            return url
        else:
            return url

    @defer.inlineCallbacks
    def _image_is_exists(self, uri):
        if uri.startswith('/'):
            uri = uri[1:]
        state = yield self.bucket.object_exists(uri)
        return state

    @defer.inlineCallbacks
    def handle(self, url, to_try=None, ori=None):
        if to_try is None:
            to_try = ['z', 'y', 'b', 'n', 'l', 't', 'd', 's', 'e', 'g']
        try:
            fr = URL(url).path[1:]
            if ori:
                _ori = URL(ori)
                if _ori.path.startswith('/'):
                    to = _ori.path[1:]
                else:
                    to = _ori.path
            else:
                to = fr
            state = yield self._image_is_exists(to)
            if state:
                return True
            _upload_image.delay(url, to)
            return True
        except Exception as e:
            self.logger.error('Exception', exc_info=e)
            return False
