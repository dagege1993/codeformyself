# coding: utf-8
import logging, re, copy
import json
from scripture.utils import parse_element as pe
from scripture.xpath import bookings_v2 as bk


def parser_booking_price(response):
    url = response.url
    prices_tr_list = response.xpath(bk.PRICES_TABLE_TR)
    logger = logging.getLogger(__name__)
    prices = {}
    min_price = {}
    prices['prices'] = []
    for index, tr in enumerate(prices_tr_list):
        if tr.xpath('.' + bk.ROOM_TYPE):
            room_type = tr.xpath(
                '.' + bk.ROOM_TYPE).extract_first().strip()
            if index == 0 and not room_type:
                logger.error(f'网页[{url}]解析规则变更')
                break
        price = tr.xpath('.' + bk.ROOM_PRICE).extract_first()
        if price:
            price = pe.find_price(url, price)
            price_tax_div = tr.xpath(
                '.' + bk.ROOM_PRICE_TAX).extract_first()
            if price_tax_div:
                tax_price = pe.find_price(url, price_tax_div)
                if tax_price:
                    price += tax_price
            policies = pe.get_policies(
                tr.xpath('.' + bk.ROOM_POLICIES).extract())
            occupancy = tr.xpath(
                '.' + bk.ROOM_OCCUPANCY).extract_first().strip()
            one_room_price = {
                'occupancy': occupancy,
                'room_type': room_type,
                'price': price,
                'policies': policies,
            }
            if index == 0:
                min_price = copy.copy(one_room_price)
            prices['prices'].append(one_room_price)
        else:
            policies = tr.xpath('.' + bk.ROOM_SOLD_OUT).extract_first()
            if not policies:
                continue
            price = pe.find_price(url, policies.strip())
            occupancy = tr.xpath(
                '.' + bk.ROOM_OCCUPANCY).extract_first().strip()
            sold_room_price = {
                'occupancy': occupancy,
                'room_type': room_type,
                'price': price,
                'policies': policies,
            }
            prices['prices'].append(sold_room_price)
    return prices, min_price


def ctrip_min_price(response):
    ori_json = response.xpath('*//input[@class="model_data"]/@data-roomlistinfo').extract()
    if len(ori_json) == 0:
        return '0', '当日无报价', '0', '0'
    data = json.loads(ori_json[0])
    rooms = data['rooms']
    # 根据列表里的字典里的字典的某个值排序
    sorted_rooms = sorted(rooms, key=lambda e: e.__getitem__('priceInfo').get('cnyTotalPrice'))
    if len(sorted_rooms) == 0:
        return '0', '当日无报价', '0', '0'
    return_room = sorted_rooms[0]
    roomid = return_room.get('id', '')
    shadowid = return_room.get('shadowId', '')
    bookChangeCheck = return_room.get('bookChangeCheck')
    ceckid = return_room.get('ceckid')
    return roomid, shadowid, bookChangeCheck, ceckid


def analysis_two_level_response(response):
    """
    解析携程网二级页面的房间名称和价格
    :param response: 房间名称和价格
    :return:
    """
    min_name = re.findall('"roomName":"(.*?)"', response.text)
    if len(min_name) > 0:
        min_name = min_name[0]
    else:
        min_name = 'Unknown'
    min_price = re.findall('"price":(\d+)', response.text)
    if len(min_price) > 0:
        min_price = float(min_price[0])
    else:
        min_price = '当日无报价'
    return min_name, min_price


def get_extra_info(url_dict):
    if isinstance(url_dict, dict):
        adult = url_dict.get('adult', '2')  # 默认两个大人
        rcount = url_dict.get('rcount', '1')  # 预订房间数,默认为1
        childAges = url_dict.get('childAges', '-1,-1,-1')  # 默认没有小孩
        isoversea = url_dict.get('isoversea')
        if isoversea:
            isoversea = 'H5overseas'
        else:
            isoversea = 'H5Domestic'

    else:
        adult = '2'
        rcount = '1'
        childAges = '-1,-1,-1'
        isoversea = 'H5overseas'
    return adult, rcount, childAges, isoversea
