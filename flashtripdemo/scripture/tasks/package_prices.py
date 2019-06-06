# coding: utf8


import json
import logging
from datetime import date, datetime, timedelta
from functools import lru_cache

import redis
import requests
from bson import ObjectId
from influxdb import InfluxDBClient
from tasks import settings
from tasks.application import app
from tasks.utils import notifiers
from tasks.utils.database import databases

histories = {}


@app.task
def packages():
    hub = databases("hub")

    packages = hub.sku_packages.find(
        {
            "$and": [
                {"edit_status": {"$in": ["edited", "audited"]}},
                {"publish_status": {"$ne": "offline"}},
                {"has_relevant_hotel": True},
            ]
        },
        {
            "hotels": 1,
            "daily_inventory": 1,
            "air_price": 1,
            "appreciation_fee": 1,
            "inventory_updated_at": 1,
        },
    )

    return (
        package_check.chunks(
            [[json.dumps(pkg, default=on_json_serialize)] for pkg in packages],
            16,
        )
        | on_finished.s()
    ).apply_async()


def on_json_serialize(o):
    if isinstance(o, datetime):
        return o.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(o, date):
        return o.strftime("%Y-%m-%d")
    if isinstance(o, ObjectId):
        return str(o)
    return o


@app.task
def on_finished(t):
    r = redis.StrictRedis.from_url(settings.REDIS, db=3)
    key = f'package-checked-{datetime.now().strftime("%Y-%m-%d")}'
    r.expire(key, 86400)
    alertings = r.lrange(key, 0, -1)
    package_cnt = len(set(each["package"] for each in alertings))
    total = len(alertings)
    content = (
        f"{package_cnt}个套餐有价格问题  \n"
        f"共{total}个日期  \n"
        f"[查看详情](http://scripture.weegotr.com/views/package-prices/{key})"
    )
    message = notifiers.DingtalkMessage(title="套餐价格高于Trip.com", text=content)
    notifiers.DingtalkNotifier().send(message, settings.DINGTALK_NOTIFY[''])


@app.task
def package_check(package):
    logger = logging.getLogger(__name__)
    r = redis.StrictRedis.from_url(settings.REDIS, db=3)
    key = f'package-checked-{datetime.now().strftime("%Y-%m-%d")}'
    package = json.loads(package)
    daily_inventory = package.get("daily_inventory")

    hub = databases("hub")

    influx = InfluxDBClient(host="172.16.2.208", database="quotes")

    if not daily_inventory:
        return
    hotels = package.get("hotels")
    if not hotels:
        return
    updated_at = datetime.strptime(
        package["inventory_updated_at"], "%Y-%m-%d %H:%M:%S"
    )

    sk_hotel_id = None
    # 现在的套餐都是最多一家酒店
    hotel = hotels[0]
    duration = hotel["days"]
    _hotel = hub.poi_items.find_one({"_id": ObjectId(hotel["hotel"])})
    if not _hotel.get("third_ref_ids"):
        logger.critical(
            "Package(%s) - Hotel(%s)", package["name"], _hotel["name"]
        )
        return
    for third_ref in _hotel["third_ref_ids"]:
        if third_ref["name"] == "skyscanner":
            sk_hotel_id = third_ref["value"]
            break
    else:
        raise Exception("hotel id of skyscanner is missing.")

    def daily_check(daily):
        if not all(
            [
                daily.get("code"),
                daily.get("below_average"),
                daily.get("no_newquotes_count") <= 0,
            ]
        ):
            return
        daily_date = datetime.strptime(daily["date"], "%Y-%m-%d %H:%M:%S")
        checkin = daily_date.strftime("%Y-%m-%d")
        checkout = (daily_date + timedelta(days=duration)).strftime("%Y-%m-%d")
        code = daily["code"]
        if code not in histories:
            result = influx.query(sql(updated_at))
            results = {
                item["code"]: item for item in list(result.items()[0][1])
            }
            histories.update(results)

        history = histories.get(code)
        if not history:
            logger.warning(
                "Not found price from history of %s", hotel["hotel"]
            )

        try:
            resp = retry(
                skyscanner_hotel,
                checkin=checkin,
                checkout=checkout,
                hotel_id=sk_hotel_id,
            )
        except Exception as exc:
            logger.info(exc)
            return
        for offer in resp["hotel"]["offers"]:
            if offer["partner"] == "Trip.com":
                trip_price = offer["price"]
                break
        else:
            logger.info("Failed fetch price of trip.com from skyscanner.")
            return
        trip_average_price = trip_price / duration
        threshold = history["price"] * 1.1
        if trip_average_price > threshold:
            logger.info(
                {
                    "package": str(package["_id"]),
                    "checkin": daily["date"],
                    "trip_price": trip_average_price,
                    "history": history,
                }
            )
            r.lpush(
                key,
                json.dumps(
                    {
                        "package": str(package["_id"]),
                        "checkin": checkin,
                        "trip_price": trip_average_price,
                        "price": history["price"],
                        "provider": daily["quote_name"],
                    }
                ),
            )
            return

    for daily in daily_inventory:
        daily_check(daily)
    return


def set_results(f):
    logger = logging.getLogger(__name__)
    exc = f.exception()
    if exc:
        logger.critical(exc)


def retry(func, *args, max_times=2, **kwargs):
    for _ in range(max_times):
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            pass
    raise Exception("Max retry times excced.")


def skyscanner_hotel(checkin, checkout, hotel_id):
    params = {
        "checkin": checkin,
        "checkout": checkout,
        "rooms": 1,
        "adults": 2,
        "market": "CN",
        "locale": "zh-CN",
        "currency": "CNY",
    }
    response = requests.get(
        f"http://172.16.1.221/api/v2/skyscanner/hotel/{hotel_id}",
        params=params,
    )
    assert response.status_code == 200, response.text
    json = response.json()
    assert json["status"] == 200, json
    assert json["hotel"]["offers"], json
    return json


@lru_cache(64)
def sql(updated_at):
    three_hours = timedelta(hours=3)
    time_before = (updated_at - three_hours).strftime("%Y-%m-%dT%H:%M:%SZ")
    time_after = (updated_at + three_hours).strftime("%Y-%m-%dT%H:%M:%SZ")

    return f"""select code, value as price from \
    autogen.reservation_price_histories \
    where is_package='True' and time >= '{time_before}' \
    and time <= '{time_after}'"""


if __name__ == "__main__":
    # print(packages.apply_async())
    print(app.send_task("tasks.package_prices.packages"))
