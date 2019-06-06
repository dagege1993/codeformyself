# coding: utf-8
import json
import logging
import time
import redis
from datetime import datetime, timedelta
from bson import ObjectId
from aioredis import create_redis
from api import settings
from api.utils.database import databases, redis_db
from api.types.handler import BaseHandler
from api.utils.serializers import on_json_dumps
from api.spider.engine import BaseEngine
from api.spider.availability.ctrip import CtripSpider
from api.settings import configs
from api.types.consts import const

spider_list = [('ctrip', CtripSpider)]

base_engine = BaseEngine('baseEngine')
spider_cache = {}


class AvaiCompetitor(BaseHandler):

    async def prepara(self):
        await super().prepare

    async def post(self, *args, **kwargs):
        logger = self.logger.getChild('post')
        body = json.loads(self.request.body.decode('utf-8'))
        msg = {
            'hotel_id': body['hotel_id'],
            'checkin': body['checkin'],
            'checkout': body['checkout'],
            'roomfilters': body['roomfilters'],
        }
        logger.info(f"body: {body}")
        key = json.dumps(msg)
        redis_conn = await redis_db('redis')
        prices = await redis_conn.get(key)
        if prices is None:
            logger.info('Parameter expired, re-crawl')
            logger.info(key)
            spiders = find_spider(**body)
            prices = await do_crawl(spiders=spiders.values(), **msg)
            await redis_conn.psetex(key, configs[const.REDIS_EXPIRE_TIME], json.dumps(prices))
            logger.info(f"body: {body} response: {prices}")
        else:
            logger.info('The parameter has not expired, get it directly')
            logger.info(key)
            prices = json.loads(prices)
        return self.write(
            on_json_dumps(
                {'status_code': 200, 'data': prices}
            )
        )


class PrepCompetitor(BaseHandler):

    async def prepara(self):
        await super().prepare

    async def post(self, *args, **kwargs):
        logger = self.logger.getChild('post')
        body = json.loads(self.request.body.decode('utf-8'))
        logger.info(f"body: {body}")
        key = body.get('key')
        if not key:
            return self.write(
                on_json_dumps(
                    {'status_code': 400, 'data': {}, 'errmsg': 'availability key can not be None'}
                )
            )
        rds = await redis_db('redis')
        data = await rds.get(f"competitor::prep::{key}")
        if not data:
            return self.write(
                on_json_dumps(
                    {'status_code': 400, 'data': {}, 'errmsg': f'availability key: {key} expired'}
                )
            )
        data = json.loads(data)
        '''
        data : {
            'hotel_id': '',
            'website': '',
            'query': ''
        }
        '''
        logger.info(f'data: {data}')
        spider = spider_cache[data['hotel_id']][data['website']]
        prices = await spider.prep(key, data['query'])
        logger.info(f'prep_prices: {prices}')
        return self.write(
            on_json_dumps(
                {'status_code': 200, 'data': prices}
            )
        )


async def do_crawl(
        hotel_id=None, checkin=None, checkout=None,
        roomfilters=None,
        spiders=None,
        engine=base_engine,
        **kwargs
):
    hub = databases('hub')
    hotel = await hub['poi_items'].find_one({"_id": ObjectId(hotel_id)}, {'name_en'})
    hotel_name = hotel.get('name_en', '')
    rooms = await engine.crawl(
        spiders,
        **{
            'hotel_id': hotel_id,
            'checkin': checkin,
            'checkout': checkout,
            'roomfilters': roomfilters,
            'hotel_name': hotel_name,
            **kwargs,
        }
    )
    res = {'rooms': rooms, 'hotel_name': hotel_name, 'currency': 'CNY', 'timezone': '+08:30:00'}
    return res


def find_spider(hotel_id, *args, **kwargs):
    if hotel_id not in spider_cache:
        spiders = {
            website:
                spider(hotel_id=hotel_id, *args, **kwargs)
            for website, spider in spider_list
        }
        spider_cache[hotel_id] = spiders
    return spider_cache[hotel_id]
