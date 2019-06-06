# coding: utf8

# Standard Library
import logging
import json

import redis
from yarl import URL
from datetime import datetime

from web import settings

logger = logging.getLogger(__name__)
redis_conn = redis.from_url(settings.REDIS)


def get_compare_prices(url, cms_id, start_time, days, spider_name='booking_prices', **kwargs):
    _url = URL(url)
    if _url.host not in ['www.booking.com', 'm.ctrip.com']:
        logger.info(f"invalid params : {url}")
        return False
    base_url = f"{_url.scheme}://{_url.host}{_url.path}"
    try:
        days = int(days)
        checkin = datetime.strptime(start_time, '%Y-%m-%d')
        checkin = checkin.strftime('%Y-%m-%d')
    except Exception as exc:
        logger.info(f"invalid params", exc_info=exc)
        return False
    to_redis = json.dumps(
        {
            'spider_name': spider_name,
            'base_url': base_url,
            'cms_id': cms_id,
            'start_time': checkin,
            'days': days,
            **kwargs,
        }
    )
    try:
        redis_conn.lpush('distributed_spider', to_redis)
        return True
    except Exception as exc:
        logger.warning(f"redis 异常", exc_info=exc)
        return False

