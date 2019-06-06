# coding: utf8

# Standard Library
import logging
import json

from web.utils.database import databases
from yarl import URL
from datetime import datetime

from web import settings
from tasks.check_prices import _check_prices
from web.utils.japanican_spider import start_crawl_japanican

logger = logging.getLogger(__name__)


async def get_booking_prices(url, cms_id, start_time, days, spider_name='booking_prices', **kwargs):
    rds = databases(settings.REDIS)
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
    if not 0 < days < 91:
        logger.info(f"invalid params : {days}")
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
        await rds.lpush('distributed_spider', to_redis)
        return True
    except Exception as exc:
        logger.warning(f"redis 异常", exc_info=exc)
        return False


async def start_compair(websites, compair):
    rds = databases(settings.REDIS)
    to_redis = json.dumps(
        {
            'spider_name': 'compair',
            'websites': websites,
            'compair': compair
        }
    )
    try:
        await rds.lpush('distributed_spider', to_redis)
        return True
    except Exception as exc:
        logger.warning(f"redis 异常", exc_info=exc)
        return False


async def start_ta_spider(city, country, allow_num, lost_city, filter_or_not):
    rds = databases(settings.REDIS)
    to_redis = json.dumps(
        {
            'city': city,
            'country': country,
            'allow_num': allow_num,
            'lost_city': lost_city,
            'filter_or_not': filter_or_not,
            'spider_name': 'tripadvisor'
        }
    )
    try:
        await rds.lpush('distributed_spider', to_redis)
        return True
    except Exception as exc:
        # logger.warning(f"redis 异常", exc_info=exc)
        return False


async def start_ja_spider():
    start_crawl_japanican()
