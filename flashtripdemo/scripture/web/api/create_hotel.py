# coding: utf8
"""Crawled urls
"""

# Standard Library
import logging

import aiohttp
from yarl import URL
import concurrent.futures

from web import settings
from web.utils.database import databases

# Current Project
from . import api_v1
from .crawled_urls import crawl_booking, crawl_hcom, rest_result
from scripture.models.hub_hotel import transfor_pic_url, executor
from .abstract_datas import forrmat_relux_rooms, fetch_relux_comment, fix_relux_facility, fix_relux_policy_traffic

crawling = settings.CRAWLING_WEBSITE

upload_url = f"{settings.CMS_API}/api/internal/hotels"


@api_v1.route("/creating/hotel", methods=["POST", "OPTIONS"])
async def upload_hotel(request):
    logger = logging.getLogger(__name__)
    request.headers["Accept"] = "application/json"
    body = request.json
    ori_name = body.get("name")
    supplier = body.get("supplier")
    hotel_id = body.get("hid", '').strip()
    website = body.get("website")
    crawl_url = body.get("url")
    ori_address = body.get("address")
    _id = body.get("cmsId")
    updated_by = body.get('updatedBy')
    logging.debug(f"body : {body}")
    comments = body.get("comments")
    comments_url = body.get("comments_url")
    capture_id = await capture_insert(hotel_id)
    capture_id = str(capture_id)
    rooms_payload = None

    # 保证更新capture_id
    if not supplier or supplier not in settings.SUPPLIER_ID_2_NAME:
        async with aiohttp.ClientSession(headers={"accept-version": "6.0.0"}) as sess:
            async with sess.post(
                upload_url,
                json={"id": _id, "capture_id": capture_id, 'updatedBy': updated_by},
            ) as resp:
                logging.debug(f"resp : {resp}")
                logger.warning('必须提供一个合法的供应商名称')
        if not crawl_url:
            return rest_result(
                request, {"status": 400, "errmsg": "必须提供一个合法的供应商名称或抓取的第三方网站"}
            )
    if not hotel_id and not crawl_url:
        logger.warning('必须提供一个供应商酒店ID或供抓取的第三方网站')
        return rest_result(request, {"status": 400, "errmsg": "必须提供一个供应商酒店ID或供抓取的第三方网站"})
    statics_data = await supplier_data(supplier, hotel_id)
    logger.debug(f"statics_data: {statics_data}")

    if website in crawling:
        url = URL(crawl_url)
        url = f"{url.scheme}://{url.host}{url.path}"
        crawl_data = await crawl_website(website, url, capture_id)
        logger.debug(f'crawl_data: {crawl_data}')
        payload = merge_payload(
            statics_data,
            ori_name,
            ori_address,
            hotel_id,
            supplier,
            capture_id,
            website,
            url,
            crawl_data,
        )
    else:
        payload = merge_payload(
            statics_data,
            ori_name,
            ori_address,
            hotel_id,
            supplier,
            capture_id,
            website,
            crawl_url,
            {}
        )
    payload["id"] = _id
    payload['updatedBy'] = updated_by
    if comments:
        payload["comments"] = comments
        payload["comments_url"] = comments_url
    logger.info(f"请求创建酒店的原始数据:payload : {payload}")
    async with aiohttp.ClientSession(headers={"accept-version": "6.0.0"}) as sess:
        async with sess.post(
            upload_url, json=payload,
        ) as res:
            resp = await res.json()
    if not resp or resp["status"] != 200:
        logger.warning(f'hotel_id:{hotel_id},上传酒店失败: resp: {resp} ')
        return rest_result(request, {"status": 400, "errmsg": "上传酒店失败！"})
    if "_id" in resp["data"]:
        _id = resp["data"]["_id"]
    elif "id" in resp["data"]:
        _id = resp["data"]["id"]
    else:
        _id = resp
    
    # relux 直接上传房型
    if settings.SUPPLIER_ID_2_NAME[supplier] == "relux":
        db = databases("scripture")
        _rooms = await db['statics.hotels.relux.rooms'].find_one({'code': str(hotel_id)}, {'rooms': '1', 'rooms_cn': '1'})
        if _rooms:
            rooms = await forrmat_relux_rooms(_rooms.get('rooms_cn'), _rooms.get('rooms'))
            logger.info(f"rooms : {[e['room_type'] for e in rooms]}")
            for room in rooms:
                room['capture_id'] = capture_id
            rooms_payload = {
                'capture_id': capture_id,
                'rooms': rooms,
                'updatedBy': updated_by
            }
            async with aiohttp.ClientSession(headers={"accept-version": "6.0.0"}) as sess:
                async with sess.post(
                    f"{upload_url}/hotelrooms/{capture_id}",
                    json=rooms_payload,
                ) as res:
                    resp = await res.json()
    logger.info(f'_id:{_id} upload success')
    return rest_result(request, {"status": 200, "data": rooms_payload or _id})


async def supplier_data(supplier, hotel_id):
    logger = logging.getLogger(__name__)
    coll = settings.SUPPLIER_NAME_2_COLL[settings.SUPPLIER_ID_2_NAME[supplier]]
    if coll == 'wg_hotel':
        db = databases('whotel')
    else:
        db = databases("scripture")
    query = settings.SUPPLIER_QUERY[settings.SUPPLIER_ID_2_NAME[supplier]]
    query["code"] = "1"
    condition = [{'code': hotel_id}, {'hotel_id': str(hotel_id)}]
    try:
        int_hotel_id = int(hotel_id)
        condition.append({"code": int_hotel_id})
        condition.append({"hotel_id": int_hotel_id})
    except Exception :
        pass
    s_data = await db[coll].find_one(
       {'$or': condition} , query
    )
    if not s_data:
        logger.info(f'supplier:{supplier},hotel_id:{hotel_id} can not query s_data')
        return {}
    logger.info(f'supplier:{supplier},hotel_id:{hotel_id} query s_data success')
    return formatter_statics_data(settings.SUPPLIER_ID_2_NAME[supplier], s_data)


async def capture_insert(hid):
    db = databases("scripture")
    res = await db["capture_urls"].insert_one({"hotel_id": hid})
    cid = res._InsertOneResult__inserted_id
    return str(cid)


async def crawl_website(website, url, cid):
    _url = URL(url)
    url = f"{_url.scheme}://{_url.host}{_url.path}"
    if website == "bk_url" and "booking" in url:
        resp = await crawl_booking(cid, url)
    elif website == "hcom_id" and "hotels" in url:
        resp = await crawl_hcom(cid, url)
    else:
        resp = {}
        logging.warning(f"invalid website with url : {website}&{url} !")
    logging.info(f"url:{url} crawl_website success")
    return resp.get('data', {})


def formatter_statics_data(supplier, ori_data):
    if supplier == "bonotel":
        data = dict(
            name=ori_data.get("name_cn", ""),
            name_en=ori_data.get("name", ""),
            hotel_id=ori_data["code"],
            address=ori_data.get("address", ""),
            latitude=ori_data.get("latitude", ""),
            longitude=ori_data.get("longitude", ""),
            rating=ori_data.get("wgstar", ""),
            telephone=ori_data.get("phone", ""),
        )
    elif supplier == "hotelbeds":
        data = dict(
            name=ori_data.get("name_cn", ""),
            name_en=ori_data.get("name", ""),
            hotel_id=ori_data["code"],
            address=ori_data.get("address", ""),
            latitude=ori_data.get("latitude", ""),
            longitude=ori_data.get("longitude", ""),
            telephone=ori_data.get("phone", ""),
            website=ori_data.get("web", "") or ori_data.get("website", ""),
            city_name=ori_data.get("province", ""),
        )
    elif supplier == "hotelspro":
        data = dict(
            name=ori_data.get("name_cn", ""),
            name_en=ori_data.get("name", ""),
            hotel_id=ori_data["code"],
            address=ori_data.get("address", ""),
            latitude=ori_data.get("latitude", ""),
            longitude=ori_data.get("longitude", ""),
            telephone=ori_data.get("phone", ""),
            city_name=ori_data.get("province", ""),
        )
    elif supplier == "jactravel":
        data = dict(
            name=ori_data.get("name_cn", ""),
            name_en=ori_data.get("name", ""),
            hotel_id=ori_data["code"],
            address=ori_data.get("address", ""),
            latitude=ori_data.get("latitude", ""),
            longitude=ori_data.get("longitude", ""),
            telephone=ori_data.get("phone", ""),
            city_name=ori_data.get("province", ""),
        )
    elif supplier == "relux":
        data = dict(
            name=ori_data.get("name_cn", ""),
            name_en=ori_data.get("name", ""),
            name_ruby=ori_data.get('ruby', ""),
            hotel_id=ori_data["code"],
            address=ori_data.get("address", ""),
            latitude=ori_data.get("latitude", ""),
            longitude=ori_data.get("longitude", ""),
            telephone=ori_data.get("tel", ""),
            website=ori_data.get("url", ""),
            city_name=ori_data.get("province", ""),
            policy=ori_data.get("policy_cn", []),
            gallery=ori_data.get("gallery", []),
            traffic_info=ori_data.get('traffic_info_cn', []),
            introduction=ori_data.get('description_cn', '')
        )
        data['name_en'] = f"{data['name_en']}  （{data.get('name_ruby')}）"
        data['introduction'].replace('\r\n', '\n').replace('\n\n', '\n').replace('◆', '').replace('★', '').replace('・', '').replace('~', '').replace('※', '').replace('～', '')
        for i, url in enumerate(
            executor.map(
                transfor_pic_url, data['gallery']
            )
        ):
            data['gallery'][i]['image_url'] = url
        if data['policy']:
            data['policy'] = fix_relux_policy_traffic(data['policy'], 'policy')
        if data['traffic_info']:
            data['traffic_info'] = fix_relux_policy_traffic(data['traffic_info'], 'traffic')
    elif supplier == "whotel":
        data = dict(
            name=ori_data.get("name_cn", ""),
            name_en=ori_data.get("name_en", ""),
            hotel_id=ori_data["code"],
            address=ori_data.get("address", ""),
            latitude=ori_data.get("latitude", ""),
            longitude=ori_data.get("longitude", ""),
            telephone=ori_data.get("tel", ""),
            website=ori_data.get("url", ""),
        )
    elif supplier == 'travflex':
        data = dict(
            name=ori_data.get("name_cn", ""),
            name_en=ori_data.get("name_en", ""),
            hotel_id=ori_data["code"],
            address=ori_data.get("address", ""),
            latitude=ori_data.get("latitude", ""),
            longitude=ori_data.get("longitude", ""),
            telephone=ori_data.get("tel", ""),
            website=ori_data.get("url", ""),
        )
    else:
        return {}
    return data


def merge_payload(
    datas, ori_name, ori_address, hotel_id, quotes, capture_id, website, url, crawl_data
):
    if not datas:
        datas = {}
    datas["crawl_info"] = [{"crawl_url": url, "crawl_website": website}]
    datas_name_en = datas.get("name_en", "").strip().lower()
    datas_name_cn = datas.get("name", "").strip().lower()
    datas["quote_ids"] = [{"quoter": quotes, "hotel_id": hotel_id}]
    datas["capture_id"] = capture_id
    if ori_name.strip().lower() in [datas_name_en, datas_name_cn]:
        if datas.get("name") == "":
            datas["name"] = ori_name
    elif datas_name_cn == "" :
        datas["name"] = ori_name
    else:
        datas["name"] = f"供应商酒店名称：{datas.get('name')} ； 创建时名称：{ori_name}"
    if datas.get("name") == "" and crawl_data:
        datas["name"] = ori_name or datas_name_cn or crawl_data.get('name') or datas_name_en
    elif datas.get("name") == "":
        datas["name"] = ori_name or datas_name_cn or datas_name_en
    if datas.get("address", "").strip() == "":
        datas["address"] = ori_address
    if crawl_data.get('latitude') and not datas.get('latitude'):
        datas['latitude'] = crawl_data['latitude']
    if crawl_data.get('longitude') and not datas.get('longitude'):
        datas['longitude'] = crawl_data['longitude']
    
    return datas
