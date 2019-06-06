# coding: utf8

# Standard Library
import logging
import requests
from datetime import datetime, timedelta
from tasks.utils.database import databases
from web import settings
from bson import ObjectId

hub = databases('hub')
scripture = databases('scripture')
quotes_api = settings.QUOTES_API

one_day = timedelta(days=1)


def skyscanner_prices(checkin, checkout, sid):
    checkin = checkin.strftime("%Y-%m-%d")
    checkout = checkout.strftime("%Y-%m-%d")
    res = None
    params = {
        "checkin": checkin,
        "checkout": checkout,
        "rooms": 1,
        "adults": 2,
        "market": "CN",
        "locale": "zh-CN",
        "currency": "CNY",
    }
    result_dict = {'checkin': checkin}
    for j in range(5):
        try:
            res = req(sid, params)
        except:
            logging.debug(f"sid : {sid} not find price in {j+1} request")
        if res and res.get("offers"):
            logging.info(f"find price in {j} times retry!")
            break

    if not res or not res.get("offers"):
        logging.info(f"not find offer! : {sid}")
        return {'skyscanner_price': '当日无报价',
                'ct_price': '当日无报价',
                'checkin': checkin,
                "updated_at": datetime.now()}

    for offer in res["offers"]:
        pid = offer["partner_id"]
        pprice = float(offer["price"])
        if pid == "h_ct":
            result_dict["ct_price"] = pprice
            result_dict["ct_room"] = offer["room_type"][0]
            continue

        if "skyscanner_price" not in result_dict:
            result_dict["skyscanner_price"] = pprice
            result_dict["skyscanner_room"] = offer["room_type"][0]
        if pprice < result_dict["skyscanner_price"]:
            result_dict["skyscanner_price"] = pprice
            result_dict["skyscanner_room"] = offer["room_type"][0]
    result_dict["updated_at"] = datetime.now()

    return result_dict


def crawl_one(base_day, days, sid, hotel_id=None, hotel_name=None):
    try:
        base_day = datetime.strptime(base_day, '%Y-%m-%d')
    except Exception:
        logging.warning(f"invalid base_day of skyscanner! : {base_day}")
        return
    new_prices = {}
    for i in range(days):
        checkin = base_day + one_day
        checkout = base_day + one_day * 2
        base_day = base_day + one_day
        new_prices[checkin.strftime(
            '%Y-%m-%d')] = skyscanner_prices(checkin, checkout, sid)

    prices = formart_skyscanner_prices(new_prices, sid)
    payload = {'prices': prices}
    if hotel_id:
        payload['hotel_id'] = hotel_id
    if hotel_name:
        payload['hotel_name'] = hotel_name
    resp = scripture['statics.skyscanner.prices'].update_one(
        {'sid': sid},
        {
            '$set': payload,
            '$setOnInsert': {'created_at': datetime.now()},
            "$currentDate": {'updated_at': True},
        },
        upsert=True,
    )
    logging.debug(f'{resp.raw_result}')


def req(sid, params):
    resp = requests.get(
        f"http://172.16.1.221/api/v2/skyscanner/hotel/{sid}", params=params)
    res = resp.json()
    return res["hotel"]


def formart_skyscanner_prices(new_prices, sid):
    old_prices = scripture['statics.skyscanner.prices'].find_one({"sid": sid})
    base_day = (datetime.now() + timedelta(days=-1)).strftime('%Y-%m-%d')
    base_day = datetime.strptime(base_day, '%Y-%m-%d')
    if not old_prices:
        return new_prices
    prices_dict = {}
    if isinstance(old_prices['prices'], dict):
        for _, price in old_prices['prices'].items():
            if isinstance(price, str):
                prices_dict[_] = {}
                continue
            date = price.get('checkin') or _
            checkin_time = datetime.strptime(date, '%Y-%m-%d')
            if checkin_time <= base_day:
                continue
            prices_dict[date] = price
    else:
        for price in old_prices['prices']:
            checkin_time = datetime.strptime(price['checkin'], '%Y-%m-%d')
            if checkin_time <= base_day:
                continue
            prices_dict[price['checkin']] = price

    if isinstance(new_prices, dict):
        for _, price in new_prices.items():
            date = price.get('checkin') or _
            checkin_time = datetime.strptime(date, '%Y-%m-%d')
            if checkin_time <= base_day:
                continue
            prices_dict[date] = price
    else:
        for price in old_prices['prices']:
            checkin_time = datetime.strptime(price['checkin'], '%Y-%m-%d')
            if checkin_time <= base_day:
                continue
            prices_dict[price['checkin']] = price

    return list(prices_dict.values())
