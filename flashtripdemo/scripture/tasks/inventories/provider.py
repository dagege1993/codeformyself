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

from web import settings

quotes_api = settings.QUOTES_API
calendar_days = 90
logger = logging.getLogger(__name__)


def save_prices(
    hotel_id,
    quoter_id,
    start_time=None,
    end_time=None,
    days=None
):
    scripture = databases("scripture")
    quoter = settings.SUPPLIER_ID_2_NAME[quoter_id]
    if not start_time:
        checkin = datetime.now() + timedelta(days=-1)
    else:
        checkin = datetime.strptime(start_time, "%Y-%m-%d") + timedelta(
            days=-1
        )
    if end_time:
        days = (datetime.strptime(end_time, "%Y-%m-%d") - checkin).days
    elif days:
        pass
    else:
        days = calendar_days
    checkout = checkin + timedelta(days=1)
    prices = []
    sum_price = 0
    min_price = 9999999999999.0
    has_price_day = 0
    pre_no_price = 0
    for i in range(days):
        if i == 30 and pre_no_price == 30:
            scripture["statics.provider.prices"].update_one(
                {"hotel_id": hotel_id, "quoter_id": quoter_id},
                {"$set": {"without_price": True}},
                upsert=True,
            )
            return f"{hotel_id} of {quoter} without price in pre-30-days"
        checkin = checkin + timedelta(days=1)
        checkout = checkout + timedelta(days=1)
        payload = dict(
            checkin=checkin.strftime("%Y-%m-%d"),
            checkout=checkout.strftime("%Y-%m-%d"),
            roomfilters=[{"adults": 2}],
            quoters=[{"quoter": quoter_id, "hotel_id": hotel_id}],
        )
        try:
            resp = requests.post(
                quotes_api, headers={"x-query-from": "robot"}, json=payload
            )
            res = resp.json()
        except Exception as exc:
            logger.error(
                f"{checkin} {hotel_id} get price faild!\ndetail : {resp.content}",
                exc_info=exc,
            )
            prices.append(
                {
                    "checkin": checkin.strftime("%Y-%m-%d"),
                    "checkout": checkout.strftime("%Y-%m-%d"),
                    "price": False,
                }
            )
            pre_no_price += 1
            continue
        if not res or res["status"] != 200 or not res.get('data'):
            logger.warning(f"{checkin} {hotel_id} get price faild!")
            prices.append(
                {
                    "checkin": checkin.strftime("%Y-%m-%d"),
                    "checkout": checkout.strftime("%Y-%m-%d"),
                    "price": False,
                }
            )
            pre_no_price += 1
            continue
        if not res["data"].get("categorized"):
            if quoter != "relux":
                prices.append(
                    {
                        "checkin": checkin.strftime("%Y-%m-%d"),
                        "checkout": checkout.strftime("%Y-%m-%d"),
                        "price": False,
                    }
                )
                pre_no_price += 1
                continue
            else:
                relux_msg = fix_relux_price(res)
                if not relux_msg:
                    continue
                prices.append(
                    {
                        "checkin": checkin.strftime("%Y-%m-%d"),
                        "checkout": checkout.strftime("%Y-%m-%d"),
                        "price": relux_msg["price"],
                        "ori_price": relux_msg["ori_price"],
                        "supplier": "relux",
                        "room_type_en": relux_msg["room_type_en"],
                        "room_type_cn": relux_msg["room_type_cn"],
                        "updated_at": str(datetime.now()),
                    }
                )
                sum_price += relux_msg["price"]
                has_price_day += 1
                continue
        _min_price_room = list(res["data"]["categorized"].values())[0][0]
        _min_price = float(_min_price_room.get("total_price", 9999999))
        _min_supplier = _min_price_room.get("identity", {}).get(
            "provider", "Unknown"
        )
        if _min_price < min_price:
            min_price = _min_price
        prices.append(
            {
                "checkin": checkin.strftime("%Y-%m-%d"),
                "checkout": checkout.strftime("%Y-%m-%d"),
                "price": _min_price,
                "ori_price": float(
                    _min_price_room.get("ori_total_price_cny", 9999999999999)
                ),
                "supplier": _min_supplier,
                "room_type_en": _min_price_room.get("room_type", ""),
                "room_type_cn": _min_price_room.get("translation", ""),
                "updated_at": str(datetime.now()),
            }
        )
        sum_price += _min_price
        has_price_day += 1
    if not has_price_day:
        logger.warning(f"{hotel_id} without price in {days}days")
        return
    avg_price = sum_price / has_price_day
    thred = min(avg_price, min_price + avg_price * 0.2)
    for _price in prices:
        if _price["price"] <= thred:
            _price["special"] = True
    prices = remove_prices(hotel_id, quoter_id, prices, scripture)
    datas = {
        "hotel_id": hotel_id,
        "quoter_id": quoter_id,
        "prices": prices,
        "without_price": False,
    }
    try:
        scripture["statics.provider.prices"].update_one(
            {"hotel_id": hotel_id, "quoter_id": quoter_id},
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
        return f"{hotel_id} save prices failed"
    return f"{hotel_id} save prices succeed"


def remove_prices(hotel_id, quoter_id, new_prices, db):
    # 避免可能由于时区导致的问题，预留一天历史数据
    base_day = (datetime.now() + timedelta(days=-1)).strftime("%Y-%m-%d")
    base_day = datetime.strptime(base_day, "%Y-%m-%d")
    old_prices = db["statics.provider.prices"].find_one(
        {"hotel_id": hotel_id, "quoter_id": quoter_id, "without_price": False}
    )
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
        # 不使用计算数据覆盖真实数据
        if not price.get("price"):
            continue
        prices_dict[price["checkin"]] = price
    return list(prices_dict.values())


def fix_relux_price(resp):
    if isinstance(resp, str):
        return False
    try:
        ori_relux_rooms = (
            resp.get("errors", [{}])[0]
            .get("response", {})
            .get("content", {})
            .get("rooms")
        )
    except Exception:
        return False
    if not ori_relux_rooms:
        return False
    min_price = None
    ori_price = None
    room_type_en = None
    room_type_cn = None
    for ids in ori_relux_rooms:
        for _price in ids["plans"]:
            price = float(_price["price"]["summary"].get("2")) / 15.9485
            if not price:
                continue
            if not min_price or price < min_price:
                min_price = price * 1.05
                ori_price = price
                room_type_cn = ""
                room_type_en = ""
    if not min_price:
        return {
            "price": "当日无报价",
            "ori_price": "当日无报价",
            "room_type_en": "Unknown",
            "room_type_cn": "Unknown",
        }
    return {
        "price": math.ceil(min_price),
        "ori_price": math.ceil(ori_price),
        "room_type_en": room_type_en,
        "room_type_cn": room_type_cn,
    }


def provider_booking(
    provider, start_time, days, hotel_id=None, hotel_name=None, bk_url=None
):
    if not bk_url:
        hotel_path = get_booking_url(provider, hotel_id, hotel_name)
    else:
        hotel_path = str(URL(bk_url).path)
    get_compare_prices(
        f"http://www.booking.com{hotel_path}",
        f"{hotel_id or hotel_name}::{provider}",
        start_time,
        days,
    )
    return True


def get_booking_url(provider, hotel_id=None, hotel_name=None):
    if provider == "cms":
        hub = databases("hub")
        data = hub["poi_items"].find_one(
            {"_id": ObjectId(hotel_id), "crawl_info.crawl_website": "bk_url"},
            {"crawl_info.$": "1"},
        )
        if data and data.get("crawl_info"):
            return str(URL(data["crawl_info"][0]["crawl_url"]).path)
    if not hotel_name:
        hotel_name = find_hotel_name(provider, hotel_id)
        if not hotel_name:
            logger.info(f"not find hotel_name with {provider}, {hotel_id}")
            return False
    query_url = (
        f"https://www.booking.com/searchresults.zh-cn.html?ss={hotel_name}"
    )
    resp = requests.get(
        query_url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
        },
    )
    if resp.status_code != 200:
        # logger.error(f'hotel: {hotel_id}, {hotel_name} get url failed.')
        return False
    et = etree.HTML(resp.content.decode("utf-8"))
    try:
        hotel_path = (
            et.xpath('//a[@class="hotel_name_link url"]/@href')[0]
            .strip()
            .split("?")[0]
        )
        return hotel_path
    except Exception as exc:
        logger.error(
            f"hotel: {hotel_id}, {hotel_name} get url in {query_url} failed.",
            exc_info=exc,
        )
        return False


def compair_ctrip(provider, start_time, days, hotel_id=None, hotel_name=None):
    if not hotel_name:
        hotel_name = find_hotel_name(provider, hotel_id)
        if not hotel_name:
            return False
    resp = requests.get(
        f"http://m.ctrip.com/restapi/h5api/searchapp/search?action=autocomplete&source=globalonline&keyword={hotel_name}"
    )
    if not resp or resp.status_code != 200 or not resp.json()["data"]:
        return False
    hid = resp.json()["data"][0]["url"].split("/")[-1]
    get_compare_prices(
        f"http://m.ctrip.com/webapp/hotel/j/hoteldetail/dianping/rooms/{hid}",
        f"{hotel_id or hotel_name}::{provider}",
        start_time,
        days,
        spider_name="ctrip_prices",
    )


def find_hotel_name(provider, hotel_id):
    if provider == "cms":
        hub = databases("hub")
        data = hub["poi_items"].find_one(
            {"_id": ObjectId(hotel_id)}, {"name_en": "1", "city": "1"}
        )
        if not data:
            logger.info(f"invalid cms_id : {hotel_id}")
            return False
        city = hub["meta_cities"].find_one(
            {"_id": data.get("city", "")}, {"name_en": "1"}
        )
        if not city or not city.get("name_en", ""):
            logger.info(
                f"invalid city_id of hotel: {hotel_id}, {data.get('city')}"
            )
            city_name = ""
        else:
            city_name = city["name_en"]
        return f"{data.get('name_en')} {city_name}"
    quoter_coll = settings.SUPPLIER_ID_2_COLL.get(
        provider
    ) or settings.SUPPLIER_NAME_2_COLL.get(provider)
    if not quoter_coll:
        return False
    if quoter_coll == "wg_hotel":
        db = databases("whotel")
    else:
        db = databases("scripture")
    condition = {"$or": []}
    try:
        int_hid = int(hotel_id)
        condition["$or"].append({"hotel_id": int_hid})
    except Exception:
        pass
    try:
        str_hid = str(hotel_id)
        condition["$or"].append({"code": str_hid})
        condition["$or"].append({"hotel_id": str_hid})
    except Exception:
        pass
    hotel_msg = db[quoter_coll].find_one(condition, {"name": "1", "province": "1"})
    if not hotel_msg:
        return False
    hotel_name = (
        f"{hotel_msg['name'].replace('&', ' ')} {hotel_msg.get('city', {'name': ''})['name'] or hotel_msg.get('province', '')}"
    )
    return hotel_name
