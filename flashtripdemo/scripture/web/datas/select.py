# coding: utf-8

import json
import xlwt
import copy
import logging
from bson import ObjectId
from datetime import datetime, timedelta
from collections import defaultdict
from itertools import chain

from . import select_v1
from .query_transformer import validate_request
from web.api.formatter_response import rest_result
from web.utils.database import databases
from web import settings

from sanic import exceptions

logger = logging.getLogger(__name__)
city_map = {}


def find_min_price(**kwargs):
    '''
    input all price_provider: price
    1st 1 for 2 or more price
    1st 0 for only one has price
    1st -1 for 0 price
    2st for provider or list(kwargs.keys())
    3st for (2nd / 1st price) - 1 or None
    '''
    all_prices = {}
    for k, v in kwargs.items():
        if not v:
            continue
        if isinstance(v, float):
            all_prices[k] = v
        else:
            try:
                all_prices[k] = float(v)
            except Exception:
                pass
    if not all_prices:
        return -1, list(kwargs.keys()), None
    prices = sorted(all_prices.items(), key=lambda x: x[1])
    if len(prices) == 1:
        return 0, prices[0][0], None  # 仅一家有价
    else:
        return 1, prices[0][0], prices[1][1] / prices[0][1] - 1


@select_v1.post("/availability")
async def availability(request):
    """
    查价任务统一查询数据接口\n
    compare中为需要比价的第三方网站\n
    目前支持ctrip 和 booking
    return {
        'status': 200,
        'data': {
            quoter_id1::hotel_id1;quoter_id2::hotel_id2:
            [
                {'checkin': {
                    'price': '', 'booking': '', 'ctrip', '', 'msg': '',
                    'type': -1/0/1
                    }
                }
            ],
            cms::cms_id
            [
                {'checkin': {
                    'price': '', 'booking': '', 'ctrip', '', 'msg': '',
                    'type': -1/0/1
                    }
                }
            ],
        }
    }
    """
    request.headers["Accept"] = "application/json"
    valid = await validate_request(request)
    if valid["errmsg"]:
        return rest_result(request, {"status": 400, "errmsg": valid["errmsg"]})
    results = []
    if valid['is_ori_price']:
        price_type = 3
    elif valid['is_without_tax']:
        price_type = 2
    else:
        price_type = 1
    to_text = valid['to_text']
    only_supplier = valid["only_supplier"]
    start_time = datetime.strptime(valid["start_time"], "%Y-%m-%d")
    end_time = datetime.strptime(valid["end_time"], "%Y-%m-%d")
    logger.info(f"valid: {valid}")
    _hotel_prices = {
        datetime.strftime(start_time + timedelta(days=i), "%Y-%m-%d"): {
            "type": -1,
            "price": "",
            "room": "",
            "supplier": "",
            "each_supplier": {},
            "updated_at": "",
        }
        for i in range((end_time - start_time).days + 1)
    }
    for uid in valid["hotels"]:
        hotel_prices = copy.deepcopy(_hotel_prices)
        hotel_prices = await get_weego_prices(uid, hotel_prices, price_type)
        for compare in valid["compare"]:
            hotel_prices = await add_compare_prices(
                compare, uid, hotel_prices, start_time, end_time
            )
        results.append({uid: hotel_prices})
    results = add_msg(results, to_text, only_supplier)
    return rest_result(request, {"status": 200, "data": results})


async def get_weego_prices(uid, hotel_prices, price_type):
    db = databases("scripture")
    for hotel in uid.split(";"):
        quoter_id, hotel_id = hotel.split("::")

        if quoter_id == 'cms':
            hotel_data = await db["statics.hotels.prices"].find_one({"hotel_id": hotel_id})
        else:
            hotel_data = await db["statics.provider.prices"].find_one(
                {"quoter_id": quoter_id, "hotel_id": hotel_id}
            )
        if not hotel_data or not hotel_data.get("prices"):
            continue
        
        for price in hotel_data['prices']:
            if price["checkin"] not in hotel_prices:
                continue
            hotel_prices[price['checkin']]['updated_at'] = price.get('updated_at', '')
            if isinstance(price["price"], (str, bool)):
                checkin_price = '当日无报价'
            else:
                if price_type == 3:
                    checkin_price = price.get('ori_price') or price['price']
                elif price_type == 2:
                    checkin_price = price.get('without_tax_price') or price['price']
                elif price_type == 1:
                    checkin_price = price['price']
                else:
                    checkin_price = "当日无报价"
                    logger.error(f"invalid price_type {price_type}")
            
            # 首次有效查价
            if not hotel_prices[price['checkin']]['price']:
                hotel_prices[price['checkin']]['price'] = checkin_price
                hotel_prices[price['checkin']]['room'] = price.get('room_type_en', '')
                if quoter_id == 'cms':
                    hotel_prices[price['checkin']]['supplier'] = price.get('supplier')
                    hotel_prices[price['checkin']]['each_supplier'].update(price.get('each_supplier', {}))
                else:
                    hotel_prices[price["checkin"]]["supplier"] = settings.SUPPLIER_ID_2_NAME[quoter_id]
                    hotel_prices[price['checkin']]['each_supplier'][settings.SUPPLIER_ID_2_NAME[quoter_id]] = price
                if checkin_price == '当日无报价':
                    hotel_prices[price['checkin']]['type'] = 0
                else:
                    hotel_prices[price['checkin']]['type'] = 1
            # 存在有效价格但无报价
            elif hotel_prices[price['checkin']]['price'] == '当日无报价':
                # 此次有报价
                if checkin_price != '当日无报价':
                    hotel_prices[price['checkin']]['price'] = checkin_price
                    hotel_prices[price['checkin']]['room'] = price.get('room_type_en', '')
                    hotel_prices[price['checkin']]['type'] = 1
                    if quoter_id == 'cms':
                        hotel_prices[price['checkin']]['supplier'] = price.get('supplier')
                        hotel_prices[price['checkin']]['each_supplier'].update(price.get('each_supplier', {}))
                    else:
                        hotel_prices[price["checkin"]]["supplier"] = settings.SUPPLIER_ID_2_NAME[quoter_id]
                        hotel_prices[price['checkin']]['each_supplier'][settings.SUPPLIER_ID_2_NAME[quoter_id]] = price
                # 此次也无报价
                else:
                    if quoter_id == 'cms':
                        hotel_prices[price['checkin']]['each_supplier'].update(price.get('each_supplier', {}))
                    else:
                        hotel_prices[price["checkin"]]["supplier"] = settings.SUPPLIER_ID_2_NAME[quoter_id]
                        hotel_prices[price['checkin']]['each_supplier'][settings.SUPPLIER_ID_2_NAME[quoter_id]] = price
            # 存在有效价格且有报价
            else:
                # 此次有报价且小于历史价格
                if checkin_price != '当日无报价' and checkin_price < hotel_prices[price['checkin']]['price']:
                    hotel_prices[price['checkin']]['price'] = checkin_price
                    hotel_prices[price['checkin']]['room'] = price.get('room_type_en', '')
                    if quoter_id == 'cms':
                        hotel_prices[price['checkin']]['supplier'] = price.get('supplier')
                        hotel_prices[price['checkin']]['each_supplier'].update(price.get('each_supplier', {}))
                    else:
                        hotel_prices[price["checkin"]]["supplier"] = settings.SUPPLIER_ID_2_NAME[quoter_id]
                        hotel_prices[price['checkin']]['each_supplier'][settings.SUPPLIER_ID_2_NAME[quoter_id]] = price
                # 此次有报价但非最低价格
                elif checkin_price != '当日无报价':
                    if quoter_id == 'cms':
                        hotel_prices[price['checkin']]['each_supplier'].update(price.get('each_supplier', {}))
                    else:
                        hotel_prices[price['checkin']]['each_supplier'][settings.SUPPLIER_ID_2_NAME[quoter_id]] = price
    return hotel_prices


async def add_compare_prices(compare, uid, hotel_prices, start_time, end_time):
    """
    """
    db = databases("scripture")
    coll = f"statics.{compare}.prices"
    for hotel in uid.split(";"):
        quoter_id, hotel_id = hotel.split('::')
        hotel = f"{hotel_id}::{quoter_id}"
        hotel_data = await db[coll].find_one({"cms_id": hotel})
        if not hotel_data:
            hotel_data = {}
        compare_prices = {
            price["checkin"]: price
            for price in hotel_data.get("min_price", []) or hotel_data.get('prices', [])
            if price and isinstance(price, dict) and start_time
            <= datetime.strptime(price["checkin"], "%Y-%m-%d")
            <= end_time
        }
        for checkin in hotel_prices.keys():
            if checkin not in compare_prices:
                hotel_prices[checkin][compare] = ''
                continue
            hotel_prices[checkin][compare] = compare_prices.get(checkin, {}).get('price', '')
            hotel_prices[checkin][f"{compare}_room"] = compare_prices.get(checkin, {}).get('room_type', '') or compare_prices.get(checkin, {}).get('room_type_cn', '')
    return hotel_prices

        

def add_msg(results, to_text, only_supplier):
    '''
    `results` :
    [
        {
            uid: {
                checkin: {
                    type: -1/0/1,
                    price: float/str/bool,
                    room: str,
                    supplier: str,
                    each_supplier: {},
                    booking: float/str/bool,
                    booking_room: str,
                    ctrip: float/str/bool,
                    ctrip_room: str
                }
            }
        }
    ]\n
    return :
    {
        uid:
            [
                {'checkin': {
                    'price': '',
                    'booking': '',
                    'ctrip', '',
                    'msg': '',
                    'supplier': '',
                    'rate': '',
                    'lowest': '',
                    'type': -1/0/1,
                    'checkin': 'YYYY-mm-dd'
                    }
                }
            ]
        }
    }
    '''
    result = {}
    for _hotel_dict in results:
        uid = list(_hotel_dict.keys())[0]
        hotel_dict = _hotel_dict[uid]
        prices = []
        for checkin, data in hotel_dict.items():
            price_args = {}
            key_set = list(data.keys())
            supplier = data.get('supplier', '')
            if supplier:
                supplier = settings.SUPPLIER_ID_2_NAME.get(supplier, supplier.lower())
            else:
                supplier = ''
            if only_supplier:
                if supplier in only_supplier:
                    price_args[supplier] = data['price']
            else:
                price_args['weego'] = data['price']
            if to_text:
                msg = f"入住日期: {checkin}\nweego: {data['price']}\nweego房型: {data['room']}\nweego最低价供应商: {settings.SUPPLIER_ID_2_NAME.get(supplier, supplier)}\n\n"
            data.pop('room', '')
            if len(data['each_supplier'].keys()) >= 1:
                for quoter_id, _data in data['each_supplier'].items():
                    provider = settings.SUPPLIER_ID_2_NAME.get(quoter_id, quoter_id).lower()
                    if only_supplier and provider in only_supplier:
                        price_args[provider] = _data.get('price')
                    if provider.lower() == supplier.lower():
                        continue
                    if to_text:
                        msg += f"{provider}: {_data.get('price')}\n{provider}房型: {_data.get('room_type_en', '')}\n\n"
            data.pop('each_supplier', '')
            for key in key_set:
                if not '_room' in key:
                    continue
                compare = key.split('_')[0]
                price_args[compare] = data.get(compare, '当日无报价')
                if to_text:
                    msg += f"{compare}: {data.get(compare, '当日无报价')}\n{compare}房型: {data.get(key, '')}\n\n"
                data.pop(key, '')
            if to_text:
                data['msg'] = msg.strip()
            data['checkin'] = checkin
            price_flag, providers, rate = find_min_price(**price_args)
            if price_flag == 1:
                data['lowest'] = providers
                data['rate'] = rate
            data['checkin'] = checkin
            if only_supplier:
                data.update(price_args)
            prices.append(data)
        result[uid] = prices
    return result
