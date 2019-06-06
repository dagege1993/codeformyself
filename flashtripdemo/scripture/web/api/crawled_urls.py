# coding: utf8
"""Crawled urls
"""

# Standard Library
import re
import logging
from bson import ObjectId

# Non Standard Library
from yarl import URL

# Current Project
from . import api_v1
from .abstract_datas import crawl_booking, crawl_hcom
from .formatter_response import rest_result
from web import settings
from web.utils.database import databases
from scripture.models import hub_hotel


crawling = settings.CRAWLING_WEBSITE


@api_v1.route("/crawled/<crawled_id>", methods=["GET"])
async def list_website_crawled_by_id(request, crawled_id):
    """Get list of website where we crawled from by crawled id"""

    logger = logging.getLogger(__name__)
    scripture = databases("scripture")

    if len(crawled_id) == 24:
        crawled = await scripture.capture_urls.find_one(
            {"_id": ObjectId(crawled_id)}
        )
    else:
        crawled = await scripture.capture_urls.find_one(
            {"hotel_id": crawled_id}
        )
    if not crawled:
        logger.warning("Bad crawled id %s", crawled_id)
        return rest_result(
            request, {"status": 400, "err_msg": "Invalid capture_id"}
        )
    filters = request.args.get("filters")
    if filters and isinstance(filters, str):
        kwargs = {
            "hotels_cn_id": crawled.get("hotels_cn_id"),
            "jset_id": crawled.get("jset_id"),
            "bookings_id": crawled.get("bookings_id"),
            "capture_id": crawled_id,
        }
        logging.debug(f"kwargs : {kwargs}")
        hotel = await request.app.loop.run_in_executor(
            None,
            lambda: hub_hotel.HubHotel(**kwargs).to_dict(
                columns=filters.split(",")
            ),
        )
        logging.info(f"crawled_id:{crawled_id} ,api hotel : {hotel}")
        keys = [f.strip() for f in filters.split(",")]
        if "all" in keys:
            logger.info(f'crawled_id:{crawled_id} crawled success and "all" in keys ')
            return rest_result(request, {"hotel": hotel, "status": 200})
        hotel = {key: filed_formatter(key, hotel.get(key)) for key in keys}
        logger.info(f'crawled_id:{crawled_id} crawled success ')
        return rest_result(request, {"hotel": hotel, "status": 200})
    urls = {}
    if crawled.get("hotels_cn_id") or crawled_id.get("_hotels_cn_id"):
        urls["hotels.cn"] = (
            "https://www.hotels.cn/"
            f'ho{crawled.get("hotels_cn_id") or crawled_id.get("_hotels_cn_id")}'
        )  # noqa
    if crawled.get("jset_id") or crawled_id.get("_jset_id"):
        jset = await scripture.jsets.find_one(
            {"jset_id": crawled.get("jset_id") or crawled_id.get("_jset_id")}
        )
        if not jset:
            logger.warning("Jset not found %s", crawled.get("jset_id"))
        else:
            urls["jetsetter.com"] = jset["url"]
    if crawled.get("hotel_id") and not crawled.get("bookings_id"):
        urls["roomsxml id"] = crawled.get("hotel_id")

    if crawled.get("bookings_id") or crawled.get("_bookings_id"):
        urls["bookings"] = crawled.get("bk_url")

    if urls:
        logger.info(f'crawled_id:{crawled_id} , found url:{urls}')
        return rest_result(request, {"urls": urls, "status": 200})

    logger.info(f'crawled_id:{crawled_id} , not found url')
    return rest_result(request, {"err_msg": "Not Found", "status": 404})


@api_v1.route("/hotel_static/<crawled_id>", methods=["GET"])
async def crawl_statics_data(request, crawled_id):
    logger = logging.getLogger(__name__)
    url = request.args.get("url")
    _url = URL(url)
    url = f"{_url.scheme}://{_url.host}{_url.path}"
    website = request.args.get("website")
    scripture = databases("scripture")
    if not website or website not in crawling:
        logger.warning("Bad website : not website or website not in crawling")
        return rest_result(
            request, {"status": 400, "err_msg": "Invalid website!"}
        )

    if len(crawled_id) == 24:
        exists = await scripture.capture_urls.find_one(
            {"_id": ObjectId(crawled_id)}
        )
    else:
        exists = await scripture.capture_urls.find_one(
            {"hotel_id": crawled_id}
        )
    if not exists:
        logger.info(f"invalid crawled_id!: {crawled_id}")
        return rest_result(request, {"status": 400, "errmsg": f"invalid crawled_id!: {crawled_id}"})
    if website in exists and exists[website] == url:
        logger.info(f'{crawled_id} 此网站已经抓取')
        return rest_result(request, {"status": 200, "data": "此网站已经抓取"})
    if website == "bk_url":
        try:
            res = await crawl_booking(str(exists["_id"]), url)
        except Exception as exc:
            logging.warning("", exc_info=exc)
            res = {
                "status": 500,
                "errmsg": f"网站抓取失败，请联系刘博文同学(liubowen@weego.me)\n{exc}",
            }
    elif website == "hcom_id":
        try:
            res = await crawl_hcom(crawled_id, url)
        except Exception as exc:
            logging.warning("", exc_info=exc)
            res = {
                "status": 500,
                "errmsg": f"网站抓取失败，请联系刘博文同学(liubowen@weego.me)\n{exc}",
            }
    else:
        logger.warning(f'Invalid website:{website}')
        return rest_result(
            request, {"status": 400, "err_msg": "Invalid website!"}
        )

    if res and res.get('status') == 200:
        scripture.capture_urls.update_one(
            {"_id": exists["_id"]}, {"$set": {website: url}}
        )
        logger.info(f'url:{url},酒店静态数据抓取完成')
        return rest_result(request, {"status": 200, "data": "酒店静态数据抓取完成!"})
    else:
        logger.warning(f'{crawled_id}抓取失败.errmsg: {res["errmsg"]}')
        return rest_result(
            request, {"status": 500, "errmsg": f"{res['errmsg']}"}
        )


@api_v1.route("/crawl/hcom/<capture_id>", methods=["GET"])
async def _crawl_hcom(request, capture_id):
    logger = logging.getLogger(__name__)
    url = request.args.get("url")
    if not capture_id or not url:
        logger.warning(f"invalid request : {request}")
        return rest_result(
            request, {"status": 400, "errmsg": "params invalid"}
        )
    result = await crawl_hcom(capture_id, url)
    logger.info(f'hcom_url:{url} crawl success')
    return rest_result(request, result)


@api_v1.route("/crawl/booking/<capture_id>", methods=["GET"])
async def _crawl_booking(request, capture_id):
    logger = logging.getLogger(__name__)
    url = request.args.get("url")
    if not capture_id or not url:
        logger.warning(f"invalid request : {request}")
        return rest_result(
            request, {"status": 400, "errmsg": "params invalid"}
        )
    result = await crawl_booking(capture_id, url)
    logger.info(f'bk_url:{url} crawl success')
    return rest_result(request, result)


def filed_formatter(filed, info):
    if filed == 'policy':
        for policy in info:
            if '并有权在您抵达之前进行预授权' in policy["content"]:
                policy["content"] = policy["content"].replace('并有权在您抵达之前进行预授权', '')
            if '请输入您的入住日期并参阅您所需的客房的条款' in policy["content"]:
                policy["content"] = re.sub('请输入您的入住日期并参阅您所需的客房的条款。\n?', '', policy["content"])
    return info