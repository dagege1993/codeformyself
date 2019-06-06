# coding: utf-8
import logging
from datetime import datetime, timedelta

import aiohttp
from bson import ObjectId
from sanic.response import json
from yarl import URL

from web import settings
from web.utils import add_compair_task
from web.utils.database import databases
from web.models.quotes import PullDown as pulldown

from . import api_v1
from .formatter_response import rest_result

logger = logging.getLogger(__name__)
city_maps = {}

@api_v1.post('/record/quotes')
async def record_quotes(request):
    request.headers['accept'] = 'application/json'
    hub = databases('hub')
    body = request.json
    if not body:
        return rest_result(
            request,
            {'status': 400, 'errmsg': 'body must be non-empty!'}
        )
    body['query_time'] = datetime.utcfromtimestamp(int(body['time_stamp']))
    cms_id = body.get('cms_hotel_id')
    if not cms_id:
        logger.error(f"invalid request without cms_id\n{body}")
        return rest_result(
            request,
            {'status': 400, 'errmsg': 'cms_id: {cms_id} illegal.'}
        )
    else:
        logger.info(f"save pull_down data with {body}")
    cms = await hub['poi_items'].find_one({"_id": ObjectId(cms_id)}, {'city': '1'})
    if not cms.get('city'):
        logger.error(f"invalid cms id : {cms_id} without city")
        return 
    if cms['city'] not in city_maps:
        city = await hub['meta_cities'].find_one({"_id": cms['city']}, {'name': '1'})
        if not city:
            logger.error(f"")
            body['city'] = 'Unknown'
        else:
            city_maps[cms['city']] = city['name']
    body['city'] = city_maps[cms['city']]

    body.pop('time_stamp', '')

    resp = await pulldown.create(**body)
    return rest_result(
        request,
        {'status': 200, 'data': resp.to_dict()}
    )
    