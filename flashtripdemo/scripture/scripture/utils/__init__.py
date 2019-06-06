# coding: utf8

import logging
import requests
from datetime import datetime, timedelta

from .pool import Pool
from .html import strip_tags
from .proxy import refresh_ip
from .split import split

from scripture.settings import PRICES_DING_TOKEN

__all__ = ['strip_tags', 'refresh_ip', 'Pool', 'split']

Ding_params = {"access_token": PRICES_DING_TOKEN}


def price_compare_check(data, created_at, item):
    logger = logging.getLogger(__name__)
    weego_price = data.get("weego_price")
    compair_prices = data.get("prices")
    compair_price = [
        e["price"] for e in compair_prices if e["compair"] == "booking"
    ] or data.get("compair_price")
    if compair_price and isinstance(compair_price, list):
        compair_price = compair_price[0]
    if weego_price == "当日无报价":
        return item
    query_time = data["query_time"]
    if isinstance(query_time, str):
        query_time = datetime.strptime(str(query_time)[:10], "%Y-%m-%d")
    if (
        query_time > created_at + timedelta(days=-7)
        and compair_price
        and isinstance(compair_price, (float, int))
        and weego_price
    ):
        try:
            weego_price = float(weego_price)
        except Exception as exc:
            logger.error(
                f"invalid weego_price: {weego_price}!", exc_info=exc
            )
            return item
        logger.info(f"compair_price: {compair_price}, weego_price: {weego_price}")
        if compair_price / weego_price > 1.2:
            compair_with = ""
            for third in data["prices"]:
                compair_with += f"""- {third['compair']} 价格: {third['price']}; 房型: {third['room_type']}
- 链接: {third['url']}
"""
            text = f"""# 有用户在 {data['stage']} 时我方价格存在上调空间 \n
- 入住日期: {data['checkin']}
- 离店日期: {data['checkout'].strip()}
- 酒店名称: {data.get('hotel_name').strip()}
{compair_with.rstrip()}
- 我方价格： {weego_price}; 房型： {data['weego_room_type']}
- cms链接: http://wop.feifanweige.com/admin/hotels/{data['cms_id']}
- H5链接: https://www.flashtrip.cn/hotels/{data['cms_id']}"""
            btns = [
                {
                    "title": f"{third['compair']}酒店链接",
                    "actionURL": third["url"],
                }
                for third in data["prices"]
            ]
            btns.extend(
                [
                    {
                        "title": "cms酒店链接",
                        "actionURL": f"http://wop.feifanweige.com/admin/hotels/{data['cms_id']}",
                    },
                    {
                        "title": "H5酒店链接",
                        "actionURL": f"https://www.flashtrip.cn/hotels/{data['cms_id']}",
                    },
                ]
            )
            payload = {
                "msgtype": "actionCard",
                "actionCard": {
                    "title": f"有用户在 {data['stage']} 时我方价格存在上调空间",
                    "text": text,
                    "btns": btns,
                },
            }
            resp = requests.post(
                "https://oapi.dingtalk.com/robot/send",
                params=Ding_params,
                json=payload,
            )

    return item