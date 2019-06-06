# coding: utf8

import json as jsonlib
import logging

from aioredis import create_redis
from sanic import Blueprint
from sanic.request import Request
from sanic.response import json

from web import settings

logger = logging.getLogger(__name__)
package_bp = Blueprint("package-prices", url_prefix="/views/package-prices")


@package_bp.get("/<date>")
async def view_prices(unused_request: Request, date: str):
    if not date:
        return json({"error": "参数缺失", "status": 400})
    R = await create_redis(settings.REDIS, db=3)
    cached = await R.lrange(f"package-checked-{date}", 0, -1)
    if not cached:
        return json({"error": "已经过期或者价格没有问题", "status": 404})
    values = []
    for v in cached:
        values.append(jsonlib.loads(v))
    return json(values)
