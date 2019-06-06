# coding: utf8
from gino import Gino
from aioredis import create_redis
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient

from web import settings


_db = None
_db_cache = {}


def connection(name=None):
    global _db

    if not _db:
        _db = MongoClient('mongodb://172.17.1.201:27017')

    return _db


def databases(name):
    if name not in _db_cache:
        connection = MongoClient(settings.DATABASES[name])
        _db_cache[name] = connection.get_database()
    return _db_cache[name]


def pg_databases(name):
    if name not in _db_cache:
        connection = Gino()
        _db_cache[name] = connection
    return _db_cache[name]


async def redis_db(url):
    if url not in _db_cache:
        connection = await create_redis(url)
        _db_cache[url] = connection
    return _db_cache[url]
