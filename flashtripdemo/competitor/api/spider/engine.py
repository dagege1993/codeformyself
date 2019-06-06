# coding: utf-8

import aioredis
import aiohttp
import logging
from .base_spider import BaseSpider


class BaseEngine:

    def __init__(self, name):
        self.name = name
        self.sess = aiohttp.ClientSession()

    async def crawl(self, spiders, **kwargs):
        logger = logging.getLogger(__name__)
        logger.info(f"kwargs: {kwargs}")
        res = []
        for spider in spiders:
            res.extend(await spider.crawl(sess = self.sess, **kwargs))
        return res