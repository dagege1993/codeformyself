# -- coding: utf-8 --

import hmac
import json
import time
import base64
import random
import asyncio
import hashlib
import urllib.parse

from collections import namedtuple

from yarl import URL
from aiohttp import ClientSession
from multidict import CIMultiDict

Response = namedtuple('Response', ('headers', 'status_code', 'content'))


class Suggest(object):

    async def suggestions(self):
        pass


class QueryBuilder(object):

    def __init__(self, query={}, configs={}, filters={}):
        self._query = query
        self._configs = configs or {
            'start': 0,
            'hit': 10,
            'format': 'json',
            'rerank_size': 200,
        }
        self._filters = filters or {}

    def set_config(self, key, value):
        self._configs[key] = value

    def set_query(self, query):
        self._query = query

    def set_filter(self, key, value):
        self._filters[key] = value

    def serialize(self):
        return '='.join(['config', ','.join([':'.join([k, v]) for k, v in
                                            self._configs.items()])])

    def __and__(self, x):
        return self

    def __or__(self, x):
        return self


class Query(object):

    def __init__(self, *apps):
        self._apps = apps

    def set_query(self, query: QueryBuilder):
        self._query = query

    async def get(self, *fields):
        params = {
            'query': self._query,
            'fetch_fields': ';'.join(fields)
        }
        names = ','.join([app.name for app in self._apps])
        resp = await self._req(
            uri='/'.join([self._apps[0]._req.URI_PREFIX, names]),
            http_params=params
        )
        return resp.content['items'], resp.content['facet']

    async def multi_apps(self, *apps):
        pass


class Docsets(object):

    def __init__(self, app):
        self._app = app
        self._docs = []

    def add(self, doc):
        self._docs.append({
            "cmd": "add",
            "fields": doc
        })

    def update(self, doc):
        self.add(doc)

    def delete(self, doc):
        self._docs.append({
            "cmd": "delete",
            "fields": doc
        })

    async def commit(self):
        resp = await self._app._req(
            method='POST',
            uri='/'.join([
                self._app._req.URI_PREFIX,
                self._app.name,
                self._app._table,
                'actions',
                'bulk'
            ]),
            http_body=self._docs)
        assert resp.content.get('status') == 'OK', resp.content
        self._docs.clear()
        return resp.content.get('result')


class App(object):
    def __init__(self,
                 name='',
                 table='',
                 endpoint='',
                 accesskey_id=None,
                 accesskey_secret=None):
        self._name = name
        self._table = table
        self._endpoint = endpoint
        self._accesskey_id = accesskey_id
        self._accesskey_secret = accesskey_secret
        self._infomation = {}
        self._req = Request(endpoint, accesskey_id, accesskey_secret, self)

        self.docsets = Docsets(self)

    @property
    def name(self):
        return self._name

    @classmethod
    async def lists(cls, page=1, size=10):
        params = {'page': page, 'size': size}
        resp = await cls._req(
            http_params=params
        )
        apps = []
        append = apps.append
        for app in resp['result']:
            append(cls.from_infomation(app))

        return apps

    @classmethod
    def from_infomation(cls, info, req):
        app = cls(info['name'], req)
        app._infomation = info
        return app

    async def infomation(self):
        if not self._infomation:
            resp = await self._req(
                uri='/'.join([self._req.URI_PREFIX, self.name])
            )
            self._infomation = resp.content['result']
        return self._infomation


class Request(object):

    URI_PREFIX = '/v3/openapi/apps'

    def __init__(self,
                 endpoint='',
                 accesskey_id=None,
                 accesskey_secret=None,
                 app=None):
        self._endpoint = URL(endpoint)
        self._ak = accesskey_id
        self._sk = accesskey_secret
        self.app = app

    async def __call__(self,
                       method='GET',
                       uri='/v3/openapi/apps',
                       http_header=None,
                       http_params=None,
                       http_body=None):

        if http_body:
            body = json.dumps(http_body)
        else:
            body = ''
        headers = Headers.build(verb=method,
                                uri=uri,
                                access_key=self._ak,
                                secret=self._sk,
                                http_params=http_params or {},
                                http_body=body,
                                http_headers=http_header or {})

        async with ClientSession() as session:
            async with session.request(
                method,
                self._endpoint.with_path(uri),
                params=http_params,
                data=body,
                headers=headers
            ) as resp:
                return Response(resp.headers,
                                resp.status,
                                await resp.json())


class Headers(CIMultiDict):

    OS_PREFIX = 'OPENSEARCH'

    def _canonicalized_resource(self, uri, http_params):
        canonicalized = urllib.parse.quote(uri).replace('%2F', '/')

        if not http_params:
            return canonicalized
        sorted_params = sorted(
            http_params.items(),  # list?
            key=lambda http_params: http_params[0]
        )
        params = []
        for (key, value) in sorted_params:
            if value is None or len(value) == 0:
                continue

            params.append(
                '='.join([
                    urllib.parse.quote(key),
                    urllib.parse.quote(value)
                ])
            )

        return '?'.join([canonicalized, '&'.join(params)])

    def authorization(self,
                      uri,
                      access_key,
                      secret,
                      http_params):
        '''此处为签名代码实现.
        '''
        canonicalized = ''.join([
            '\n'.join([
                self._verb,
                self.get('Content-MD5', ''),
                self.get('Content-Type', ''),
                self.get('Date', ''),
                self._canonicalized()
            ]),
            self._canonicalized_resource(uri, http_params)
        ])

        signature_hmac = hmac.new(
            secret.encode('utf-8'),
            canonicalized.encode('utf-8'),
            'sha1'
        )
        signature = base64.b64encode(signature_hmac.digest())
        return ' '.join([
            self.OS_PREFIX,
            ''.join([
                access_key,
                ':',
                signature.decode('utf-8')
            ])
        ])

    def utctime(self, datefmt="%Y-%m-%dT%H:%M:%SZ", timestamp=None):
        if timestamp is None:
            return time.strftime(datefmt, time.gmtime())
        else:
            return time.strftime(datefmt, timestamp)

    def generate_nonce(self):
        return str(int(time.time()*100)) + str(random.randint(1000, 9999))

    def _canonicalized(self):
        headers = {}
        for key, value in self.items():
            if key is None or value is None:
                continue
            k = key.strip(' \t')
            v = value.strip(' \t')
            if k.startswith('X-Opensearch-') and len(v) > 0:
                headers[k.lower()] = v

        if len(headers) == 0:
            return ''

        sorted_headers = sorted(
            list(headers.items()),
            key=lambda headers: headers[0]
        )
        canonicalized = ''
        for (key, value) in sorted_headers:
            canonicalized += (key.lower() + ':' + value + '\n')

        return canonicalized

    @classmethod
    def build(cls,
              verb,
              uri,
              access_key,
              secret,
              http_params,
              http_body,
              http_headers):
        '''构建Request Header.
        '''
        headers = cls(http_headers)
        headers._verb = verb
        if http_body is not None:
            if 'Content-MD5' not in headers:
                headers['Content-MD5'] = (hashlib
                                          .md5(http_body.encode('utf8'))
                                          .hexdigest())
        else:
            headers['Content-MD5'] = ''
        if 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'
        if 'Date' not in headers:
            headers['Date'] = headers.utctime()
        if 'X-Opensearch-Nonce' not in headers:
            headers['X-Opensearch-Nonce'] = headers.generate_nonce()
        if 'Authorization' not in headers:
            headers['Authorization'] = headers.authorization(uri,
                                                             access_key,
                                                             secret,
                                                             http_params)
        key_del = []
        for key, value in headers.items():
            if value is None:
                key_del.append(key)

        for key in key_del:
            del headers[key]

        return headers


async def main():
    accesskey_id = ''
    accesskey_secret = ''
    # 下面host地址，替换为访问对应应用api地址，例如华东1区
    app_name = 'hotel_names'
    endpoint = 'http://opensearch-cn-beijing.aliyuncs.com'

    # api = Request(
    #     endpoint=endpoint,
    #     app=App(app_name, '', None, None),
    #     accesskey_id=accesskey_id,
    #     accesskey_secret=accesskey_secret,
    # )
    app = App(app_name, 'en_names', endpoint, accesskey_id, accesskey_secret)
    # 下面为设置查询信息，query参数中可设置对应的查询子句，添加查询参数，
    # 参考fetch_fields用法
    # query_subsentences_params = {
    #     'query': "&&".join(["query=name:'hotel~0.5'",
    #                         "config=start:0,hit:500,format:json",
    #                         "sort=+id"]),
    #     'fetch_fields': 'id;name'
    # }
    from tasks import settings
    from motor.motor_asyncio import AsyncIOMotorClient as Motor
    db = Motor(settings.DATABASES['scripture']).get_database()
    idx = 0
    async for doc in db.statics.hotels.hotelbeds.find():
        app.docsets.add({
            'id': '_'.join(['hb', str(doc['_id'])]),
            'name': doc['name']
        })
        if idx % 100 == 0:
            resp = await app.docsets.commit()
            print(idx, resp)
        idx += 1
    # resp = await api(
    #     uri='/'.join([app._req.URI_PREFIX, app.name, 'search']),
    #     http_params=query_subsentences_params,
    #     http_header={}
    # )
    # docset = Docset(App(app_name, endpoint, accesskey_id, accesskey_secret))
    # print(json.dumps(resp.content['result'], indent=2))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
