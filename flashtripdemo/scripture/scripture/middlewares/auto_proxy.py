# coding: utf8

import logging
from scrapy import signals
from scripture.utils import refresh_ip
from twisted.internet.defer import DeferredLock


class AutoProxyMiddleware:

    logger = logging.getLogger(__name__)

    crawled_times = 0

    lock = DeferredLock()

    enabled = False

    def __init__(self, proxy, crawler):
        self.crawler = crawler
        self.http_proxy = proxy

    @classmethod
    def from_crawler(cls, crawler):
        c = cls(crawler.settings.get('HTTP_PROXY'), crawler)
        crawler.signals.connect(c.spider_opened, signal=signals.spider_opened)
        return c

    def process_request(self, request, spider):
        if not self.enabled:
            return
        request.meta['proxy'] = self.http_proxy
        AutoProxyMiddleware.crawled_times += 1
        if AutoProxyMiddleware.crawled_times <= 500:
            return
        if AutoProxyMiddleware.lock.locked:
            return
        AutoProxyMiddleware.lock.acquire()
        self.crawler.engine.pause()
        self.logger.info('Out ip chnaged to: %s', refresh_ip())
        self.crawler.engine.unpause()
        AutoProxyMiddleware.crawled_times = 0
        AutoProxyMiddleware.lock.release()

    def spider_opened(self, spider):
        if hasattr(spider, 'enable_proxy') and spider.enable_proxy:
            self.enable()
        else:
            self.disable()

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True
