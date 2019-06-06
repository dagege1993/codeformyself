# coding: utf8

# Standard Library
import logging
from typing import Dict

# Third Party
from sanic.server import HttpProtocol
from sanic.response import HTTPResponse


def access_log(extra: Dict) -> None:
    logging.getLogger('access').info('access', extra=extra)


class HttpProto(HttpProtocol):

    def log_response(self, response: HTTPResponse) -> None:
        if self.access_log and self.request.path != '/healthcheck':
            extra = {
                'status': getattr(response, 'status', 0),
            }

            if isinstance(response, HTTPResponse):
                extra['byte'] = len(response.body)
            else:
                extra['byte'] = -1

            extra['host'] = 'UNKNOWN'
            if self.request is not None:
                if self.request.ip:
                    extra['host'] = '{0[0]}:{0[1]}'.format(self.request.ip)

                extra['request'] = '{0} {1}'.format(self.request.method,
                                                    self.request.url)
            else:
                extra['request'] = 'nil'

            access_log(extra)
