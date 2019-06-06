# coding: utf-8
import logging
import json
import time
from datetime import datetime, timedelta

import aiohttp
from bson import ObjectId
from yarl import URL

from web import settings
from web.utils import add_compair_task, async_price_compare_check
from web.utils.database import databases

from . import api_v1
from .formatter_response import rest_result

ctrip_maps = {}

logger = logging.getLogger(__name__)

period = settings.COMPARE_TIME_PERIOD


async def send_compair_task(
    cms_id,
    stage,
    price,
    checkin,
    room_type,
    checkout,
    meal_type,
    is_package,
    user_id,
    source,
    cancel_policy, 
    user_ip,
    source_type,
    voucher,
    deal_check_code,
    uid=''
):
    '''
    相同酒店相同查询日期，限定时间内仅查询1次
    '''
    rds_db = databases(settings.REDIS)
    query_key = f"scripture::record::{cms_id}::{checkin}::{checkout}"
    true_query_uid = await rds_db.get(query_key)
    db = databases("hub")
    urls = None
    if not true_query_uid:
        urls = await db["poi_items"].find_one(
            {"_id": ObjectId(cms_id)},
            {"crawl_info": "1", "city": "1", "name_en": "1"},
        )
        if not urls:
            logger.info(f"cms_id: {cms_id} not find!")
            return
        await rds_db.psetex(query_key, period, 'temp')
    if not urls:
        urls = await db["poi_items"].find_one(
            {"_id": ObjectId(cms_id)},
            {"crawl_info": "1", "city": "1", "name_en": "1"},
        )
    compair = {}
    compair["weego_price"] = price
    compair["stage"] = stage
    compair["checkin"] = checkin
    compair["weego_room_type"] = room_type
    compair["checkout"] = checkout
    compair["cms_id"] = cms_id
    compair["meal_type"] = meal_type
    compair["query_time"] = str(datetime.now())
    compair["is_package"] = is_package
    compair["hotel_name"] = urls["name_en"]
    compair["user_id"] = user_id
    compair["cancel_policy"] = cancel_policy
    compair["user_ip"] = user_ip
    compair["source_type"] = source_type
    compair["voucher"] = voucher
    compair["deal_check_code"] = deal_check_code
    compair['uid'] = uid
    days = (
        datetime.strptime(checkout, "%Y-%m-%d")
        - datetime.strptime(checkin, "%Y-%m-%d")
    ).days
    websites = {}
    for website in urls.get("crawl_info", {}):
        if "crawl_website" not in website:
            continue
        if website["crawl_website"] == "bk_url":
            bk_url = str(
                URL(website["crawl_url"]).with_query(
                    {
                        "checkin_year": checkin[:4],
                        "checkin_month": checkin[5:7],
                        "checkin_monthday": checkin[8:],
                        "checkout_year": checkout[:4],
                        "checkout_month": checkout[5:7],
                        "checkout_monthday": checkout[8:],
                    }
                )
            )
            websites["booking"] = bk_url
        elif website["crawl_website"] == "ctrip_url":
            ctrip_url = str(
                URL().with_query(
                    {
                        'inday': checkin.replace('-', '/'),
                        'outday': checkout.replace('-', '/'),
                        'subchannel': '',
                        'hotelchannel': '1',
                        'isoversea': '1'
                    }
                )
            )
            websites["ctrip"] = ctrip_url
        else:
            continue
    if "ctrip" not in websites:
        city_name = await get_city_name(urls["city"])
        if f"{urls['name_en']} {city_name}" not in ctrip_maps:
            cid = await get_ctrip_id(urls["name_en"], city_name)
            ctrip_maps[f"{urls['name_en']} {city_name}"] = cid
        cid = ctrip_maps[f"{urls['name_en']} {city_name}"]
        logger.info(f'find ctrip id with {urls["name_en"]}, {city_name}')
        if cid:
            websites["ctrip"] = str(
                URL(
                    f"http://m.ctrip.com/webapp/hotel/j/hoteldetail/dianping/rooms/{cid}"
                ).with_query(
                    {
                        'inday': checkin.replace('-', '/'),
                        'outday': checkout.replace('-', '/'),
                        'subchannel': '',
                        'hotelchannel': '1',
                        'isoversea': '1'
                    }
                )
            )
        else:
            logger.warning(f"not find ctrip hotel id! {urls['name_en']}")
    logger.info(
        f"start_compair with websites: {websites} and compair: {compair}"
    )
    if not true_query_uid:
        await add_compair_task.start_compair(websites, compair)
    else:
        await update_premium(compair, query_key.replace('record', 'compare'))


async def get_ctrip_id(hotel_name, hotel_city=""):
    resp = None
    async with aiohttp.ClientSession() as sess:
        async with sess.get(
            f"http://m.ctrip.com/restapi/h5api/searchapp/search?action=autocomplete&source=globalonline&keyword={hotel_name}",
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
            },
        ) as res:
            if res.status == 200:
                try:
                    resp = await res.json()
                except Exception as exc:
                    logger.info(f"get ctrip id false!", exc_info=exc)
                    return False
    if not resp or not resp["data"]:
        return False
    hid = resp["data"][0]["url"].split("/")[-1]
    return hid


async def get_city_name(city_id):
    hub = databases("hub")
    name = await hub["meta_cities"].find_one(
        {"_id": city_id}, {"name_en": "1"}
    )
    if name:
        return name["name_en"]
    else:
        return ""


@api_v1.post("/record/user")
async def record_user_behavior(request):
    logger = logging.getLogger(__name__)
    payload = await check_request(request)
    if 'errmsg' in payload:
        logger.error(f"{payload['errmsg']}")
        request.headers['Accept'] = 'application/json'
        return rest_result(
            request,
            {'status': 400, 'errmsg': payload['errmsg']}
        )
    stage = payload["stage"]
    cms_id = payload["cms_id"]
    user_id = payload["user_id"]
    room_type = payload["room_type"]
    price = payload["price"]
    checkin = payload["checkin"]
    checkout = payload["checkout"]
    meal_type = payload["meal_type"]
    is_package = payload["is_package"]
    source = payload["source"]
    cancel_policy = payload["cancel_policy"]
    user_ip = payload['user_ip']
    source_type = payload['source_type']
    deal_check_code = payload['deal_check_code']
    voucher = payload['voucher']
    uid, format_payload = await save_user_record(
        cms_id,
        stage,
        price,
        checkin,
        room_type,
        checkout,
        meal_type,
        is_package,
        user_id,
        source,
        cancel_policy, 
        user_ip,
        source_type,
        voucher,
        deal_check_code
    )
    if stage == 'availability':
        price = format_payload['weego_price']
        room_type = format_payload['room_type']
        meal_type = format_payload['meal_type']
        cancel_policy = format_payload['cancel_policy']
    if stage == "preparation" or stage == "availability":
        logger.info(f"send compare task with {payload}")
        await send_compair_task(
            cms_id,
            stage,
            price,
            checkin,
            room_type,
            checkout,
            meal_type,
            is_package,
            user_id,
            source,
            cancel_policy,
            user_ip,
            source_type,
            voucher,
            deal_check_code,
            str(uid)
        )

    return rest_result(request, {"status": 200, "data": "ok"})


async def save_user_record(
    cms_id,
    stage,
    price,
    checkin,
    room_type,
    checkout,
    meal_type,
    is_package,
    user_id,
    source,
    cancel_policy,
    user_ip,
    source_type,
    voucher,
    deal_check_code
):
    db = databases("scripture")
    payload = {
        "cms_id": cms_id,
        "stage": stage,
        "checkin": checkin,
        "checkout": checkout,
        "is_package": is_package,
        "user_id": user_id,
        "query_time": datetime.now(),
        'source': source,
        'source_type': source_type,
        'user_ip': user_ip,
        'created_at': datetime.now(),
        'weego_price': price,
        'meal_type': meal_type,
        'room_type': room_type,
        'cancel_policy': cancel_policy,
    }
    if stage == "availability":
        if price:
            payload['weego_price'] = float(price[0]['price'])
            payload['meal_type'] = price[0].get('meal_type', '')
            payload['cancel_policy'] = price[0].get('cancel_policy', '')
            payload['room_type'] = price[0].get('room_type', '')
            payload['weego_availability'] = price
        else:
            payload['weego_price'] = '当日无报价'
            payload['meal_type'] = ''
            payload['cancel_policy'] = ''
            payload['weego_availability'] = []
            payload['room_type'] = ''
    elif stage == "booking":
        payload['deal_check_code'] = deal_check_code
        payload['voucher'] = voucher
    else:
        # preparation or cancellation
        logger.debug(f"stage: {stage}")
    # 目前除下订和取消外，传入的都是单价，在此处更新为总价
    if isinstance(payload['weego_price'], float) and stage not in ['booking', 'cancellation']:
        book_day = (
            datetime.strptime(payload['checkout'], '%Y-%m-%d')
            - 
            datetime.strptime(payload['checkin'], '%Y-%m-%d')
        ).days
        payload['weego_price'] *= book_day
    res = await db["compair"].insert_one(payload)
    return res._InsertOneResult__inserted_id, payload


async def check_request(request):
    logger = logging.getLogger(__name__)
    body = request.json
    if not body:
        logger.error(f"invalid request without body!")
        return {'errmsg': 'must post non-empty request'}
    stage = body.get("stage", "")
    # 以前约定的单词拼写错了，在此处兼容
    if stage == 'cancelation':
        stage = 'cancellation'
    cms_id = body.get("cms_id", "")
    user_id = body.get("user_id", "")
    room_type = body.get("room_type", "")
    price = body.get("price", "")
    checkin = body.get("checkin", "")
    checkout = body.get("checkout", "")
    meal_type = body.get("meal_type", False)
    cancel_policy = body.get('cancel_policy', '')
    is_package = body.get("is_package", False)
    voucher = body.get('voucher', '')
    deal_check_code = body.get('deal_check_code', '')
    user_ip = body.get('user_ip', '')
    source = body.get("source", "")
    source_type = body.get('source_type', '')
    if stage not in settings.STAGES:
        logger.error(f"invalid stage: {stage}")
        return {"errmsg": f'stage: {stage} invalid, must be one of :{settings.STAGES}'}
    if stage == 'availability':
        if price and isinstance(price, str):
            logger.error(f"invalid price: {price} with stage: {stage}")
            return {"errmsg": f'price: {stage} invalid in stage:{stage}, must be None(当日无报价) or list(每个房型价格)'}
    elif stage == 'preparation':
        if price:
            try:
                price = float(price)
            except Exception:
                logger.error(f"invalid price: {price} with stage: {stage}")
                return {"errmsg": f'price: {stage} invalid in stage:{stage}, must be None or float/str(float)'}
    elif stage == 'booking': 
        if not voucher and deal_check_code:
            logger.error(f"")
            return {'errmsg': "booking stage must provider voucher or deal_check_code"}
    elif stage == 'cancellation': 
        ...
    try:
        datetime.strptime(checkin, '%Y-%m-%d')
    except Exception:
        logger.error(f"invalid checkin: {checkin}")
        return {'errmsg': f"checkin invalid : {checkin}, must be YYYY-mm-dd"}
    try:
        datetime.strptime(checkout, '%Y-%m-%d')
    except Exception:
        logger.error(f"invalid checkout: {checkout}")
        return {'errmsg': f"checkout invalid : {checkout}, must be YYYY-mm-dd"}
    try:
        ObjectId(cms_id)
    except Exception:
        logger.error(f"invalid cms_id: {cms_id}")
        return {'errmsg': f'invalid cms_id: {cms_id}, must be an ObjectId'}
    return {
        'stage': stage,
        'cms_id': cms_id,
        'user_id': user_id,
        'room_type': room_type,
        'price': price,
        'checkin': checkin,
        'checkout': checkout,
        'meal_type': meal_type,
        'is_package': is_package,
        'source': source,
        'cancel_policy': cancel_policy,
        'user_ip': user_ip,
        'source_type': source_type,
        'voucher': voucher,
        'deal_check_code': deal_check_code
    }


async def update_premium(data, fir_query):
    logger = logging.getLogger(__name__)
    db = databases(settings.REDIS)
    i = 0
    while True or i > 20:
        compare_msg = await db.get(fir_query)
        if not compare_msg:
            time.sleep(5)
            i += 1
            continue
        data.update(json.loads(compare_msg))
        await async_price_compare_check(data)
        # 将数据传给溢价系统，供动态溢价使用
        # async with aiohttp.ClientSession() as sess:
        #     async with sess.post(
        #         f"",
        #         headers={},
        #         json=data
        #     ) as res:
        #         ...
        break
    logger.info(f"{fir_query} send data to premium succeed!")
    return