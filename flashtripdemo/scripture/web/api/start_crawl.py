# conding: utf8
# Standard Library

import json

from bson import ObjectId
from yarl import URL
import xlrd
import logging

# Non Standard Library
from aioredis import create_redis
from sanic.response import html

# Current Project
from web import settings
from . import api_v1
from .formatter_response import rest_result
from web.utils.database import databases

XLSXMIME = 'application/vnd.ms-excel'
logger = logging.getLogger(__name__)


@api_v1.post('/crawl/upload')
async def _crawl_upload(request):
    excel = request.files.get('excel')
    if not excel:
        logger.info(f'{request}包含文件为空')
        return rest_result(
            request, {"status": 403, "errmsg": "文件为空"}
        )
    excel_info = f'文件名: {excel.name},mime: {excel.type}'
    opt = request.form.get('opt')
    if not opt:
        logger.info(f'{request}{excel_info} invalid params : opt')
        return rest_result(
            request, {"status": 400, "errmsg": "params invalid"}
        )
    if XLSXMIME != excel.type:
        logger.info(f'{request}{excel_info} 上传了错误的文件类型')
        return rest_result(
            request, {"status": 403, "errmsg": "错误的文件类型"}
        )
    book = xlrd.open_workbook(file_contents=excel.body)
    url_ori_info = book.sheet_by_index(0)
    result = await write_redis(opt, url_ori_info)
    logger.info(f'{request}上传了一份excel文件,response_dict:{result}')
    return rest_result(request, result)


@api_v1.post('/crawl/status')
async def _crawl_status(request):
    excel = request.files.get('excel')
    if not excel:
        logger.info(f'{request} 包含文件为空')
        return rest_result(
            request, {"status": 403, "errmsg": "文件为空"}
        )
    excel_info = f'文件信息:文件名: {excel.name}mime: {excel.type}'
    opt = request.form.get('opt')
    query = request.args.get('query')
    if not opt or not query:
        logger.info(f'{excel_info} invalid params : opt or query')
        return rest_result(
            request, {"status": 400, "errmsg": "params invalid"}
        )
    if XLSXMIME != excel.type:
        logger.info(f'{request} 上传错误的文件类型')
        return rest_result(
            request, {"status": 403, "errmsg": "错误的文件类型"}
        )

    book = xlrd.open_workbook(file_contents=excel.body)
    url_ori_info = book.sheet_by_index(0)
    hotels_id = []
    bookings_id = []
    bookings_url_list = []
    for index in range(url_ori_info.nrows):
        url = url_ori_info.cell_value(rowx=index, colx=1)
        if not url:
            continue
        url_info = extract_url(url)
        host = url_info.get("url_host")
        if opt == 'hcom' and (
                        host == 'www.hotels.cn' or host == 'www.hotels.com'
        ):
            hid = url_info.get("hid")
            if hid in hotels_id:
                continue
            hotels_id.append(hid)
        elif opt == 'booking' and host == 'www.booking.com':
            hid = url_info.get("hid")
            if hid in bookings_id:
                continue
            bookings_id.append(hid)
            bookings_url_list.append(url_info.get("url"))
    if query == 'number':
        try:
            redis_conn = await create_redis(settings.REDIS)
            crawl_done_num = parse_redis('parse', await redis_conn.smembers(f'crawl_done_{opt}'))
            total = hotels_id + bookings_id
            unknow = set(total) - set(crawl_done_num)
            rest_dict = {
                '可以抓取的网址数目': len(total),
                '已抓取的网址数目': len(total) - len(unknow),
                '仍未成功抓取的网站id': unknow
            }
            logger.info(f'{request},query=number,文件为{excel_info}response_dict:{rest_dict}')
            return rest_result(
                request, rest_dict
            )
        except Exception as exc:
            logger.warning(f"redis 异常", exc_info=exc)
            return rest_result(
                request, {"status": 500, "errmsg": "redis lose effectiveness"}
            )
    elif query == 'details':
        scripture = databases("scripture")
        try:
            if hotels_id:
                hcom_list = scripture["hotels"].find(
                    {'hotels_id': {"$in": hotels_id}},
                    {"name": 1, "url": "1", "_id": 1}
                )
                hcom_list = [[value.get('name'), value.get('url'), value.get('_id')] async for value in hcom_list if
                             value]
                hcom_body = ''.join([
                                        f'<li>'
                                        f'<a href="/api/v1/crawl/hotels/details?db=hotels&_id={value[2]}" target="_blank">酒店名:&nbsp;{value[0]}</a>'
                                        f'&nbsp;&nbsp;&nbsp;&nbsp;'
                                        f'<a href={value[1]} target="_blank">酒店链接:&nbsp;{value[1]}</a>'
                                        f'</li>'
                                        for value in hcom_list
                                        ])
                if not hcom_body:
                    return rest_result(request, {'详情': '暂无数据'})
                return html(hcom_body)
            if bookings_id:
                bookings_list = scripture["bookings"].find(
                    {'bk_url': {"$in": bookings_url_list}},
                    {"name": 1, "bk_url": 1, "_id": 1}
                )
                bookings_list = [[value.get('name'), value.get('bk_url'), value.get('_id')] async for value in
                                 bookings_list if value]
                booking_body = ''.join([
                                           f'<li>'
                                           f'<a href="/api/v1/crawl/hotels/details?db=bookings&_id={value[2]}" target="_blank">酒店名:&nbsp;{value[0]}</a>'
                                           f'&nbsp;&nbsp;&nbsp;&nbsp;'
                                           f'<a href={value[1]} target="_blank">酒店链接:&nbsp;{value[1]}</a>'
                                           f'</li>'
                                           for value in bookings_list
                                           ])
                if not booking_body:
                    return rest_result(request, {'详情': '暂无数据'})
                return html(booking_body)
        except Exception as exc:
            logger.warning(f"mongodb 异常", exc_info=exc)
            return rest_result(
                request, {"status": 500, "errmsg": "mongodb lose effectiveness"}
            )
    else:
        logger.info(f'{request} invalid params:query')
        return rest_result(
            request, {"status": 400, "errmsg": "params invalid"}
        )


@api_v1.route("/crawl/hotels/details", methods=['GET'])
async def _hotels_details(request):
    db = request.args.get("db")
    _id = request.args.get("_id")
    scripture = databases("scripture")
    if db == "hotels":
        hotels_info = await scripture[db].find_one(
            {"_id": ObjectId(_id)}
        )
    elif db == "bookings":
        hotels_info = await scripture[db].find_one(
            {"_id": ObjectId(_id)}
        )
    else:
        hotels_info = {"status": 400, "errmsg": "params invalid"}
    logger.info(f'{request}_id :{_id },response_dict{hotels_info}')
    return rest_result(request, hotels_info)


@api_v1.get('/crawl/clear')
async def _crawl_clear(request):
    try:
        redis_conn = await create_redis(settings.REDIS)
        keys = [
            'crawl_hcom', 'crawled_hcom', 'crawl_done_hcom',
            'crawl_booking', 'crawled_booking', 'crawl_done_booking',
        ]
        await redis_conn.delete(*keys)
        logger.info(f'清除了一次历史抓取记录')
        return rest_result(request, {'clear': 'done'})
    except Exception as exc:
        logger.warning(f"redis 异常", exc_info=exc)
        return rest_result(
            request, {"status": 500, "errmsg": "redis lose effectiveness"}
        )


async def write_redis(opt, url_ori_info):
    logger = logging.getLogger(__name__)
    hotels_id = []
    bookings_id = []
    hotels_url = []
    bookings_url = []
    url_num = url_ori_info.nrows
    try:
        redis_conn = await create_redis(settings.REDIS)
        crawled_id = parse_redis('parse',
                                 await redis_conn.smembers(f"crawl_{opt}")
                                 )
    except Exception as exc:
        logger.warning(f"redis 异常", exc_info=exc)
        return {"status": 500,
                "errmsg": f"网站抓取失败，请联系刘博文同学(liubowen@weego.me)\n{exc}"}
    for index in range(url_ori_info.nrows):
        url = url_ori_info.cell_value(rowx=index, colx=1)
        if not url:
            url_num -= 1
            continue
        url_info = extract_url(url)
        host = url_info.get("url_host")
        if opt == 'hcom' and (
                        host == 'www.hotels.cn' or host == 'www.hotels.com'
        ):
            hid = url_info.get("hid")
            if hid in crawled_id or hid in hotels_id:
                continue
            hotels_id.append(hid)

            hotels_url.append(json.dumps(
                {
                    'spider_name': 'hcom_page',
                    'base_url': f"https://www.hotels.cn/ho{hid}",
                }
            ))
            hotels_url.append(json.dumps(
                {
                    'spider_name': 'hcom_page',
                    'base_url': f"https://www.hotels.com/ho{hid}/?pos=HCOM_US&locale=en_US",
                }
            ))

        elif opt == 'booking' and host == 'www.booking.com':
            hid = url_info.get("hid")
            if hid in crawled_id or hid in bookings_id:
                continue
            bookings_id.append(hid)
            bookings_url.append(json.dumps(
                {
                    'spider_name': 'booking_page',
                    'base_url': f'{url_info.get("url")}',
                }
            ))
    if hotels_url == bookings_url == []:
        return {"status": 200,
                '检测到的网址数目': url_num,
                '可以抓取的网址数目': 0}
    try:
        redis_conn = await create_redis(settings.REDIS)
        if opt == 'hcom' and hotels_url:
            await redis_conn.sadd('crawl_hcom', *hotels_id)
            await redis_conn.lpush('distributed_spider', *hotels_url)
            await redis_conn.expire('crawl_hcom', settings.REDIS_EXPIRE_TIME)
            await redis_conn.expire('hcom', settings.REDIS_EXPIRE_TIME)
            return {"status": 200,
                    '检测到的网址数目': url_num,
                    '可以抓取的网址数目': len(hotels_url) // 2}
        elif opt == 'booking' and bookings_url:
            await redis_conn.sadd('crawl_booking', *bookings_id)
            await redis_conn.lpush('distributed_spider', *bookings_url)
            await redis_conn.expire('crawl_booking', settings.REDIS_EXPIRE_TIME)
            await redis_conn.expire('booking', settings.REDIS_EXPIRE_TIME)
            return {"status": 200,
                    '检测到的网址数目': url_num,
                    '可以抓取的网址数目': len(bookings_url)}
        else:
            return {"status": 400, "errmsg": "params invalid"}
    except Exception as exc:
        logger.warning(f"redis 异常", exc_info=exc)
        return {"status": 500,
                "errmsg": f"网站抓取失败，请联系刘博文同学(liubowen@weego.me)\n{exc}"}


def extract_url(url):
    _url = URL(url)
    _url_host = _url.host
    if _url_host == 'www.hotels.cn' or _url_host == 'www.hotels.com':
        hid = _url.path.strip("/").split("/")[0][2:]
    elif _url_host == 'www.booking.com':
        hid = _url.path[7:]
    else:
        hid = 'unknow_url'
    url_info = {
        "url_host": _url_host,
        "url": f"{_url.scheme}://{_url.host}{_url.path}",
        "hid": hid
    }
    return url_info


def parse_redis(opt, bytes_obj):
    if opt == 'hcom':
        return list(map(lambda x: 'https://www.hotels.cn/ho' + x.decode(), bytes_obj))
    elif opt == 'booking':
        return list(map(lambda x: 'https://www.booking.com/hotel/' + x.decode(), bytes_obj))
    elif opt == 'parse':
        return list(map(lambda x: x.decode(), bytes_obj))
