# coding: utf8

import random
import logging

import oss2
import requests
from yarl import URL


class Gallery(dict):
    domains = [
        'img3.weegotr.com',
        'img4.weegotr.com'
    ]

    session = requests.Session()
    session.mount(
        'http://',
        requests.adapters.HTTPAdapter(pool_connections=50, pool_maxsize=100)
    )
    session.mount(
        'https://',
        requests.adapters.HTTPAdapter(pool_connections=50, pool_maxsize=100)
    )

    def __init__(self, url):
        self.logger = logging.getLogger(__name__)
        oss2.defaults.connection_pool_size = 150
        endpoint = 'http://oss-cn-beijing.aliyuncs.com'
        auth = oss2.Auth('LTAIwHXVgRkPRxcw', 'PCm6kdpeyjAG2gJz4B4C2js3TIifrc')
        self.bucket = oss2.Bucket(auth, endpoint, 'weegotr-statics')

        if self.handle(url):
            host = random.choice(self.domains)
            url = str(URL(url).with_scheme('http').with_host(host))
            self['image_url'] = url
        else:
            self['image_url'] = url

    def _image_is_exists(self, uri):
        if uri.startswith('/'):
            uri = uri[1:]
        return self.bucket.object_exists(uri)

    def _upload_image(self, url, path):
        resp = self.session.get(
            str(url),
            headers={'User-Agent': ''}
        )
        self.logger.debug('Image(%s), StatusCode(%d)', url, resp.status_code)
        if resp.status_code != 200:
            return False
        put_result = self.bucket.put_object(path, resp.iter_content())
        self.logger.debug('Fetched object %s source %s', path, url)
        return put_result.status < 300 and True or False

    def handle(self, url, to_try=None, ori=None):
        if to_try is None:
            to_try = ['z', 'y', 'b', 'n', 'l', 't', 'd', 's', 'e', 'g']
        try:
            fr = URL(url).path[1:]
            to = ori and URL(ori).path[1:] or fr
            if self._image_is_exists(to):
                return True
            if self._upload_image(url, to):
                return True
            else:
                if not ori:
                    ori = url
                prefix, postfix = url.rsplit('.', 1)
                return self.handle(
                    prefix[:-1] + to_try[0] + '.' + postfix,
                    to_try[1:],
                    ori
                )
        except oss2.exceptions.ClientError as e:
            self.logger.exception(e)
            return False
