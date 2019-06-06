# coding: utf8
"""Crawled urls
"""

# Standard Library
import math
import aiohttp
import logging
from datetime import datetime, timedelta
from web.utils.database import databases
from web import settings
from random import choices

# Current Project
from . import api_v1
from .formatter_response import rest_result
from tasks.inventories import (
    calendar_one,
    calendar_all,
    bug_price_one,
    bug_price_all,
)
from tasks.supplier_statics import update_relux_rooms

alpha_set = 'abcdefghijklmn'


@api_v1.route("/hotels/calendar", methods=["OPTIONS"])
async def pre_process_options(request):
    return rest_result(request, {"status": 200})


@api_v1.route("/hotels/calendar", methods=["POST"])
async def get_price_calendar(request):
    logger = logging.getLogger(__name__)
    body = request.json
    hotel_id = body.get("hotel_id", "")
    start_time = body.get("start_time")
    end_time = body.get("end_time")
    uid = ''.join(choices(alpha_set, k=24))
    logger.info(f"uid: {uid}.get {hotel_id} calendar with start_time: {start_time}, end_time: {end_time}")
    if not hotel_id:
        logger.warning("hotel_id cannot be None")
        return rest_result(
            request, {"status": 400, "errmsg": "invalid hotel_id"}
        )

    db = databases("scripture")
    hotel = await db["statics.hotels.prices"].find_one({"hotel_id": hotel_id})

    if not hotel:
        logger.info(f"hotel_id:{hotel_id} corresponding no hotel ")
        return rest_result(request, {"status": 200, "data": []})
    # type == 1 当日有价格；type == 0 当日无报价；type == -1 当日价格无效
    if not end_time:
        base_day = datetime.now()
        days = await get_calendar_days()
    else:
        base_day = datetime.strptime(start_time, "%Y-%m-%d")
        days = (datetime.strptime(end_time, "%Y-%m-%d") - base_day).days
    date = [
        (base_day + timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range(int(days))
    ]
    prices = {}
    for day in hotel["prices"]:
        if day["checkin"] not in date:
            continue
        price = day.get("without_tax_price") or day["price"]
        if isinstance(price, str):
            flag = 0
            price = "已抢光"
            special = False
        elif isinstance(price, int) or isinstance(price, float):
            flag = 1
            special = day.get("special", False)
            price = math.ceil(price)
        else:
            flag = -1
            special = False
        prices[day["checkin"]] = {
            "price": price,
            "type": flag,
            "checkin": day["checkin"],
            "checkout": day["checkout"],
            "special": special,
        }
        if "bug_price_type" in day:
            prices[day["checkin"]]["bug_price_type"] = day["bug_price_type"]

    for checkin in date:
        if checkin not in prices:
            prices[checkin] = {
                "price": "",
                "type": -1,
                "checkin": checkin,
                "special": False,
            }
    prices = list(prices.values())
    if hotel.get("selecting"):
        logger.info(f"{uid}_hotel_id:{hotel_id} Refreshing")
        return rest_result(
            request, {"status": 200, "data": prices, "msg": "Refreshing..."}
        )
    else:
        logger.info(f"{uid}_hotel_id:{hotel_id} get price succeed")
        return rest_result(request, {"status": 200, "data": prices})


@api_v1.route("/hotels/calendar/refresh", methods=["POST"])
async def refresh_price_calendar(request):
    logger = logging.getLogger(__name__)
    body = request.json
    if not body:
        logger.warning("request has not body")
        return rest_result(
            request, {"status": 400, "errmsg": "body is empty!"}
        )
    hotel_id = body.get("hotel_id", "")
    if not hotel_id:
        logger.warning("hotel_id cannot be None")
        return rest_result(
            request, {"status": 400, "errmsg": "hotel_id cannot be None"}
        )
    db = databases("scripture")
    status = await db["statics.hotels.prices"].find_one(
        {"hotel_id": hotel_id}, {"selecting", "updated_at"}
    )
    if (
        status
        and status.get("selecting")
        and status.get("updated_at", datetime.now() + timedelta(days=-1))
        < datetime.now() + timedelta(days=-1)
    ):
        logger.info(f"hotel_id:{hotel_id},Refreshing")
        return rest_result(request, {"status": 200, "data": "Refreshing..."})
    if body.get("bug_price", False):
        if body.get("days"):
            bug_price_one.delay(hotel_id, int(body["days"]))
        else:
            bug_price_one.delay(hotel_id)
        logger.info(f"bug price publish")
    else:
        calendar_one.delay(hotel_id)
    await db["statics.hotels.prices"].update_one(
        {"hotel_id": hotel_id}, {"$set": {"selecting": True}}
    )
    logger.info(f"hotel_id:{hotel_id}, publish task succeed")
    return rest_result(request, {"status": 200, "data": "succeed"})


@api_v1.post("/hotels/calendar/refresh/all")
async def refresh_calendar_all(request):
    logger = logging.getLogger(__name__)
    logger.info(f"{request.json.get('user', 'Unknown')} refresh all calendar")
    calendar_all.delay()
    return rest_result(request, {"status": 200, "data": "ok"})


async def get_calendar_days():
    logger = logging.getLogger(__name__)
    async with aiohttp.ClientSession() as sess:
        async with sess.get(
            f"{settings.CMS_API}/api/internal/configs/hotel",
            params={"configs": "price_calendar_display_day_span"},
            headers={"accept-version": "6.0.0"},
        ) as resp:
            if resp.status == 200:
                resp = await resp.json()
            else:
                logger.error(f"get calendar days from hub fail!")
                return 130
    return resp["data"].get("price_calendar_display_day_span", 130)


@api_v1.post("/hotels/bugprice")
async def get_bug_price(request):
    """
    仅读取超低价数据，计算日期范围内的均价、众数、最大值
    """
    logger = logging.getLogger(__name__)
    body = request.json
    cms_ids = body.get("cms_ids", [])
    start_time = body.get("start_time", datetime.now().strftime("%Y-%m-%d"))
    num = body.get("num", 1)
    try:
        start_time = datetime.strptime(start_time, "%Y-%m-%d")
    except:
        logger.error(f"invalid start_time: {body['start_time']}")
        return rest_result(
            request,
            {
                "status": 400,
                "errmsg": f"invalid start_time: {body['start_time']} should be YYYY-mm-dd",
            },
        )
    end_time = body.get("end_time", "")
    if not end_time:
        days = await get_calendar_days()
        end_time = start_time + timedelta(days=days)
    else:
        try:
            end_time = datetime.strptime(end_time, "%Y-%m-%d")
        except:
            logger.error(f"invalid end_time: {body['end_time']}")
            return rest_result(
                request,
                {
                    "status": 400,
                    "errmsg": f"invalid end_time: {body['end_time']} should be YYYY-mm-dd",
                },
            )
    show_detail = body.get("show_detail", False)
    result = {}
    db = databases("scripture")
    for cid in cms_ids:
        result[cid] = {}
        data = await db["statics.hotels.prices"].find_one({"hotel_id": cid})
        cid_result = {}
        max_price = 0
        mode_price_num = 0
        mode_price = 0
        price_result = []
        for price in data.get("prices", []):
            if (
                not price
                or isinstance(price.get("price", ""), (str, bool))
                or start_time > datetime.strptime(price["checkin"], "%Y-%m-%d")
                or end_time < datetime.strptime(price["checkin"], "%Y-%m-%d")
            ):
                continue
            # 最低价且离当前日期最近的一天
            if price.get("bug_price_type") and (
                "price" not in result[cid]
                or result[cid]["price"]['price'] > price["price"]
            ):
                result[cid]["price"] = {
                    "checkin": price["checkin"],
                    "price": price["price"],
                }
            _mode_price = int(f"{str(int(price['price']))[:-2]}00") + 100
            checkin = price["checkin"]
            if _mode_price not in cid_result:
                cid_result[_mode_price] = 0
            cid_result[_mode_price] += 1
            if cid_result[_mode_price] > mode_price_num:
                mode_price_num = cid_result[_mode_price]
                mode_price = _mode_price
            if price["price"] > max_price:
                max_price = price["price"]
            price_result.append(price["price"])
        if show_detail:
            if len(price_result):
                avg_price = math.ceil(sum(price_result) / len(price_result))
            else:
                avg_price = "无有效报价！"
            result[cid]["max_price"] = max_price
            result[cid]["avg_price"] = avg_price
            result[cid]["mode_prive"] = mode_price
    return rest_result(request, {"status": 200, "data": result})
