# coding: utf-8

import logging
from datetime import datetime, date
from decimal import Decimal
from enum import Enum, EnumMeta
from ipaddress import IPv4Address

from dateutil import tz
from gino.crud import CRUDModel


def on_json_dumps(obj):
    logger = logging.getLogger(f'{__name__}.on_json_dumps')
    if obj is None:
        return obj
    if isinstance(obj, (int, float, str, bool)):
        return obj
    if isinstance(obj, (list, tuple)):
        return [on_json_dumps(o) for o in obj]
    if isinstance(obj, dict):
        return {key: on_json_dumps(val) for key, val in obj.items()}
    if isinstance(obj, CRUDModel):
        return on_json_dumps(obj.to_dict())
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, EnumMeta):
        return {val.name: val.value for val in obj.__members__.values()}
    if isinstance(obj, (Decimal, IPv4Address)):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.astimezone(tz.tzlocal()).strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')
    logger.warning(f'Unexpected obj, with type {type(obj)}: {obj}')
