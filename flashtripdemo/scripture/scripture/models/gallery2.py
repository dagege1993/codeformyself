# coding: utf8

import logging

import oss2
import requests

from io import BytesIO

from yarl import URL


class Gallery(dict):
    domains = [
        'img3.weegotr.com',
        'img4.weegotr.com'
    ]

    session = requests.Session()

    def __init__(self, url):
        self.logger = logging.getLogger(__name__)
        endpoint = 'http://oss-cn-beijing-internal.aliyuncs.com'
        auth = oss2.Auth('LTAIwHXVgRkPRxcw', 'PCm6kdpeyjAG2gJz4B4C2js3TIifrc')
        self.bucket = oss2.Bucket(auth, endpoint, 'weegotr-statics')

        u = URL(url)
        path = u.path if not u.path.startswith('/') else u.path[1:]
        exists = self.bucket.object_exists(path)
        if not exists:
            url = u.with_host('exp.cdn-hotels.com')
            content = BytesIO(self.session.get(str(url)).content)
            put_result = self.bucket.put_object(path, content)
            if put_result.status >= 300:
                print({
                    'status': put_result.status,
                    'text': put_result.resp
                })
            else:
                print({
                    'status': put_result.status,
                    'file': u.path
                })
