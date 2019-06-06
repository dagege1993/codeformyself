# coding: utf-8
from random import choice

from api.utils.database import databases, redis_db
from api.settings import configs
from api.types.consts import const

class BaseSpider:

    @property
    def proxy(self):
        ...
    

    @property
    def UA(self):
        return choice(
            configs[const.UA]
        )
    

    @property
    def referer(self):
        ...
    

    @property
    def host(self):
        ...
    

    def get_cookie(self):
        ...
    

    def update_cookie(self, *args, **kwargs):
        ...


    async def cache_write(self, key, value, *args, **kwargs):
        rdb = await redis_db('redis')
        await rdb.psetex(key, configs[const.REDIS_EXPIRE_TIME], value)
        return True
    

    async def cache_read(self, key, *args, **kwargs):
        rdb = await redis_db('redis')
        data = await rdb.get(key)
        return data
        


    async def crawl(self, *args, **kwargs):
        raise NotImplementedError()
    

    async def handler(self, response, *args, **kwargs):
        raise NotImplementedError()
