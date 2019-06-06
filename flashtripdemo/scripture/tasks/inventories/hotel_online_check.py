# coding: utf8

# Standard Library
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

import requests
from tasks.utils.database import databases

from web import settings

executer = ThreadPoolExecutor(max_workers=4)
max_missed = 7
quotes_url = settings.QUOTES_API
headers = {"x-request-from": "order"}


def hotel_check():
    hub = databases("hub")
    scripture = databases("scripture")
    scripture["hotel.online.check"].update_one(
        {"__t": "flag"}, {"$set": {"refreshing": True}}, upsert=True
    )
    base_day = datetime.now()
    onlines = []
    for online in hub["poi_items"].find(
        {
            "__t": "Hotel",
            "edit_status": {"$in": ["edited", "audited"]},
            "publish_status": "online",
        },
        {
            "_id": "1",
            "quote_ids": "1",
            "name": "1",
            "name_en": "1", 
            'address': '1', 
            'en.address': '1'
        },
    ):
        onlines.append((online, base_day))
    for available in executer.map(check_price, onlines):
        if available:
            available["updated_at"] = datetime.now()
            scripture["hotel.online.check"].update_one(
                {"hotel_id": available["_id"]},
                {"$set": available},
                upsert=True,
            )
    scripture["hotel.online.check"].update_one(
        {"__t": "flag"}, {"$set": {"refreshing": False}}, upsert=True
    )


def check_price(hotel_base_day):
    res = None
    hotel = hotel_base_day[0]
    base_day = hotel_base_day[1]
    if not hotel.get("quote_ids"):
        return False
    quoter = []
    need_slow_down = False
    for _quoter in hotel['quote_ids']:
        if _quoter['hotel_id'].strip() == "":
            continue
        if str(_quoter['quoter']) == "59c1f0f8e1812033000e1de8":
            need_slow_down = True
        if str(_quoter['quoter']) == settings.SUPPLIER_NAME_2_ID['hotelspro']:
            continue
        quoter.append({"quoter": str(_quoter["quoter"]), "hotel_id": _quoter["hotel_id"]})
    days = [
        (base_day + timedelta(days=7), base_day + timedelta(days=8)),
        (base_day + timedelta(days=7), base_day + timedelta(days=9)),
        (base_day + timedelta(days=7), base_day + timedelta(days=10)),
        (base_day + timedelta(days=30), base_day + timedelta(days=31)),
        (base_day + timedelta(days=30), base_day + timedelta(days=32)),
        (base_day + timedelta(days=30), base_day + timedelta(days=33)),
        (base_day + timedelta(days=60), base_day + timedelta(days=61)),
        (base_day + timedelta(days=60), base_day + timedelta(days=62)),
        (base_day + timedelta(days=60), base_day + timedelta(days=63)),
    ]
    missed = 0
    for _index, day in enumerate(days):
        index = _index + 1
        payload = dict(
            checkin=day[0].strftime("%Y-%m-%d"),
            checkout=day[1].strftime("%Y-%m-%d"),
            roomfilters=[{"adults": 2}],
            quoters=quoter,
        )
        try:
            res = requests.post(
                quotes_url, headers=headers, json=payload
            ).json()
            if need_slow_down:
                time.sleep(6)
        except Exception as exc:
            logging.warning(f"quotes api error", exc_info=exc)
            missed += 1
        if not res or not res["data"]["categorized"]:
            missed += 1
        if missed >= max_missed:
            return False
        elif 9 - index < max_missed - missed:
            return hotel
    if missed <= max_missed:
        return hotel
    else:
        return False
