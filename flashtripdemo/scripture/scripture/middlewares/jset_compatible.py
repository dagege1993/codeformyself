# coding: utf8

import logging
from scrapy import signals
from scrapy.exceptions import IgnoreRequest

from pymongo import MongoClient

logger = logging.getLogger(__name__)


class JsetCompatibleMiddleware:

    def __init__(self, settings):
        self.settings = settings
        self._compat = lambda x: None

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        middleware = cls(settings)
        crawler.signals.connect(
            middleware.spider_opened,
            signal=signals.spider_opened
        )
        return middleware

    def _for_jset_request(self, request):
        if '.com/search/q=' in request.url:
            origin_url = request.url
            request.url = request.url.replace('/search/q=', '/search/?q=')
            logger.debug('(%s) is fixed to (%s)', origin_url, request.url)
            return

        if '.com/hotels/' in request.url:
            city = request.url.split('/')[4].replace('-', ' ').title()
            if city not in self.online_cities:
                logger.debug('City is: %s', city)
                logger.debug('IgnoreRequest %s', request.url)
                # raise IgnoreRequest(request.url)
            logger.debug('Add splash support for hotel page: %s', request.url)
            request.meta.update({
                'splash': {
                    'args': {
                        'html': 1,
                        'wait': 0.5,
                        'images': 0,
                        'resource_timeout': 5,
                        # 'proxy': 'socks5://127.0.0.1:1080'
                        'allowed_content_types': ','.join([
                            'text/html',
                            'application/javascript',
                            'application/json',
                        ]),
                        'filters': 'nofonts,easylist,fanboy-annoyance'
                    },
                    'endpoint': 'render.html',
                }
            })
            return

    def spider_opened(self, spider):
        if spider.name != 'jetsetter':
            return
        self._compat = self._for_jset_request
        m = MongoClient(self.settings.get('MONGO'))
        self.online_cities = list(map(
            lambda item: item['en_name'],
            m.scripture.cities.find(
                {},  # {'is_online': True},
                {'en_name': 1}
            )
        ))
        logger.info('Online cities: %s', self.online_cities)

    def process_request(self, request, spider):
        return self._compat(request)
