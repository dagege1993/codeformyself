import requests
import re
import random

from yarl import URL
from lxml import etree
from datetime import datetime, timedelta
from celery.utils.log import get_task_logger
from simhash import Simhash

from tasks.application import app
from scripture.settings import USER_AGENT_LIST
from scripture.xpath import bookings_v2 as bk
from tasks import settings
from tasks.utils.database import databases
from tasks.utils.parse_element import safe_xpath, dingding, find_price, get_policies

logger = get_task_logger('tasks')

@app.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 5})
def _check_prices(**kwargs):
    days = kwargs.get('days')
    check_num = int(days / settings.CHECK_PRICE_FREQUENCY) + 1
    checkin_str = kwargs.get('start_time')
    _base_url = URL(kwargs.get('base_url'))
    cms_id = kwargs.get('cms_id')
    for i in range(check_num):
        checkin = datetime.strptime(checkin_str, '%Y-%m-%d')
        checkout_str = (
            checkin + timedelta(days=1)
        ).strftime('%Y-%m-%d')
        url = _base_url.with_query({
            'checkin_year': checkin_str[:4],
            'checkin_month': checkin_str[5:7],
            'checkin_monthday': checkin_str[8:],
            'checkout_year': checkout_str[:4],
            'checkout_month': checkout_str[5:7],
            'checkout_monthday': checkout_str[8:],
        })
        user_agent = random.choice(USER_AGENT_LIST)
        resp = requests.get(
            str(url),
            headers={'User-Agent': user_agent}
        )
        new_prices = parse_booking_prices(resp)
        compare_data(new_prices,checkin_str,cms_id,url)
        checkin_str = (
            checkin + timedelta(days=settings.CHECK_PRICE_FREQUENCY)
        ).strftime('%Y-%m-%d')

def parse_booking_prices(resp):
    url = resp.url
    if resp.status_code != 200:
        logger.info(f'校验({url})失败, StatusCode({resp.status_code})')
        return False
    et = etree.HTML(resp.content.decode())
    prices_tr_list = et.xpath(bk.PRICES_TABLE_TR)
    if len(prices_tr_list) == 0:
        logger.info(f'所有房间已售出,校验({url})失败)')
        return False
    new_prices = []
    for index, tr in enumerate(prices_tr_list):
        if tr.xpath('.' + bk.ROOM_TYPE):
            room_type = safe_xpath(tr, bk.ROOM_TYPE, 'room_type')
            if index == 0 and not room_type:
                logger.error(f'网页[{url}]解析规则变更')
                return False
        price = tr.xpath('.' + bk.ROOM_PRICE)
        if price:
            price = find_price(url, price[0])
            price_tax = safe_xpath(tr, bk.ROOM_PRICE_TAX, 'price_tax')
            if price_tax and not re.search('含税费', price_tax):
                price += find_price(url, price_tax)
            policies = get_policies(tr.xpath('.' + bk.ROOM_POLICIES))
            occupancy = safe_xpath(tr,bk.ROOM_OCCUPANCY,'occupancy')
            one_room_price = {
                'occupancy': occupancy,
                'room_type': room_type,
                'price': price,
                'policies': policies,
            }
            new_prices.append(one_room_price)
        else:
            policies = tr.xpath('.' + bk.ROOM_SOLD_OUT)
            print(policies)
            if not policies:
                continue
            policies = safe_xpath(tr, bk.ROOM_SOLD_OUT, 'policies')
            price = find_price(url, policies.strip())
            occupancy = safe_xpath(tr, bk.ROOM_OCCUPANCY, 'occupancy')
            one_room_price = {
                'occupancy': occupancy,
                'room_type': room_type,
                'price': price,
                'policies': policies,
            }
            new_prices.append(one_room_price)
    return new_prices

def compare_data(new_prices,checkin_str,cms_id,url):
    scripture = databases('scripture')
    db_prices = scripture.statics.booking.prices.find_one(
        {"cms_id": cms_id, 'prices.checkin': checkin_str},
        {
            'prices.$': 1
        }
    )
    if not db_prices and new_prices:
        logger.error(f'爬虫失效/数据库失连,数据库cms_id:{cms_id},目标url:{url}')
        title = 'booking_prices爬虫失效/数据库失连'
        text = f'## [告警]booking爬虫失效\n,数据库cms_id:{cms_id},目标url:{url}'
        dingding(title, text)
    elif db_prices and not new_prices:
        logger.error(f'比价模块失效,数据库cms_id:{cms_id},目标url:{url}')
        title = 'booking_prices比价模块失效'
        text = f'## [告警]booking比价模块失效\n,数据库cms_id:{cms_id},目标url:{url}'
        dingding(title, text)
    elif db_prices and new_prices:
        db_prices = db_prices.get('prices')[0].get('prices')
        new_prices_info = {}
        for one_room_dict in new_prices:
            room_info_hash = Simhash(
                f'{one_room_dict["occupancy"]}{one_room_dict["room_type"]}{one_room_dict["policies"]}'
            ).value
            new_prices_info[room_info_hash] = one_room_dict["price"]
        for one_room_dict in db_prices:
            room_info_hash = Simhash(
                f'{one_room_dict["occupancy"]}{one_room_dict["room_type"]}{one_room_dict["policies"]}'
            ).value
            db_one_room_price = one_room_dict.get('price')
            new_one_room_price = new_prices_info.get(room_info_hash)
            if not new_one_room_price:
                logger.info(f'{kwargs}在{checkin_str}的房型({one_room_dict["room_type"]})已售出')
            if compare_price(db_one_room_price, new_one_room_price):
                _info = {
                    'url': url,
                    'checkin': checkin_str,
                    'room_type': one_room_dict["room_type"],
                    'mongodb_price': db_one_room_price,
                    'celery_task_get_price': new_one_room_price
                }
                title = 'booking_prices异常'
                text = f'## [告警]booking抓取价格异常\n{_info}'
                dingding(title, text)

def compare_price(db_price, new_price):
    if db_price * settings.CHECK_PRICE_SIMILARITY \
            < new_price < \
                    db_price * (1 + settings.CHECK_PRICE_SIMILARITY):
        return False
    return True
