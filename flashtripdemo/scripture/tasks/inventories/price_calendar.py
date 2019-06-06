# coding: utf8

# Standard Library
import logging
import math
from datetime import datetime, timedelta

import requests
from bson import ObjectId
from tasks.utils.database import databases  # noqa

from web import settings
from tasks import settings as tsk_st
from .fix_imp import check_bug_price
from .utils import find_each_min_supplier

quotes_api = settings.QUOTES_API
default_calendar_days = 130
logger = logging.getLogger("celery.worker")
hub = databases("hub")
scripture = databases("scripture")
delay_time = tsk_st.BUG_PRICE_TASK_TIMEDELTA*60


def catch_one(hotel_id, start_time=None, end_time=None, days=default_calendar_days, do_bug_price=False):
    hotel = hub["poi_items"].find_one(
        {"_id": ObjectId(hotel_id)},
        {"quote_ids": "1", "min_booking_days": "1", "city": "1"},
    )
    if not hotel:
        logger.warning(f"hotel_id : {hotel_id} not find!")
        return
    price_save(hotel, start_time, end_time, days, do_bug_price)


def price_save(hotel, start_time=None, end_time=None, max_days=None, do_bug_price=False):
    logger.info(f"{hotel} {start_time} {end_time} {max_days} {do_bug_price}")
    hotel["id"] = str(hotel["_id"])
    min_booking_days = int(hotel.get("min_booking_days", 1))
    if not start_time:
        checkin = datetime.now() + timedelta(days=-1)
    else:
        # 由于下方会先+1天抓取，所以先-1天
        checkin = datetime.strptime(start_time, "%Y-%m-%d") + timedelta(days=-1)
    if end_time:
        days = (datetime.strptime(end_time, "%Y-%m-%d") - checkin).days
    elif max_days:
        days = max_days
    else:
        days = default_calendar_days
    checkout = checkin + timedelta(days=min_booking_days)
    prices = []
    sum_price = 0
    min_price = 9999999999999.0
    has_price_day = 0
    mode_price = 0
    mode_price_num = 0
    mode_price_count = {}
    avg_price = 0
    req_time = datetime.now()
    has_tf_id_error = False
    for i in range(days):
        checkin = checkin + timedelta(days=1)
        checkout = checkout + timedelta(days=1)
        payload = dict(
            checkin=checkin.strftime("%Y-%m-%d"),
            checkout=checkout.strftime("%Y-%m-%d"),
            roomfilters=[{"adults": 2}],
            quoters=[
                {
                    "quoter": str(value["quoter"]),
                    "hotel_id": value["hotel_id"],
                    "premium_ratio": value.get("premium_ratio", None),
                }
                for value in hotel["quote_ids"]
                if value["hotel_id"].strip() != "" or str(value["quoter"]) != '59c1f0f8e1812033000e1de8'
            ],
        )
        try:
            resp = requests.post(
                quotes_api, headers={"x-query-from": "robot"}, json=payload
            )
            res = resp.json()
        except Exception as exc:
            logger.error(
                f"{checkin} {hotel['_id']} get price faild!\ndetail : {resp.content}",
                exc_info=exc,
            )
            prices.append(
                {
                    "checkin": checkin.strftime("%Y-%m-%d"),
                    "checkout": checkout.strftime("%Y-%m-%d"),
                    'without_tax_price': "已抢光",
                    "price": "当日无报价",
                    "updated_at": datetime.now(),
                }
            )
            continue
        if not res or res["status"] != 200 or not res.get('data'):
            logger.warning(f"{checkin} {hotel['_id']} get price faild!")
            prices.append(
                {
                    "checkin": checkin.strftime("%Y-%m-%d"),
                    "checkout": checkout.strftime("%Y-%m-%d"),
                    'without_tax_price': "已抢光",
                    "price": "当日无报价",
                    "updated_at": datetime.now(),
                }
            )
            if 'not found travflex location data' in resp.content.decode('utf-8'):
                has_tf_id_error = True
            continue
        if not res["data"].get("categorized"):
            prices.append(
                {
                    "checkin": checkin.strftime("%Y-%m-%d"),
                    "checkout": checkout.strftime("%Y-%m-%d"),
                    'without_tax_price': "已抢光",
                    "price": "当日无报价",
                    "updated_at": datetime.now(),
                }
            )
            if 'not found travflex location data' in resp.content.decode('utf-8'):
                has_tf_id_error = True
            continue
        _min_price_room = list(res["data"]["categorized"].values())[0][0]
        supplier_rooms = find_each_min_supplier(res["data"]["categorized"])
        _min_price = (
            float(_min_price_room.get("total_price", 9999999))
            / min_booking_days
        )
        _min_supplier = _min_price_room.get("identity", {}).get(
            "provider", "Unknown"
        )
        if _min_price < min_price:
            min_price = _min_price
        _city_rate = hub['meta_cities'].find_one({"_id": hotel['city']}, {'tax_rate': '1'})
        if not _city_rate:
            city_rate = 0.05
        else:
            city_rate = float(_city_rate.get('tax_rate', 0.05))
        without_tax_price = math.ceil(_min_price * (1-city_rate))

        # 按百（向上取整）计算众数
        if _min_price < 100:
            _mode_price = 100
        else:
            _mode_price = int(f"{str(int(_min_price))[:-2]}00") + 100
        if _mode_price not in mode_price_count:
            mode_price_count[_mode_price] = 0
        mode_price_count[_mode_price] += 1
        if mode_price_count[_mode_price] > mode_price_num:
            mode_price_num = mode_price_count[_mode_price]
            mode_price = _mode_price

        prices.append(
            {
                "checkin": checkin.strftime("%Y-%m-%d"),
                "checkout": checkout.strftime("%Y-%m-%d"),
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
        )
        sum_price += _min_price
        has_price_day += 1
    logger.info(f"{hotel['_id']} get {days} price use {(datetime.now() - req_time).seconds} seconds")
    print((f"{hotel['_id']} get {days} price use {(datetime.now() - req_time).seconds} seconds"))
    if not has_price_day:
        logger.warning(f'{hotel["id"]} without price in {days}days')
    else:
        avg_price = sum_price / has_price_day
        thred = min(avg_price, min_price + avg_price * 0.2)
        for _price in prices:
            if isinstance(_price["price"], float) and _price["price"] < thred:
                _price["special"] = True
    rem_time = datetime.now()
    prices = remove_prices(hotel["id"], prices, avg_price, mode_price, do_bug_price)
    logger.info(f"{hotel['_id']} remove_prices use {(datetime.now() - rem_time).seconds} seconds")
    print((f"{hotel['_id']}remove_prices use {(datetime.now() - rem_time).seconds} seconds"))
    datas = {"hotel_id": hotel["id"], "prices": prices, "selecting": False}
    try:
        scripture["statics.hotels.prices"].update_one(
            {"hotel_id": hotel["id"]},
            {
                "$set": datas,
                "$setOnInsert": {"created_at": datetime.now()},
                "$currentDate": {"updated_at": True},
            },
            upsert=True,
        )
        logger.debug("update succeed")
        if has_tf_id_error:
            scripture['taskmsg.availability'].update_one(
                    {'hotel_id': hotel['id'], 'type': 'travflex_id_error'},
                    {
                        '$set': {
                            'hotel_id': hotel['id'], 
                            'type': 'travflex_id_error'
                            },
                        "$setOnInsert": {"created_at": datetime.now()},
                        "$currentDate": {"updated_at": True},
                    },
                    upsert=True
                )
    except Exception as exc:
        logger.error("update error!", exc_info=exc)
        return f'{hotel["id"]} save calendar failed'
    return f'{hotel["id"]} save calendar succeed'


def remove_prices(hotel_id, new_prices, avg_price=None, mode_price=None, do_bug_price=False):
    # 避免可能由于时区导致的问题，预留一天历史数据
    calculate = []
    if avg_price:
        calculate.append(avg_price/2)
    if mode_price:
        calculate.append(mode_price/2)
    logger.info(f"calculate: {calculate} of {hotel_id} and do_bug_price is : {do_bug_price}")
    base_day = (datetime.now() + timedelta(days=-1)).strftime("%Y-%m-%d")
    base_day = datetime.strptime(base_day, "%Y-%m-%d")
    old_prices = scripture["statics.hotels.prices"].find_one({"hotel_id": hotel_id})
    if not old_prices:
        return new_prices
    prices_dict = {}
    for price in old_prices["prices"]:
        checkin_time = datetime.strptime(price["checkin"], "%Y-%m-%d")
        if checkin_time <= base_day:
            continue
        prices_dict[price["checkin"]] = price

    for price in new_prices:
        checkin_time = datetime.strptime(price["checkin"], "%Y-%m-%d")
        if checkin_time <= base_day:
            continue
        # 功能初期需要对没报价的日期计算虚假报价，标记为`is_calculate`
        if price.get("is_calculate"):
            continue
        if price["checkin"] in prices_dict and 'bug_price_thre' in prices_dict[price["checkin"]]:
            price['bug_price_thre'] = prices_dict[price["checkin"]]['bug_price_thre']
            price['bug_price_type'] = prices_dict[price["checkin"]]['bug_price_type']
        prices_dict[price["checkin"]] = price
        
    result = list(prices_dict.values())
    if do_bug_price and calculate:
        for price in result:
            price.pop('bug_price_type', '')
            price.pop('bug_thre_price', '')
            if not isinstance(price['price'], (str, bool)) and (price['price'] <= max(calculate) or price['price'] <= 500):
                price['bug_price_type'] = 1
                price['bug_thre_price'] = max(calculate) * 1.2
                logger.info(f"{hotel_id}, {price['checkin']} is bug_price, thre: {price['bug_thre_price']}")
                check_bug_price.apply_async((hotel_id, price['checkin'], True), countdown=delay_time)
    return result
