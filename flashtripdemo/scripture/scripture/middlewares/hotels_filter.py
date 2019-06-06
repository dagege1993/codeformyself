# coding: utf8

import logging

from scrapy import signals

from scrapy.exceptions import IgnoreRequest

from pymongo import MongoClient


class HotelsFilterMiddleware:
    logger = logging.getLogger(__name__)

    def __init__(self, settings):
        self.settings = settings
        self._filter = lambda x: None

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls(crawler.settings)
        crawler.signals.connect(
            middleware.spider_opened,
            signal=signals.spider_opened
        )
        return middleware

    def spider_opened(self, spider):
        if spider.name != 'hotels':
            return None
        self._filter = self._for_hotels_request
        m = MongoClient(self.settings.get('MONGO'))
        # TODO: add english city and country
        self.cities = list(map(
            self.comb_by_pinyin,
            m.scripture.cities.find(
                {},
                {'pinyin': 1, 'country_pinyin': 1, 'en_name': 1}
            )
        ))
        self.logger.info('Loaded online cities: %d', len(self.cities))

    def comb_by_pinyin(self, item):
        try:
            # return '-'.join([item['pinyin'], item['country_pinyin']]) \
            #     .replace(' ', '-').lower()
            return item['en_name'].replace(' ', '-').lower()
        except KeyError as e:
            self.logger.error('City is broken! %s', item)
            self.logger.exception(e)

    def _for_hotels_request(self, request):
        return
        if request.url.endswith(('.xml', 'robots.txt')):
            return
        if request.url.endswith('.xml.gz'):
            if 'www.hotels.cn/HOTEL_cn_hotels_com_' in request.url:
                return
            else:
                raise IgnoreRequest(request.url)
        if request.url.startswith('https://www.hotels.com/ho'):
            # TODO: remove this after english city and country is added
            return
        if request.url.startswith(
            ('https://www.hotels.cn/hotel/', 'https://www.hotels.com/hotel/')
        ):
            # TODO: 评论和房间详情
            return
        name_and_city = request.url.strip('/').split('/')[-1]
        filtered = filter(
            lambda city: name_and_city.endswith(city),
            self.cities
        )
        if len(list(filtered)) == 0:
            raise IgnoreRequest(request.url)

    def process_request(self, request, spider):
        return self._filter(request)
