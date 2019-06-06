import json

import requests
import logging


class ProxyMiddleware(object):
    logger = logging.getLogger(__name__)

    def process_request(self, request, spider):
        try:
            proxy = requests.get('http://scripture.weegotr.com/api/v1/proxy?website=tripadvisor')
            proxy_response = json.loads(proxy.text)
            data = proxy_response.get('data')
            if len(data) > 0:  # 如果有代理,就添加代理
                ip = data.get('ip')
                port = data.get('port')
                ip = ip + ':' + port
                request.meta['proxy'] = "http://" + ip
                # self.logger.info('添加代理成功')
            else:  # 如果代理池为空,这样会不加代理发送请求
                self.logger.info('代理池为空,用本机IP发送请求')

        except Exception as e:
            self.logger.info('当前代理挂掉了')
            pass
