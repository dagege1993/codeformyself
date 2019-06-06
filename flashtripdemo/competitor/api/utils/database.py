# coding: utf8
from gino import Gino
from aioredis import create_redis
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient

from api import settings


_db = None
_db_cache = {}


def databases(name):
    if name not in _db_cache:
        connection = MongoClient(settings.DATABASES[name])
        _db_cache[name] = connection.get_database()
    return _db_cache[name]


async def redis_db(name):
    if name not in _db_cache:
        connection = await create_redis(settings.DATABASES[name])
        _db_cache[name] = connection
    return _db_cache[name]
