# coding: utf-8

import xlwt
import logging
from io import BytesIO
from bson import ObjectId
from datetime import datetime, timedelta

from web.utils.database import databases
from web import settings
from web.api.formatter_response import rest_result
from sanic.response import raw, json
from web.api import api_v1


city_map = {}
stage_map = {
    'availability': '查价',
    'preparation': '验价/预订',
    'booking': '下单',
    'cancellation': '取消'
}

@api_v1.options('/user/record')
async def option_excel(request):
    return json({'data': 'ok'}, headers={"Access-Control-Allow-Origin": '*'})


@api_v1.post('/user/record')
async def get_excel(request):
    logger = logging.getLogger(__name__)
    body = request.json
    start_time = body.get('start_time', '')
    end_time = body.get('end_time', '')
    stages = body.get('stages', [])
    user = body.get('user', '')
    is_excel = body.get('is_excel', True)
    if not start_time:
        # 后续会对时间做时区校准，在此先将默认时间设置为北京时区
        start_time = datetime.now() + timedelta(hours=7)
    if not end_time:
        end_time = datetime.now() + timedelta(hours=8)
    logger.info(
        f"{user} download data with conditon: \nstart_time: {start_time}\nend_time: {end_time}\nstages: {stages}"
    )
    data = await extract_data(start_time, end_time, stages)
    if is_excel and len(data.get('info', [])) <= 65534:
        wb = save_excel(data)
        excel = BytesIO()
        wb.save(excel)
        excel.seek(0)
        return raw(
            excel.getvalue(),
            headers={
                "Access-Control-Allow-Origin": '*',
                "Content-Disposition": f"attachment;filename={start_time}-{end_time}{'/'.join(stages)}.xls"
            },
            content_type="application/vnd.ms-excel",
        )
    return json({'data': data})


async def extract_data(start_time, end_time, stages=[]):
    logger = logging.getLogger(__name__)
    db = databases("scripture")
    hub = databases("hub")
    condition = {"stage": {"$in": []}, "created_at": {}}
    for stage in stages:
        if stage in settings.STAGES:
            condition["stage"]["$in"].append(stage)
        else:
            logger.error(f"invalid stage: {stage}!")

    if isinstance(start_time, str):
        # 兼容scripture-views
        if "T" in start_time:
            start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M")
        else:
            start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    condition["created_at"]["$gte"] = start_time
    if isinstance(end_time, str):
        if "T" in end_time:
            end_time = datetime.strptime(end_time, "%Y-%m-%dT%H:%M")
        else:
            end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    # 服务器为UTC时间,比北京时间慢8小时,传入时间需-8
    condition["created_at"]["$lte"] = end_time
    result = {"hotel_count": {}, "city_count": {}, "user_count": {}}
    cms_msgs = {}
    async for data in db["compair"].find(condition):
        if data['cms_id'] not in cms_msgs:
            cms_msg = await hub["poi_items"].find_one(
                {"_id": ObjectId(data["cms_id"])},
                {"name": "1", "name_en": "1", "city": "1", "address": "1"},
            )
            cms_msgs[data['cms_id']] = cms_msg
        cms_msg = cms_msgs[data['cms_id']]
        if not cms_msg:
            logger.error(f"{data['cms_id']} not find!")
            continue
        if cms_msg["city"] not in city_map:
            city_msg = await hub["meta_cities"].find_one(
                {"_id": cms_msg["city"]}, {"name": "1"}
            )
            if not city_msg:
                city_map[cms_msg["city"]] = "该城市已被删除"
            else:
                city_map[cms_msg["city"]] = city_msg["name"]

        city_name = city_map[cms_msg["city"]]
        city_count_key = f"{city_name}:{data['stage']}"
        if city_count_key not in result["city_count"]:
            result["city_count"][city_count_key] = {
                "count": 0,
                "stage": data["stage"],
            }
        result["city_count"][city_count_key]["count"] += 1

        data["city_name"] = city_name
        data["name_cn"] = cms_msg["name"]
        data["name_en"] = cms_msg["name_en"]
        data["address"] = cms_msg["address"]

        # 服务器为UTC时间,比北京时间慢8小时,展示时间需+8
        if isinstance(data["query_time"], str):
            if "." in data["query_time"]:
                data["query_time"] = str(datetime.strftime(
                    datetime.strptime(data["query_time"], "%Y-%m-%d %H:%M:%S.%f"),
                    "%Y-%m-%d %H:%M:%S",
                ))

            else:
                data["query_time"] = str(datetime.strptime(
                    data["query_time"], "%Y-%m-%d %H:%M:%S"
                ))
        else:
            data["query_time"]  = str(data["query_time"])
        
        del data['_id']
        del data['created_at']

        hotel_count_key = f"{data['cms_id']}:{data['stage']}"
        if hotel_count_key not in result["hotel_count"]:
            result["hotel_count"][hotel_count_key] = {
                "count": 0,
                "data": data,
                "stage": data["stage"],
            }
        result["hotel_count"][hotel_count_key]["count"] += 1

        # 数据量过大且暂时无需求，不再返回
        # result["info"].append(data)

        user_count_key = f"{data['user_id']}"
        if not user_count_key.strip():
            continue
        if user_count_key not in result['user_count']:
            result['user_count'][user_count_key] = {
                "count": 0,
                "availability": {"count": 0, "hotel": {}},
                "preparation": {"count": 0, "hotel": {}},
                "booking": {"count": 0, "hotel": {}},
                "cancellation": {"count": 0, "hotel": {}},
            }
        if data['cms_id'] not in result['user_count'][user_count_key][data['stage']]['hotel']:
            result['user_count'][user_count_key][data['stage']]['hotel'][data['cms_id']] = 0
        result['user_count'][user_count_key][data['stage']]['hotel'][data['cms_id']] += 1
        result['user_count'][user_count_key]['count'] += 1
        result['user_count'][user_count_key][data['stage']]["count"] += 1

    return result


def save_excel(data):
    hotels = data.pop("info", [])
    hotel_count = data.pop("hotel_count", {})
    city_count = data.pop("city_count", {})
    user_count = data.pop("user_count", {})
    wb = xlwt.Workbook(encoding="utf-8")
    # info_sheet = wb.add_sheet("detail")
    city_sheet = wb.add_sheet("cityCount")
    hotel_sheet = wb.add_sheet("hotelCount")
    user_sheet = wb.add_sheet("userCount")
    # write_info_sheet(info_sheet, hotels)
    write_city_sheet(city_sheet, city_count)
    write_hotel_sheet(hotel_sheet, hotel_count)
    write_user_sheet(user_sheet, user_count)
    return wb


def write_info_sheet(info_sheet, hotels):
    for _row, msg in enumerate(hotels):
        row = _row + 1
        info_sheet.write(row, 0, msg["cms_id"])
        info_sheet.write(row, 1, msg["name_cn"])
        info_sheet.write(row, 2, msg["address"])
        info_sheet.write(row, 3, msg["city_name"])
        # 比价任务bug DATA-398 导致部分数据丢失价格信息
        info_sheet.write(row, 4, msg.get("weego_price", ""))
        info_sheet.write(row, 5, msg["checkin"])
        info_sheet.write(row, 6, msg["checkout"])
        info_sheet.write(row, 7, msg["query_time"])
        info_sheet.write(row, 8, msg["stage"])
        info_sheet.write(row, 9, msg.get("source", ''))
        info_sheet.write(row, 10, msg.get("user_ip", ''))
        info_sheet.write(row, 11, msg.get("user_id", ''))
        info_sheet.write(row, 12, msg.get("cancel_policy", ''))
        info_sheet.write(row, 13, msg.get("meal_type", ''))
        info_sheet.write(row, 14, msg.get("is_package", ''))
    info_sheet.write(0, 0, "cmsID")
    info_sheet.write(0, 1, "酒店中文名称")
    info_sheet.write(0, 2, "酒店地址")
    info_sheet.write(0, 3, "酒店所属城市")
    info_sheet.write(0, 4, "用户下单价格")
    info_sheet.write(0, 5, "入住日期")
    info_sheet.write(0, 6, "离店日期")
    info_sheet.write(0, 7, "用户查询时间")
    info_sheet.write(0, 8, "发起记录阶段")
    info_sheet.write(0, 9, "请求来源")
    info_sheet.write(0, 10, "请求发起ip")
    info_sheet.write(0, 11, "用户ID")
    info_sheet.write(0, 12, "取消政策")
    info_sheet.write(0, 13, "餐食类型")
    info_sheet.write(0, 14, "是否为套餐")


def write_city_sheet(city_sheet, data):
    data = sorted(data.items(), key=lambda x: x[1]["count"], reverse=True)
    for _row, pair in enumerate(data):
        row = _row + 1
        city_sheet.write(row, 0, pair[0].split(":")[0])
        city_sheet.write(row, 1, pair[1]["count"])
        city_sheet.write(row, 2, pair[1]["stage"])
    city_sheet.write(0, 0, "城市名称")
    city_sheet.write(0, 1, "点击次数")
    city_sheet.write(0, 2, "发起记录阶段")


def write_hotel_sheet(hotel_sheet, hotel_count):
    hotel_count = sorted(
        hotel_count.items(), key=lambda x: x[1]["count"], reverse=True
    )
    for _row, pair in enumerate(hotel_count):
        msg = pair[1]["data"]
        count = pair[1]["count"]
        stage = pair[1]["stage"]
        row = _row + 1
        hotel_sheet.write(row, 0, msg["cms_id"])
        hotel_sheet.write(row, 1, msg["name_cn"])
        hotel_sheet.write(row, 2, msg["address"])
        hotel_sheet.write(row, 3, msg["city_name"])
        hotel_sheet.write(row, 4, count)
        hotel_sheet.write(row, 5, stage)
    hotel_sheet.write(0, 0, "cmsID")
    hotel_sheet.write(0, 1, "酒店中文名称")
    hotel_sheet.write(0, 2, "酒店地址")
    hotel_sheet.write(0, 3, "酒店所属城市")
    hotel_sheet.write(0, 4, "酒店被查询次数")
    hotel_sheet.write(0, 5, "发起记录阶段")


def write_user_sheet(hotel_sheet, user_count):
    user_count = sorted(
        user_count.items(), key=lambda x: x[1]['count'], reverse=True
    )
    _row = 0
    for _, (user_id, msg) in enumerate(user_count):
        if msg['count'] <= 10:
            continue

        row = (_row + 1) * 4
        write_user_row(hotel_sheet, user_id, msg, 'availability', row - 3)
        write_user_row(hotel_sheet, user_id, msg, 'preparation', row - 2)
        write_user_row(hotel_sheet, user_id, msg, 'booking', row - 1)
        write_user_row(hotel_sheet, user_id, msg, 'cancellation', row - 0)
        _row += 1
    hotel_sheet.write(0, 0, "用户id")
    hotel_sheet.write(0, 1, "用户查询阶段")
    hotel_sheet.write(0, 2, "用户查询次数")
    hotel_sheet.write(0, 3, "用户查询最多酒店")
    hotel_sheet.write(0, 4, "用户查询最多酒店的查询次数")


def write_user_row(st, uid, msg, stage, row):
    max_query_hotel = list(sorted(
            msg[stage]['hotel'].items(), key=lambda x: x[1], reverse=True
    ))
    st.write(row, 0, uid)
    st.write(row, 1, stage)
    if not max_query_hotel:
        st.write(row, 2, "0")
        st.write(row, 3, "")
        st.write(row, 4, "")
    else:
        st.write(row, 2, msg[stage]['count'])
        st.write(row, 3, max_query_hotel[0][0])
        st.write(row, 4, max_query_hotel[0][1])
    