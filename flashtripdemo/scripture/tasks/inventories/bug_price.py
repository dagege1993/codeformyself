# coding: utf8

# Standard Library
import math
import logging
from datetime import datetime, timedelta

import requests
from yarl import URL
from bson import ObjectId
from lxml import etree
from tasks.utils.database import databases  # noqa
from tasks.utils.publish_booking import get_compare_prices

from web import settings as web_st
from tasks import settings as tasks_st
from .utils import find_each_min_supplier

quotes_api = web_st.QUOTES_API
calendar_days = 180
logger = logging.getLogger(__name__)
dele_time = tasks_st.BUG_PRICE_TASK_TIMEDELTA * 60

def update_bug_price_type(cms_id, checkin):
    hub = databases('hub')
    hotel = hub["poi_items"].find_one(
        {"_id": ObjectId(cms_id)},
        {"quote_ids": "1", "min_booking_days": "1", "city": "1"},
    )
    min_booking_days = int(hotel.get("min_booking_days", 1))
    checkout = (datetime.strptime(checkin, "%Y-%m-%d") + timedelta(days=min_booking_days)).strftime("%Y-%m-%d")
    payload = dict(
        checkin=checkin,
        checkout=checkout,
        roomfilters=[{"adults": 2}],
        quoters=[
            {"quoter": str(value["quoter"]), "hotel_id": value["hotel_id"]}
            for value in hotel["quote_ids"]
            if value["hotel_id"].strip() != ""
        ],
    )
    try:
        # 每个任务仅查询一个酒店的一个日期，只一次网络IO
        resp = requests.post(
            quotes_api, headers={"x-query-from": "robot"}, json=payload
        )
        res = resp.json()
    except Exception as exc:
        logger.error(
            f"{checkin} {hotel['_id']} get price faild!\ndetail : {resp.content}",
            exc_info=exc,
        )
        return db_update_type(cms_id, checkin, -1, {})

    if not res or res["status"] != 200 or not res["data"].get("categorized"):
        return db_update_type(cms_id, checkin, -1, {})
    _min_price_room = list(res["data"]["categorized"].values())[0][0]
    supplier_rooms = find_each_min_supplier(res["data"]["categorized"])
    _min_price = float(_min_price_room.get("total_price", 9999999))
    _min_supplier = _min_price_room.get("identity", {}).get(
        "provider", "Unknown"
    )
    _city_rate = hub['meta_cities'].find_one({"_id": hotel['city']}, {'tax_rate': '1'})
    if not _city_rate:
        city_rate = 0.05
    else:
        city_rate = float(_city_rate.get('tax_rate', 0.05))
    without_tax_price = math.ceil(_min_price * (1-city_rate))
    prices = {
        "checkin": checkin,
        "checkout": checkout,
        "price": _min_price,
        'without_tax_price': without_tax_price,
        "ori_price": float(
            _min_price_room.get("ori_total_price_cny", 9999999999999)
        ),
        "supplier": _min_supplier,
        "room_type_en": _min_price_room.get("room_type", ""),
        "room_type_cn": _min_price_room.get("translation", ""),
        "each_supplier": supplier_rooms,
        "updated_at": datetime.now(),
    }
    return db_update_type(cms_id, checkin, 1, prices)


def db_update_type(cms_id, checkin, price_type, prices):
    db = databases('scripture')
    condition = {'hotel_id': cms_id, 'prices.checkin': checkin}
    upload = {"$currentDate": {"updated_at": True}}
    price = prices['price']
    if price_type == -1 or not price or isinstance(price, str):
        upload['$set'] = {'prices.$.bug_price_type': -1}
    else:
        upload['$set'] = {'prices.$': prices}
        old_price = db['statics.hotels.prices'].find_one({'hotel_id': cms_id, 'prices.checkin': checkin}, {'prices.$'})
        # 正常不会出现此种情况，仅在发布任务的5分钟后原数据仍未更新到数据库中时才会出现，出现则抛弃此次查询结果
        if not old_price:
            logger.warning(f"bug_price_check_task_before_data_insert: {cms_id}, {checkin}")
            return
        thre_price = old_price['prices'][0].get('bug_thre_price', 0)
        if price > thre_price:
            upload['$set']['prices.$']['bug_price_type'] = 0
        else:
            upload['$set']['prices.$']['bug_price_type'] = 1
        upload['$set']['prices.$']['bug_thre_price'] = thre_price

    res = db['statics.hotels.prices'].update_one(
        condition,
        upload
    )

def get_next_day_of_week_timedelta(day, hour, minute):
    current_time = datetime.now()
    next_time = ''
    today = current_time.weekday()
    if today <= day:
        next_time = current_time + timedelta(days=day - today)
    else:
        next_time = current_time + timedelta(days=(7- (today - day)))
    next_time = next_time.replace(hour=hour, minute=minute, second=0)
    if next_time < current_time:
        next_time += timedelta(days=7)
    return (next_time - current_time).total_seconds()
