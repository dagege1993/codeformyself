# coding: utf-8

import json
from bson import ObjectId
import aiohttp
import logging
from web.utils.database import databases
from web import settings
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


async def find_hotels(
    hotel_ids: list = None,
    keywords: list = None,
    destination: str = None,
    position: str = None,
    suppliers: list = None,
    single: str = None,
    rating: str = None,
    **kwargs,
) -> list:
    """
    all query is AND
    query = {
        'hotel_ids': [ str(ObjectId) ],
        'keywords': [ k1, k2, k3, ... ],
        'destination': str(ObjectId) of meta_{position} or name_en.title() of continent,
        'position': Enum{'continent', 'country', 'province', 'city'},
        'suppliers': [ str(ObjectId) ], // allow
        'single': str(ObjectId), // only one supplier
        'rating': TripAdviser rating,
    }
    return [ str(ObjectId) of poi_items ]
    """
    hotels = hotel_ids or []
    hotels = set(hotels)
    kw_hotels = set()
    if keywords:
        async with aiohttp.ClientSession() as sess:
            async with sess.get(
                f"{settings.SOLR}/solr/hub-products/select",
                params={"q": " or ".join(keywords), "rows": 1000},
                headers={"accept": "application/json"},
            ) as res:
                if res.status == 200:
                    resp = await res.text()
                    resp = json.loads(resp)
                else:
                    resp = {"response": {"docs": {}}}
        for _id in resp["response"]["docs"]:
            if _id["type"] == "hotels":
                kw_hotels.add(_id["id"])
        if hotels and kw_hotels:
            hotels = hotels and kw_hotels
        else:
            hotels = hotels or kw_hotels
        logger.info(f"hotels of keywords : {hotels}")

    if position:
        hub = databases("hub")
        position = position.lower()
        condition = {"city": {"$in": []}}
        if position == "continent":
            async for country in hub["meta_countries"].find(
                {"continent": destination.title()}, {"_id": "1"}
            ):
                async for city in hub["meta_cities"].find(
                    {"country": country["_id"]}, {"_id": "1"}
                ):
                    condition["city"]["$in"].append(city["_id"])
        elif position == 'country':
            async for city in hub['meta_cities'].find(
                    {"country": ObjectId(destination)}, {"_id": "1"}
                ):
                    condition["city"]["$in"].append(city["_id"])
        elif position == "province":
            async for city in hub["meta_cities"].find(
                {position: ObjectId(destination)}, {"_id": "1"}
            ):
                condition["city"]["$in"].append(city["_id"])
        else:
            condition["city"] = ObjectId(destination)
        logger.info(f"position condition : {condition}")
        hotels = await hotel_filter(condition, hotels)
        logger.info(f"hotels of position : {hotels}")

    if rating:
        try:
            rating = int(rating)
        except Exception:
            return False
        condition = {"rating": {"$gte": int(rating)}}
        hotels = await hotel_filter(condition, hotels)
    logger.info(f"hotels of rating : {hotels}")

    if suppliers:
        for supplier in suppliers:
            if supplier not in settings.SUPPLIER_ID_2_NAME:
                return False
        condition = {
            "quote_ids.quoter": {"$in": [ObjectId(qid) for qid in suppliers]}
        }
        hotels = await hotel_filter(condition, hotels)
        logger.info(f"hotels of suppliers : {hotels}")

    if single:
        if single not in settings.SUPPLIER_ID_2_NAME:
            return False
        condition = {
            "$and": [
                {"quote_ids.quoter": ObjectId(single)},
                {"quote_ids": {"$size": 1}},
            ]
        }
        hotels = await hotel_filter(condition, hotels)
        logger.info(f"hotels of single : {hotels}")
    result = {}
    if hotels:
        for cms_id in list(hotels):
            result[f"cms::{cms_id}"] = [{'quoter': 'cms', 'hotel_id': cms_id}]
    return result


async def validate_request(request):
    """
    校验请求参数合法性 & 整合酒店\n
    `start_time`最早为当前日期\n
    `end_time` 和 `days` 同时存在则取最长的一个\n
    返回更新后的`start_time`、`end_time`、`days`\n
    返回的`hotels`格式为 {
        'quoter1::hotel_id1;quoter2::hotel_id2': 
            [
                {
                    'quoter': str(ObjectId of sku_quoter),
                    'hotel_id': ''
                },
                {
                    'quoter': str(ObjectId of sku_quoter),
                    'hotel_id': ''
                }
            ]
        }
    支持以添加至cms的酒店和供应商酒店同步查价\n
    `query`目前仅支持对已上线酒店进行查询
    """
    try:
        body = request.json
        start_time = body.get("start_time", "")  # 查价范围起始日期
        end_time = body.get("end_time", "")  # 查价范围结束日期
        days = body.get("days", 0)  # 查价日期数，与`end_time`取最大值

        """
        查询酒店集 [
            [
                {'quoter': 'hotelspro', 'hotel_id': '123def'},
                {'quoter': 'HotelBeds', 'hotel_id': '123456'}
            ],
            [
                {'quoter': 'cms', 'hotel_id': str(ObjectId)},
                {'quoter': str(ObjectId), 'hotel_id': '123123'}
            ],
            [
                {'quoter': str(ObjectId), 'hotel_id': '123456'},
                {'quoter': str(ObjectId), 'hotel_id': '123123'},
                {'quoter': 'bonotel', 'hotel_id': '12123'}
            ],
        ]
        """
        ori_hotels = body.get("hotels", [])  #
        query = body.get("query", "")  # 查询条件
        prices_type = body.get("prices_type")  #
        provider = body.get("provider", "")  #
        compare = body.get("compare", [])  # 需要比价的网站 目前支持booking/ctrip
        is_ori_price = body.get('is_ori_price', False)
        to_text = body.get('to_text', False)
        only_compare = body.get('only_compare', False)
        is_without_tax = body.get('is_without_tax', False)
        only_supplier = body.get('only_supplier', [])
        query_hotels = {}
        merge_hotel = {}
        errmsg = ''
        try:
            if isinstance(only_supplier, str):
                only_supplier = only_supplier.lower()
                if only_supplier in settings.SUPPLIER_ID_2_NAME or only_supplier in settings.SUPPLIER_NAME_2_ID:
                    only_supplier = [settings.SUPPLIER_ID_2_NAME.get(only_supplier, only_supplier)]
                else:
                    errmsg += f"invalid only_supplier : {body['only_supplier']}\n"
            elif isinstance(only_supplier, list):
                only_supplier = [
                    settings.SUPPLIER_ID_2_NAME.get(e.lower(), e.lower()) for e in only_supplier
                ]
            else:
                errmsg += f"invalid only_supplier type: {body['only_supplier']}\n"
        except Exception as exc:
            errmsg += f"invalid only_supplier : {body['only_supplier']}\n"
        if query:
            if isinstance(query, str):
                query = json.loads(query)
            query_hotels = await find_hotels(**query)
            logger.info(f"query hotels : {query_hotels}")
        if not (query_hotels or ori_hotels):
            errmsg += f"invalid query!\n{json.dumps(body)}\n"
        else:
            for hotel in ori_hotels:
                if isinstance(hotel, list):
                    uid = get_uid(hotel)
                    for hotel_dict in hotel:
                        hotel_dict['quoter'] = settings.SUPPLIER_NAME_2_ID.get(hotel_dict.get('quoter').lower(), hotel_dict.get('quoter'))
                    merge_hotel[uid] = hotel
                elif isinstance(hotel, str):
                    hotels = []
                    for _hotel in hotel.split(';'):
                        quoter = _hotel.split('::')[0].lower()
                        quoter_id = settings.SUPPLIER_NAME_2_ID.get(quoter, quoter)
                        hotels.append({'quoter': quoter_id, 'hotel_id': _hotel.split("::")[1].strip()})
                    uid = get_uid(hotels)
                    merge_hotel[uid] = hotels
                elif isinstance(hotel, dict):
                    errmsg = f"invalid hotel data type for {hotel} must be str or list!\n"
                else:
                    errmsg = f"invalid hotel data! : {hotel}\n"
            merge_hotel.update(query_hotels)

        if start_time and (end_time or days):
            ori_start_time = start_time
            ori_end_time = end_time
            ori_days = days
            try:
                query_start_time = datetime.strptime(
                    ori_start_time, "%Y-%m-%d"
                )
            except Exception:
                logger.error(f"invalid start_time : {ori_start_time}")
                return {"errmsg": f"invalid start_time : {ori_start_time}"}
            # 避免传入的开始时间早于当前日期导致无效查询
            _start_time = max(datetime.now(), query_start_time)
            start_time = _start_time.strftime("%Y-%m-%d")
            _end_time = None
            if ori_end_time:
                try:
                    _end_time = datetime.strptime(ori_end_time, "%Y-%m-%d")
                    if _end_time <= _start_time:
                        logger.error(
                            f"end_time can not be earlier than "
                            f"start_time({ori_start_time}) or now : {ori_end_time}"
                        )
                        return {"errmsg": f"invalid end_time : {end_time}"}
                except ValueError:
                    logger.error(f"invalid end_time : {ori_end_time}")
            if _end_time:
                end_time = ori_end_time
                days = (
                    datetime.strptime(ori_end_time, "%Y-%m-%d") - _start_time
                ).days + 1
            else:
                if start_time == ori_start_time:
                    days = ori_days
                else:
                    days = (
                        ori_days - (datetime.now() - query_start_time).days + 1
                    )
                    if days <= 0:
                        return {
                            "errmsg": f"invalid start_time and days: {ori_start_time}/{ori_days}"
                        }
                end_time = (
                    datetime.strptime(start_time, "%Y-%m-%d")
                    + timedelta(days=days)
                ).strftime("%Y-%m-%d")
        else:
            return {"errmsg": f"invalid request {request}"}
        return {
            "start_time": start_time,
            "start_time_dt": _start_time,
            "end_time": end_time,
            "days": days,
            "hotels": merge_hotel,
            "errmsg": errmsg,
            "prices_type": prices_type,
            "provider": provider,
            "compare": compare,
            "is_ori_price": is_ori_price,
            "to_text": to_text,
            "only_compare": only_compare,
            "is_without_tax": is_without_tax,
            "only_supplier": only_supplier,
        }
    except Exception as exc:
        logger.info(f"invalid request {request}", exc_info=exc)
        return {"errmsg": f"invalid request {request}"}


def dump_fake_weego_price(prices):
    for price in prices:
        if price.get("is_calculate"):
            price["price"] = "当日无报价"
    return prices


async def hotel_filter(extra_condition, selected):
    hub = databases("hub")
    condition = {
        "__t": "Hotel",
        "edit_status": {"$in": ["edited", "audited"]},
        "publish_status": "online",
    }
    condition.update(extra_condition)
    select_hotel = set()
    if selected:
        condition["_id"] = {"$in": [ObjectId(_id) for _id in selected]}
    async for hotel in hub["poi_items"].find(condition, {"_id": "1"}):
        select_hotel.add(str(hotel["_id"]))
    if selected and select_hotel:
        hotels = selected and select_hotel
    else:
        hotels = selected or select_hotel
    return hotels


def get_uid(hotel):
    hotel = sorted(
        hotel,
        key=lambda x: settings.SUPPLIER_NAME_2_ID.get(
            x["quoter".lower()], x["quoter"]
        ),
    )
    uid = ";".join(
        [
            "::".join(
                [
                    settings.SUPPLIER_NAME_2_ID.get(
                        q["quoter"].lower(), q["quoter"].lower()
                    ),
                    q["hotel_id"].strip(),
                ]
            )
            for q in hotel
        ]
    )
    return uid