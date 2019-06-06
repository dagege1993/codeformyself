# coding: utf-8

import logging
from bson import ObjectId
import requests
from datetime import datetime, timedelta

from . import publish_v1
from .query_transformer import validate_request
from web.utils.database import databases
from web.api.formatter_response import rest_result
from web.utils.add_compair_task import get_booking_prices, _check_prices
from web import settings
from tasks.inventories import (
    calendar_one,
    get_skyscanner,
    get_provider_prices,
    calendar_all,
    provider_compair_booking,
    provider_compair_ctrip,
    check_preparation,
)


logger = logging.getLogger(__name__)


@publish_v1.post("/skyscanner")
async def skyscanner(request):
    valid = await validate_request(request)
    if valid["errmsg"] and not request.json.get("provider"):
        return rest_result(request, {"status": 400, "errmsg": valid["errmsg"]})
    start_time = valid["start_time"]
    days = valid["days"]
    for hotel in valid["hotels"]:
        get_skyscanner.delay(start_time, days, hotel_id=hotel)
    db = databases("scripture")
    for hotel_id, hotel_name in request.json.get("provider", {}).items():
        sid = await db["statics.hotels.skyscanner"].find_one(
            {"name": {"$regex": hotel_name.lower(), "$options": "i"}},
            {"sid": "1"},
        )
        if sid:
            get_skyscanner.delay(
                start_time, days, sid=sid["sid"], hotel_id=hotel_id
            )
    return rest_result(request, {"status": 200, "data": "ok"})


@publish_v1.post("/booking")
async def _booking(request):
    valid = await validate_request(request)
    if valid["errmsg"]:
        return rest_result(request, {"status": 400, "errmsg": valid["errmsg"]})
    cms_ids = valid["hotels"]
    db = databases("hub")
    start_time = valid["start_time"]
    end_time = valid["end_time"]
    days = valid["days"]
    # 避免传入的开始时间早于当前日期导致无效查询
    # TODO: 抽象成单独校验日期的方法
    for index, hid in enumerate(cms_ids):
        booking_url = await db["poi_items"].find_one(
            {"_id": ObjectId(hid), "crawl_info.crawl_website": "bk_url"},
            {"crawl_info.$": "1"},
        )
        if not booking_url:
            continue
        await get_booking_prices(
            booking_url["crawl_info"][0]["crawl_url"], hid, start_time, days
        )
        calendar_one.delay(hid, start_time, end_time)
        if index % 10 == 0:
            _check_prices.apply_async(
                kwargs={
                    "base_url": booking_url["crawl_info"][0]["crawl_url"],
                    "cms_id": hid,
                    "start_time": start_time,
                    "days": days,
                },
                countdown=settings.CHECK_PRICE_DELAY_TIME,
            )
    return rest_result(request, {"status": 200, "data": "ok"})


@publish_v1.post("/weego")
async def _weego(request):
    valid = await validate_request(request)
    logger.info(f"weego params : {valid}")
    for hotel_id in valid.get("hotels", []):
        calendar_one.delay(hotel_id, valid["start_time"], valid["end_time"])
    return rest_result(
        request,
        {"status": 200, "data": valid.get("errmsg") or valid["hotels"]},
    )


@publish_v1.post("/provider")
async def _provider(request):
    """
    hotel from statics providers data
    """
    body = request.json
    if not body:
        return rest_result(
            request, {"status": 400, "errmsg": "request without params!"}
        )
    start_time = body.get("start_time")
    end_time = body.get("end_time")
    days = body.get("days")
    hotel_ids = body.get("hotel_ids", [])
    quoter = body.get("quoter")
    quoters = body.get("quoters", []) or body.get("hotels", [])
    if quoter in settings.SUPPLIER_NAME_2_ID:
        quoter = settings.SUPPLIER_NAME_2_ID[quoter]
    if days and not end_time:
        end_time = (
            datetime.strptime(start_time, "%Y-%m-%d") + timedelta(days=days)
        ).strftime("%Y-%m-%d")
    for hotel_id in hotel_ids:
        get_provider_prices.delay(
            hotel_id=hotel_id,
            quoter_id=quoter,
            start_time=start_time,
            end_time=end_time,
        )
    for hotel in quoters:
        hotel_id = hotel["hotel_id"]
        quoter_id = (
            hotel.get("quoter")
            or settings.SUPPLIER_NAME_2_ID[hotel.get("provider")]
        )
        get_provider_prices.delay(
            hotel_id=hotel_id,
            quoter_id=quoter_id,
            start_time=start_time,
            end_time=end_time,
        )
    return rest_result(request, {"status": 200, "data": "ok"})


@publish_v1.post("/provider/booking")
async def booking_provider(request):
    valid = await validate_request(request)
    provider_compair_booking.delay(
        valid["start_time"], valid["days"], valid["hotels"]
    )
    return rest_result(
        request,
        {"status": 200, "data": valid.get("errmsg") or valid["hotels"]},
    )


@publish_v1.post("/provider/ctrip")
async def ctrip_provider(request):
    valid = await validate_request(request)
    if valid["provider"]:
        hotels = []
        for _hotel in valid["hotels"]:
            if isinstance(_hotel, str):
                _hotel = {"hotel_id": _hotel, "provider": valid["provider"]}
            elif isinstance(_hotel, dict):
                _hotel["provider"] = valid["provider"]
            hotels.append(_hotel)
        valid["hotels"] = hotels
    provider_compair_ctrip.delay(
        valid["start_time"], valid["days"], valid["hotels"]
    )
    return rest_result(
        request,
        {"status": 200, "data": valid.get("errmsg") or list(valid["hotels"])},
    )


@publish_v1.post("/preparation/check")
async def preparation_check(request):
    body = request.json
    check_preparation.delay(body["hotels"])
    return rest_result(request, {"status": 200, "data": "ok"})


@publish_v1.post("/availability")
async def availability(request):
    """
    查价任务统一发布接口\n
    compare中为需要比价的第三方网站\n
    目前支持ctrip 和 booking
    """
    request.headers["Accept"] = "application/json"
    valid = await validate_request(request)
    logger.info(f"valid: {valid}")
    if valid["errmsg"]:
        return rest_result(request, {"status": 400, "errmsg": valid["errmsg"]})
    compare = valid["compare"]
    hotels = valid["hotels"]
    start_time = valid["start_time"]
    days = valid["days"]
    only_compare = valid["only_compare"]

    """
    获取第三方价格放在scrapy中执行，celery仅发布任务
    优先放入celery中执行
    """
    if "ctrip" in compare:
        await ctrip(hotels, start_time, days)
    if "booking" in compare:
        await booking(hotels, start_time, days)
    if not only_compare:
        for uid, _hotels in hotels.items():
            for hotel in uid.split(";"):
                quoter_id, hotel_id = hotel.split("::")
                if quoter_id == "cms":
                    calendar_one.delay(hotel_id, start_time=start_time, end_time=None, days=days)
                else:
                    get_provider_prices.delay(
                        hotel_id=hotel_id,
                        quoter_id=quoter_id,
                        start_time=start_time,
                        hotels=None,
                        days=days,
                    )
    return rest_result(request, {"status": 200, "data": list(hotels.keys())})


async def ctrip(ori_hotels, start_time, days):
    """
    接口需要立即返回，查询ctrip网址的部分放到celery中
    若后续需求变更，可在此方法中获取ctrip_url
    """
    hotels = []
    for uid, _hotels in ori_hotels.items():
        if "::" not in uid:
            hotels.append(uid)
        else:
            for hotel in _hotels:
                hotels.append(
                    {
                        "provider": hotel["quoter"],
                        "hotel_id": hotel["hotel_id"],
                        "hotel_name": hotel.get("hotel_name"),
                    }
                )
    provider_compair_ctrip.delay(start_time, days, hotels)


async def booking(ori_hotels, start_time, days):
    """
    接口需要立即返回，查询booking网址的部分放到celery中
    若后续需求变更，可在此方法中获取bk_url
    """
    hotels = []
    for uid, _hotels in ori_hotels.items():
        if "::" not in uid:
            hotels.append(uid)
        else:
            for hotel in _hotels:
                hotels.append(
                    {
                        "provider": hotel["quoter"],
                        "hotel_id": hotel["hotel_id"],
                        "bk_url": hotel.get("bk_url"),
                        "hotel_name": hotel.get("hotel_name"),
                    }
                )
    provider_compair_booking.delay(start_time, days, hotels)
