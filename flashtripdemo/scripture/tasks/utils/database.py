# coding: utf8
"""
Created by songww
"""
import logging

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.read_preferences import _ServerMode, ReadPreference

from tasks import settings


__DB = None  # type: MongoClient
__DB_INSTANCE = {}  # type: Dict[str, Database]

logger = logging.getLogger(__name__)  # pylint: disable=C0103


def connection() -> MongoClient:
    """Decrapted"""
    global __DB   # pylint: disable=W0603

    if not __DB:
        __DB = MongoClient('mongodb://172.17.1.201:27017')

    return __DB


def databases(name: str,
              read_preference: _ServerMode = ReadPreference.PRIMARY
              ) -> Database:
    """Get database by alias name.
    Args: name
    """
    if name not in __DB_INSTANCE:
        _connection = MongoClient(settings.DATABASES[name])
        __DB_INSTANCE[name] = _connection.get_database(
            read_preference=read_preference
        )
    return __DB_INSTANCE[name]
