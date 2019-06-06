# coding: utf-8
import logging
from datetime import datetime, timedelta
import requests
from bson import ObjectId
from tasks.utils.database import databases
from web import settings
import time, random

quotes_api = settings.QUOTES_API
logger = logging.getLogger("celery.task")
    
scripture = databases('scripture')
hub = databases('hub')

def save_preparation_data(hotel, start_time=None, end_time=None, max_days=None, min_booking_days=1):
    '''
    hotel : {
        'id': 唯一标识,若为单一供应商 id::provider_id; 若多家供应商且未上cms,则 id1::provider_id1;id2::provider_id2,
        'hotels': [
            {
                'quoter': str() or ObjectId,
                'hotel_id': str
            },
            ...
        ]
    }
    '''
    if not start_time:
        checkin = datetime.now() + timedelta(days=-1)
    else:
        checkin = datetime.strptime(start_time, "%Y-%m-%d")
    if end_time:
        days = (datetime.strptime(end_time, "%Y-%m-%d") - checkin).days
    elif max_days:
        days = max_days
    else:
        days = 130
    try:
        min_booking_days = int(min_booking_days)
    except Exception:
        min_booking_days = 1
        logger.error(f"invalid min_booking_days: {min_booking_days} of {hotel['id']}")
    checkout = checkin + timedelta(days=min_booking_days)
    prices = []
    for i in range(days):
        checkin = checkin + timedelta(days=1)
        checkout = checkout + timedelta(days=1)
        payload = dict(
            checkin=checkin.strftime("%Y-%m-%d"),
            checkout=checkout.strftime("%Y-%m-%d"),
            roomfilters=[{"adults": 2}],
            quoters=[
                {"quoter": value["quoter"], "hotel_id": value["hotel_id"]}
                for value in hotel['hotels']
                if value["hotel_id"].strip() != ""
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
                    "price": "当日无报价",
                    "updated_at": datetime.now(),
                }
            )
            continue
        if not res or res["status"] != 200:
            logger.warning(f"{checkin} {hotel['_id']} get price faild!")
            prices.append(
                {
                    "checkin": checkin.strftime("%Y-%m-%d"),
                    "checkout": checkout.strftime("%Y-%m-%d"),
                    "price": "当日无报价",
                    "updated_at": datetime.now(),
                }
            )
            continue
        if not res["data"].get("categorized"):
            prices.append(
                {
                    "checkin": checkin.strftime("%Y-%m-%d"),
                    "checkout": checkout.strftime("%Y-%m-%d"),
                    "price": "当日无报价",
                    "updated_at": datetime.now(),
                }
            )
            continue
        _min_price_room = list(res["data"]["categorized"].values())[0][0]
        _min_price = (
            float(_min_price_room.get("total_price", 9999999))
            / min_booking_days
        )
        code_2nd = _min_price_room['code']
        code_outer = res['data']['code']
        time.sleep(random.randint(1,3))
        resp_preparation = requests.post(
            f"{quotes_api.replace('availability', 'preparation')}/{code_outer}/{code_2nd}",
            headers={'x-query-from': 'robot'}
        )
        if resp_preparation.json()['status'] == 200:
            prices.append(
                {
                    "checkin": checkin.strftime("%Y-%m-%d"),
                    "checkout": checkout.strftime("%Y-%m-%d"),
                    "price": float(resp_preparation.json()['data']['total_pay_cny']) - _min_price,
                    "updated_at": datetime.now(),
                }
            )
        else:
            prices.append(
                {
                    "checkin": checkin.strftime("%Y-%m-%d"),
                    "checkout": checkout.strftime("%Y-%m-%d"),
                    "price": "preparation失败",
                    "updated_at": datetime.now(),
                }
            )
    datas = {"hotel_id": hotel["id"], "prices": prices, "selecting": False}
    try:
        scripture["statics.preparation.statistics"].update_one(
            {"hotel_id": hotel["id"]},
            {
                "$set": datas,
                "$setOnInsert": {"created_at": datetime.now()},
                "$currentDate": {"updated_at": True},
            },
            upsert=True,
        )
        logger.debug("update succeed")
    except Exception as exc:
        logger.error("update error!", exc_info=exc)
        return f'{hotel["id"]} save preparation failed'
    return f'{hotel["id"]} save preparation succeed'