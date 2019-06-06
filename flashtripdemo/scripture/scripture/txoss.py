# coding: utf8

import os
import hmac
import base64
import hashlib
import mimetypes

from urllib.parse import quote
from email.utils import formatdate

import treq

from twisted.internet import defer


_EXTRA_TYPES_MAP = {
    ".js": "application/javascript",
    ".xlsx": "application/"
             "vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".xltx": "application/"
             "vnd.openxmlformats-officedocument.spreadsheetml.template",
    ".potx": "application/"
             "vnd.openxmlformats-officedocument.presentationml.template",
    ".ppsx": "application/"
             "vnd.openxmlformats-officedocument.presentationml.slideshow",
    ".pptx": "application/"
             "vnd.openxmlformats-officedocument.presentationml.presentation",
    ".sldx": "application/"
             "vnd.openxmlformats-officedocument.presentationml.slide",
    ".docx": "application/"
             "vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".dotx": "application/"
             "vnd.openxmlformats-officedocument.wordprocessingml.template",
    ".xlam": "application/vnd.ms-excel.addin.macroEnabled.12",
    ".xlsb": "application/vnd.ms-excel.sheet.binary.macroEnabled.12",
    ".apk": "application/vnd.android.package-archive"
}


class OSS:

    _subresource_key_set = frozenset({
        'response-content-type', 'response-content-language',
        'response-cache-control', 'logging', 'response-content-encoding',
        'acl', 'uploadId', 'uploads', 'partNumber', 'group', 'link',
        'delete', 'website', 'location', 'objectInfo', 'objectMeta',
        'response-expires', 'response-content-disposition', 'cors',
        'lifecycle', 'restore', 'qos', 'referer', 'stat', 'bucketInfo',
        'append', 'position', 'security-token', 'live', 'comp', 'status',
        'vod', 'startTime', 'endTime', 'x-oss-process',
        'symlink', 'callback', 'callback-var'
    })

    def __init__(self, ak, sk, endpoint, bucket):
        self._ak = ak
        self._sk = sk
        self._bucket = bucket
        self._endpoint = lambda key: '/'.join([endpoint, bucket, key])

    @staticmethod
    def content_type_by_name(name):
        """根据文件名，返回Content-Type。"""
        ext = os.path.splitext(name)[1].lower()
        if ext in _EXTRA_TYPES_MAP:
            return _EXTRA_TYPES_MAP[ext]

        return mimetypes.guess_type(name)[0]

    @defer.inlineCallbacks
    def head_object(self, object_path):
        resp = yield self.with_signature(
            'HEAD',
            object_path,
            params={'objectMeta': ''}
        )
        return resp

    @defer.inlineCallbacks
    def get_object(self, object_path, headers=None):
        resp = yield self.with_signature(
            'GET',
            object_path,
            headers=headers
        )
        return resp

    @defer.inlineCallbacks
    def put_object(self, object_path, data, headers=None):
        content_type = self.content_type_by_name(object_path)
        headers = headers or {}
        if content_type:
            headers['Content-Type'] = content_type
        resp = yield self.with_signature(
            'PUT',
            object_path,
            headers=headers,
            data=data
        )
        return resp

    @defer.inlineCallbacks
    def with_signature(self, meth, object_path, params=None, data=None,
                       headers=None):
        meth = meth.upper()
        subresources = []
        for key, value in params.items():
            if key in self._subresource_key_set:
                subresources.append((key, value))
        subresources.sort(key=lambda p: p[0])
        _subresources = '&'.join((
            "=".join([k, v])
            if v else k
            for k, v in subresources
        ))
        resources_string = '&'.join([
            f'/{self._bucket}/{object_path}',
            _subresources
        ])

        headers = headers or {}
        headers['date'] = formatdate(None, usegmt=True)

        headers_string = '\n'.join([
            ':'.join([k, v])
            for k, v in sorted(
                [
                    (k.lower(), v)
                    for k, v in headers.items()
                    if k.lower().startswith('x-oss-')
                ],
                key=lambda h: h[0]
            )
        ])

        if headers_string:
            headers_string += '\n'

        content_md5 = headers.get('content-md5', '')
        content_type = headers.get('content-type', '')

        _string_to_sign = '\n'.join([
            meth,
            content_md5,
            content_type,
            headers['date'],
            ''.join([headers_string, resources_string])
        ])

        h = hmac.new(
            self._sk.encode(),
            _string_to_sign.encode(),
            hashlib.sha1
        )

        _signature = base64.b64encode(h.digest()).decode()

        headers["Authorization"] = f"OSS {self._ak}:{_signature}"
        params['OSSAccessKeyId'] = self._ak
        params['Signature'] = _signature

        url = '?'.join([
            self._endpoint(object_path),
            '&'.join([
                '='.join([quote(k, ''), quote(v, '')])
                if v else quote(k, '')
                for k, v in params.items()
            ])
        ])

        response = yield treq.request(
            meth,
            url,
            data=data,
            params=params,
            headers=headers
        )

        return response
