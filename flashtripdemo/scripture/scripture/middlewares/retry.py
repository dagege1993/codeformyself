import json

import requests
import logging

from twisted.internet import defer
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
from twisted.internet.error import TimeoutError, DNSLookupError, \
    ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from twisted.web.client import ResponseFailed
from scrapy.core.downloader.handlers.http11 import TunnelError


class LocalRetryMiddleware(RetryMiddleware):
    logger = logging.getLogger(__name__)
    ALL_EXCEPTIONS = (defer.TimeoutError, TimeoutError, DNSLookupError,
                      ConnectionRefusedError, ConnectionDone, ConnectError,
                      ConnectionLost, TCPTimedOutError, ResponseFailed,
                      IOError, TunnelError)

    # 捕获这个报错，并返回request，让他重新请求这个对象
    def process_exception(self, request, exception, spider):
        if isinstance(exception, TimeoutError):
            return request

        if isinstance(exception, self.ALL_EXCEPTIONS):
            # 删除代理,然后重新请求
            proxy = request.meta.get('proxy', False)
            proxy = proxy.replace('http://', '')
            # url = "http://172.16.4.110:4010/api/v1/proxy"
            url = "http://scripture.weegotr.com/api/v1/proxy"
            payload = {"website": "tripadvisor"}
            payload['proxy'] = proxy
            payload = json.dumps(payload)
            delete_response = requests.request("GET", url, data=payload)
            # self.logger.info('process_exception开始删除代理')

            if delete_response.status_code == 200:
                pass
            else:
                self.logger.info('process_exception删除代理%s失败' % proxy)

            return self._retry(request, exception, spider)

    def process_response(self, request, response, spider):

        
        self.retry_http_codes = [403, 404, 500, 503, 504, 400, 408]
        # 检查状态码是否在列表中，在的话就调用_retry方法进行重试
        if response.status in self.retry_http_codes:

            # url = "http://172.16.4.110:4010/api/v1/proxy"
            url = "http://scripture.weegotr.com/api/v1/proxy"
            payload = {"website": "tripadvisor"}
            proxy = request.meta.get('proxy', False)
            proxy = proxy.replace('http://', '')
            payload['proxy'] = proxy
            payload = json.dumps(payload)
            delete_response = requests.request("GET", url, data=payload)
            # self.logger.info('process_response开始删除代理')
            if delete_response.status_code == 200:
                pass
            else:
                self.logger.info('process_response删除代理%s失败' % proxy)
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        return response
