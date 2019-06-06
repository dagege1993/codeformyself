# -*- coding: utf-8 -*-
import json
import re
import logging
import copy
import time

import math

import requests
import scrapy
from yarl import URL
from scrapy.http import Request
from scrapy_redis.spiders import RedisSpider
from datetime import datetime, timedelta
from scrapy.loader import ItemLoader

from scripture.models import Hotels
from scripture.models.booking import Booking
from scripture.models.redis_spider import DistributedSpiderModels, MatchPrice, CTripPrice, TripAdvisor
from scripture.xpath import bookings_v2 as bk
from scripture.xpath import hotels as hotels_xp
from scripture.xpath import tripadvisor_hotel as tripadvisor_xp
from scripture.utils.html import take_first, service_to_dict
from scripture.utils import parse_element as pe
from scripture import settings
from scripture.utils.parser import parser_booking_price, ctrip_min_price, analysis_two_level_response, get_extra_info
from web.api.tripadvisor import parser_commits

logger = logging.getLogger(__name__)
useless_facilities = ["咖啡美味！", "不允许携带宠物入住。", "水果", "（额外付费）", "宠物", "免费！"]
max_retry_times = 2
lost_city_or_country = []
city_max_hotel_num = []


class DistributedSpider(RedisSpider):
    name = 'distributed_spider'
    allowed_domains = ['www.booking.com', 'www.hotels.cn', 'www.hotels.com']
    redis_key = 'distributed_spider'

    site_prefix = {
        'cn': 'CN',
        'com': 'EN'
    }

    custom_settings = {
        # 重试机制
        "RETRY_ENABLED": True,
        "HTTPERROR_ALLOWED_CODES": [403, 404],
        'DOWNLOAD_TIMEOUT': 20,  # 设置超时时间默认是180秒
        "RETRY_TIMES": 5, }

    def make_requests_from_url(self, url):
        url_dict = json.loads(url)
        spider_name = url_dict.get('spider_name')

        if spider_name == 'booking_prices':
            return self.make_bk_prices_first_request(url_dict)
        elif spider_name == 'ctrip_prices':
            return self.make_ctrip_prices(url_dict)
        elif spider_name == 'hcom_page':
            return Request(
                url_dict.get('base_url'),
                meta={
                    'spider_name': spider_name
                },
                callback=self.hcom_parse
            )
        elif spider_name == 'booking_page':
            return Request(
                url_dict.get('base_url'),
                meta={
                    'spider_name': spider_name
                },
                callback=self.booking_parse
            )
        elif spider_name == 'compair':
            return self.start_compair(url_dict)
        elif spider_name == 'tripadvisor':

            return self.start_tripadvisor(url_dict)

    def start_compair(self, url_dict):
        websites = url_dict.get('websites', {})
        compair = url_dict.get('compair', {})
        if websites:
            next_url = websites.popitem()[1]

            # 历史数据兼容
            if 'ctrip' in next_url and 'atime' in next_url:
                _url = URL(next_url)
                cid = _url.path.split('/')[-1]
                checkin = datetime.strptime(_url.query['atime'], '%Y%m%d')
                checkout = checkin + timedelta(days=int(_url.query['days']))
                _url = URL(
                    f"http://m.ctrip.com/webapp/hotel/j/hoteldetail/dianping/rooms/{cid}"
                ).with_query(
                    {
                        'inday': checkin.strftime('%Y/%m/%d'),
                        'outday': checkout.strftime('%Y/%m/%d'),
                        'subchannel': '',
                        'hotelchannel': '1',
                        'isoversea': '1'
                    }
                )
                next_url = str(_url)
            return Request(
                next_url,
                meta={
                    'retry': 0,
                    'websites': websites,
                    'compair': compair,
                },
                callback=self.check_response,
                dont_filter=True,
            )

    def check_response(self, response):
        if len(response.text) == 0 and response.status == 200 and response.meta["retry"] < max_retry_times:
            response.meta["retry"] += 1
            yield Request(
                response.url,
                meta=response.meta,
                callback=self.check_response,
                dont_filter=True,
            )
        else:
            yield from self.compair_parser(response)

    def compair_parser(self, response):
        # 默认是在第一级页面就能获取到response
        twp_level_response = 0
        url = response.url
        meta = response.meta
        websites = meta.get('websites')
        adult, rcount, childAges, isoversea = get_extra_info(websites)  # 传过来的参数做解析

        if 'roomid' in url:
            room_type, price = analysis_two_level_response(response)
            compair = 'ctrip'
        elif 'ctrip' in url:
            _url = URL(url)
            query = _url.query
            atime = query['inday'].replace('/', '')
            checkout = datetime.strptime(query['outday'], '%Y/%m/%d')
            checkin = datetime.strptime(atime, '%Y%m%d')
            ###################################
            # 这里开始更新
            hotelid = re.findall('(\d+).html', response.url)[0]  # 从上一个请求的URL中获取hotelid
            roomid, shadowid, bookChangeCheck, ceckid = ctrip_min_price(response)
            if roomid != '0':  # 房间ID!=0
                querystring = {"frflag": "detail", "paytype": "0", "rateid": "", "isMorning": "false"}
                querystring['sct'] = isoversea
                querystring['rcount'] = rcount
                querystring['childAges'] = childAges
                querystring['adult'] = adult
                querystring['roomid'] = roomid
                querystring['ceckid'] = ceckid
                querystring['shadowid'] = shadowid
                querystring['indate'] = checkin.strftime('%Y/%m/%d')
                querystring['outdate'] = checkout.strftime('%Y/%m/%d')
                querystring['hotelid'] = hotelid
                querystring.update(bookChangeCheck)
                url = "http://m.ctrip.com/webapp/hotel/booking"
                _url = URL(url)
                url = str(_url.with_query(querystring))
                websites['crip_two_level'] = url

                # 这里应该直接返回给下一次调用了
                meta['websites'] = websites
                response.meta["retry"] = 0
                twp_level_response = 1  # 表示第二次页面才能获取到要的结果,不进入payload填充
            if roomid == '0':
                price = '当日无报价'
                room_type = 'Unknonwn'
                url = response.url
                compair = 'compair'

        elif 'booking' in url:
            _, _price = parser_booking_price(response)
            room_type = _price.get('room_type', 'Unknonwn')
            price = _price.get('price', '当日无报价')
            compair = 'booking'
        else:
            logger.error(f"invalid website! {url}")
            room_type = 'Unknonwn website'
            price = 'Unknonwn website'
            compair = 'Unknonwn website'
        if twp_level_response == 0:  # 默认在一级页面获取response

            payload = {
                'price': price,
                'room_type': room_type,
                'url': url,
                'compair': compair
            }
            meta = response.meta
            p_min_price = meta.get('min_price', False)
            if not p_min_price or (price != '当日无报价' and (not p_min_price or float(price) < p_min_price)):
                meta['min_compair'] = compair
                try:
                    meta['min_price'] = float(price)
                except ValueError:
                    meta['min_price'] = ''
                meta['min_room_type'] = room_type
                meta['url'] = url
            prices = meta.get('prices', [])
            prices.append(payload)
            meta['prices'] = prices
            websites = meta.get('websites')
        if not websites:
            loader = ItemLoader(item=MatchPrice(), response=response)
            compair = meta['compair']
            is_package = compair.get('is_package', False)
            if is_package:
                total_price = float(compair['weego_price'])
            else:
                checkin = datetime.strptime(compair['checkin'], '%Y-%m-%d')
                checkout = datetime.strptime(compair['checkout'], '%Y-%m-%d')
                try:
                    # 由于查价也会发起比价，所以可能传入无报价的情况
                    # 直接传入总价
                    total_price = float(compair['weego_price'])
                except ValueError:
                    total_price = "当日无报价"
            loader.add_value('spider_name', 'compair')
            loader.add_value('stage', compair['stage'])
            loader.add_value('weego_price', total_price)
            loader.add_value('weego_room_type', compair['weego_room_type'])
            loader.add_value('checkin', compair['checkin'])
            loader.add_value('checkout', compair['checkout'])
            loader.add_value('cms_id', compair['cms_id'])
            loader.add_value('query_time', compair['query_time'])
            loader.add_value('compair', meta['min_compair'])
            loader.add_value('compair_price', meta['min_price'])
            loader.add_value('compair_room_type', meta['min_room_type'])
            loader.add_value('prices', meta['prices'])
            loader.add_value('url', meta['url'])
            loader.add_value('meal_type', compair.get('meal_type', 'null'))
            loader.add_value('hotel_name', compair.get('hotel_name', ''))
            loader.add_value('user_id', compair.get('user_id', ''))
            loader.add_value('cancel_policy', compair.get('cancel_policy', ''))
            loader.add_value('source', compair.get('source', ''))
            loader.add_value('user_ip', compair.get('user_ip', ''))
            loader.add_value('source_type', compair.get('source_type', ''))
            loader.add_value('voucher', compair.get('voucher', ''))
            loader.add_value('detail_status_code', compair.get('detail_status_code', ''))
            loader.add_value('is_package', is_package)
            loader.add_value("uid", compair.get("uid", ''))
            yield loader.load_item()
        else:
            next_url = websites.popitem()[1]
            meta['websites'] = websites
            response.meta["retry"] = 0
            yield Request(
                next_url,
                meta=meta,
                callback=self.check_response,
                dont_filter=True,
            )

    def make_bk_prices_first_request(self, url_dict):
        base_url = url_dict.get('base_url')
        _url = URL(base_url)
        cms_id = url_dict.get('cms_id')
        start_time = url_dict.get('start_time')
        days = int(url_dict.get('days'))
        checkin = datetime.strptime(start_time, '%Y-%m-%d')
        checkout_str = url_dict.get('compair', {}).get('checkout', '') or (
                checkin + timedelta(days=1)).strftime('%Y-%m-%d')
        url = _url.with_query({
            'checkin_year': start_time[:4],
            'checkin_month': start_time[5:7],
            'checkin_monthday': start_time[8:],
            'checkout_year': checkout_str[:4],
            'checkout_month': checkout_str[5:7],
            'checkout_monthday': checkout_str[8:],
        })
        _meta = {
            'spider_name': url_dict.get('spider_name'),
            'base_url': base_url,
            'start_time': start_time,
            'days': days,
            'cms_id': cms_id,
        }
        return Request(
            str(url),
            meta={
                '_meta': _meta,
                'checkin_str': start_time,
                'compair': url_dict.get('compair', False)
            },
            callback=self.parse_prices,
            dont_filter=True,
        )

    def parse_prices(self, response):
        logger.info(f"response.meta : {response.meta}")
        _meta = response.meta['_meta']
        _base_url = URL(_meta['base_url'])
        start_time = datetime.strptime(_meta['start_time'], '%Y-%m-%d')
        days = int(_meta['days'])
        spider_name = _meta['spider_name']
        cms_id = _meta['cms_id']
        checkin_str = response.meta['checkin_str']
        checkin = datetime.strptime(checkin_str, '%Y-%m-%d')
        url = response.url
        prices_tr_list = response.xpath(bk.PRICES_TABLE_TR)
        if len(prices_tr_list) == 0:
            if response.xpath(bk.PRICES_FROM):
                yield Request(
                    url,
                    meta={
                        '_meta': _meta,
                        'checkin_str': checkin_str,
                    },
                    callback=self.parse_prices,
                    dont_filter=True,
                )
            if settings.DOWNLOAD_HTML:
                with open(
                        f'logs/scripture/{datetime.now().timestamp()}.html',
                        'w') as f:
                    f.write(response.text)
            logger.info(f'booking[{url}]没有查询到报价')
        else:
            prices, min_price = parser_booking_price(response)
            prices['checkin'] = checkin_str
            min_price['checkin'] = checkin_str
            min_price['updated_at'] = datetime.now()
            loader = ItemLoader(
                item=DistributedSpiderModels(), response=response)
            loader.add_value('prices', prices)
            loader.add_value('min_price', min_price)
            loader.add_value('cms_id', cms_id)
            loader.add_value('spider_name', spider_name)
            loader.add_value('url', str(_base_url))

            yield loader.load_item()

        if checkin < start_time + timedelta(days=days - 1):
            checkin = checkin + timedelta(days=1)
            checkin_str = checkin.strftime('%Y-%m-%d')
            checkout_str = (checkin + timedelta(days=1)).strftime('%Y-%m-%d')
            next_url = _base_url.with_query({
                'checkin_year': checkin_str[:4],
                'checkin_month': checkin_str[5:7],
                'checkin_monthday': checkin_str[8:],
                'checkout_year': checkout_str[:4],
                'checkout_month': checkout_str[5:7],
                'checkout_monthday': checkout_str[8:],
            })
            yield Request(
                str(next_url),
                meta={
                    '_meta': _meta,
                    'checkin_str': checkin_str,
                },
                callback=self.parse_prices,
                dont_filter=True,
            )

    def make_ctrip_prices(self, url_dict):
        base_url = url_dict.get('base_url')
        adult, rcount, childAges, isoversea = get_extra_info(url_dict)
        _url = URL(base_url)
        cms_id = url_dict.get('cms_id')
        start_time = url_dict.get('start_time')
        days = int(url_dict.get('days'))
        checkin = datetime.strptime(start_time, '%Y-%m-%d')
        checkout = checkin + timedelta(days=1)
        url = _url.with_query({
            'inday': checkin.strftime('%Y/%m/%d'),
            'outday': checkout.strftime('%Y/%m/%d'),
            'subchannel': '',
            'hotelchannel': '1',
            'isoversea': '1'
        })
        _meta = {
            'spider_name': url_dict.get('spider_name'),
            'base_url': base_url,
            'inday': checkin,
            'outday': checkout,
            'days': days,
            'cms_id': cms_id,
            'adult': adult,
            'rcount': rcount,
            'childAges': childAges,
            'isoversea': isoversea,
        }
        return Request(
            str(url),  # 这个url请求的就是那段ul信息
            meta={
                '_meta': _meta,
                'compair': url_dict.get('compair', False)
            },
            callback=self.parse_ctrip_prices,
            dont_filter=True,
        )

    def parse_ctrip_prices(self, response):
        logger.info(f"response.meta : {response.meta}")
        _meta = response.meta['_meta']
        _base_url = URL(_meta['base_url'])
        checkin = _meta['inday']
        checkout = _meta['outday']
        days = int(_meta['days']) - 1
        spider_name = _meta['spider_name']
        cms_id = _meta['cms_id']
        prices = {}
        prices['checkin'] = checkin.strftime('%Y-%m-%d')
        prices['updated_at'] = datetime.now()

        # 从这里开始更新
        hotelid = re.findall('(\d+).html', response.url)[0]  # 从上一个请求的URL中获取hotelid
        roomid, shadowid, bookChangeCheck, ceckid = ctrip_min_price(response)
        # 如果解析出来是异常值,直接返回
        if roomid == '0':
            price = '当日无报价'
            room_type = 'Unknonwn'
            prices['price'] = price
            prices['room_type_cn'] = room_type
            loader = ItemLoader(
                item=CTripPrice(), response=response)
            loader.add_value('prices', prices)
            loader.add_value('cms_id', cms_id)
            loader.add_value('spider_name', spider_name)
            loader.add_value('url', str(_base_url))
            yield loader.load_item()

            if days > 0:
                checkin = checkout
                checkout = checkout + timedelta(days=1)
                next_url = _base_url.with_query({
                    'inday': checkin.strftime('%Y/%m/%d'),
                    'outday': checkout.strftime('%Y/%m/%d'),
                    'subchannel': '',
                    'hotelchannel': '1',
                    'isoversea': '1'
                })
                _meta['days'] = days
                _meta['inday'] = checkin
                _meta['outday'] = checkout
                yield Request(
                    str(next_url),
                    meta={
                        '_meta': _meta,
                    },
                    callback=self.parse_ctrip_prices,
                    dont_filter=True,
                )
        if roomid != '0':
            querystring = {"frflag": "detail", "paytype": "0", "rateid": "", "isMorning": "false"}
            querystring['sct'] = _meta.get('isoversea')
            querystring['childAges'] = _meta.get('childAges')
            querystring['adult'] = _meta.get('adult')
            querystring['rcount'] = _meta.get('rcount')
            querystring['roomid'] = roomid
            querystring['shadowid'] = shadowid
            querystring['indate'] = checkin.strftime('%Y/%m/%d')
            querystring['outdate'] = checkout.strftime('%Y/%m/%d')
            querystring['hotelid'] = hotelid
            querystring.update(bookChangeCheck)
            url = "http://m.ctrip.com/webapp/hotel/booking"
            _url = URL(url)
            url = _url.with_query(querystring)
            yield Request(
                str(url), callback=self.parse_crip_two_level_price,
                dont_filter=True,
                meta={"prices": prices, "checkout": checkout,
                      "days": days,
                      "spider_name": spider_name,
                      "cms_id": cms_id,
                      '_meta': _meta,
                      "_base_url": _base_url,
                      }
            )

    def parse_crip_two_level_price(self, response):

        meta = response.meta
        logger.info(f"response.meta : {response.meta}")
        _base_url = meta['_base_url']
        _meta = meta['_meta']
        prices = meta['prices']
        checkout = meta['checkout']
        days = meta['days']
        spider_name = meta['spider_name']
        cms_id = meta['cms_id']
        name, price = analysis_two_level_response(response)
        ##################################################################################
        if not price:
            prices['price'] = '当日无报价'
        else:
            prices['price'] = price
            prices['room_type_cn'] = name
        loader = ItemLoader(
            item=CTripPrice(), response=response)
        loader.add_value('prices', prices)
        loader.add_value('cms_id', cms_id)
        loader.add_value('spider_name', spider_name)
        loader.add_value('url', str(_base_url))
        yield loader.load_item()

        if days > 0:
            checkin = checkout
            checkout = checkout + timedelta(days=1)
            next_url = _base_url.with_query({
                'inday': checkin.strftime('%Y/%m/%d'),
                'outday': checkout.strftime('%Y/%m/%d'),
                'subchannel': '',
                'hotelchannel': '1',
                'isoversea': '1'
            })
            _meta['days'] = days
            _meta['inday'] = checkin
            _meta['outday'] = checkout
            yield Request(
                str(next_url),
                meta={
                    '_meta': _meta,
                },
                callback=self.parse_ctrip_prices,
                dont_filter=True,
            )

    def hcom_parse(self, response):
        spider_name = response.meta['spider_name']
        title = response.xpath(hotels_xp.TITLE).extract_first()
        if title == "好订网酒店预订 国际酒店预订 特价国外酒店预订 – 网上订酒店就到Hotels.cn":
            self.logger.debug('Drop response(%s)', response.url)
            return
        loader = ItemLoader(item=Hotels(), response=response)
        url = URL(response.url)
        hotels_id = url.path.strip('/').split('/')[0][2:]
        PREFIX = self.site_prefix.get(url.host.split('.')[-1])
        if PREFIX == 'CN':
            en_url = url.with_host('www.hotels.com') \
                .with_query({'pos': 'HCOM_US', 'locale': 'en_US'})
            en_url = str(en_url)
            loader.add_value('url', response.url)
            loader.add_value('us_url', en_url)
            loader.add_xpath('address_text', hotels_xp.ADDRESS)
        else:
            loader.add_xpath('address_text', hotels_xp.EN_ADDRESS)
        loader.add_value('hotels_id', hotels_id)
        loader.add_value('title', title)
        loader.add_xpath('name', hotels_xp.NAME)
        position = take_first(response, hotels_xp.POSITION)
        latitude, longitude = position.split(',')
        loader.add_value('latitude', latitude)
        loader.add_xpath('longitude', longitude)
        loader.add_xpath('star', hotels_xp.STAR, re='(\d+)')
        loader.add_value('address', pe._address(response))
        loader.add_xpath('price', hotels_xp.PRICE)
        loader.add_xpath('city', hotels_xp.ADDRESS_LOCALITY)
        loader.add_xpath('country', hotels_xp.ADDRESS_COUNTRY)
        loader.add_xpath('telephone', hotels_xp.TELEPHONE)
        loader.add_xpath('landmarks', hotels_xp.LANDMARKS)
        loader.add_xpath('traffic_tips', hotels_xp.TRAFFIC_TIPS)
        loader.add_value('notice', pe._notice(response, PREFIX))
        IN_STORE_SERVICES = getattr(
            hotels_xp,
            PREFIX + '_IN_STORE_SERVICE_FACT'
        )
        loader.add_value(
            'in_store_service_facilities',
            service_to_dict(response.xpath(IN_STORE_SERVICES), hotels_xp)
        )
        ROOM_SERVICES = getattr(hotels_xp, PREFIX + '_ROOM_SERVICE_FACT')
        loader.add_value(
            'room_service_facilities',
            service_to_dict(response.xpath(ROOM_SERVICES), hotels_xp)
        )
        loader.add_xpath('around', hotels_xp.AROUND)
        pictures = pe._pictures(response.xpath(hotels_xp.PICTURES))
        loader.add_value('pictures', pictures)
        loader.add_xpath('short_introduction', hotels_xp.SHORT_INTRODUCTION)
        loader.add_xpath('amenities', hotels_xp.AMENITIES)
        loader.add_xpath('for_families', hotels_xp.FOR_FAMILIES)
        loader.add_value('locale', PREFIX.lower())
        loader.add_value('summary', pe._summary(response))
        loader.add_value('spider_name', spider_name)
        parse_result = loader.load_item()
        parse_dict = dict(parse_result)
        parse_info = [k for k, v in parse_dict.items() if not v or v == ['']]
        if parse_info:
            logger.warning(f'[{hotels_id}]数据解析完成,其中空字段为{parse_info}')
        yield parse_result

    def booking_parse(self, response):
        spider_name = response.meta['spider_name']
        loader = ItemLoader(item=Booking(), response=response)
        url = response.url
        rooms = []
        rooms_base_node = response.xpath(bk.ROOMS_BASE_NODE)[0]
        info_pages = rooms_base_node.xpath(bk.INFO_PAGES)
        order_pages = rooms_base_node.xpath(bk.ORDER_PAGES)
        names_en = response.xpath(bk.NAMES_EN).extract()
        names_cn = [
            name.strip()
            for name in response.xpath(bk.NAMES_CN).extract()
            if name.strip() != ""
        ]
        for i in range(len(info_pages)):
            room = {}
            info_node = info_pages[i]
            order_node = order_pages[i]
            room["bed_size"] = ""
            room["add_bed_type"] = []
            room["useful"] = ""
            room["serve"] = ""
            room["network"] = ""
            room["recreation"] = ""
            room["dining"] = ""
            room["room_type_en"] = names_en[i].strip()
            room["room_type"] = names_cn[i]

            room["gallery"] = [
                {"image_url": url}
                for url in info_node.xpath(bk.ROOM_IMAGE).extract()
            ]
            room["room_size"] = " ".join(
                [
                    info.strip()
                    for info in info_node.xpath(
                    bk.ROOM_SIZE
                ).extract()
                    if info.strip() != ""
                ]
            )
            if order_node.xpath(bk.ROOM_OCCUPANCY_INFO):
                room["occupancy_info"] = order_node.xpath(
                    bk.ROOM_OCCUPANCY_INFO
                ).extract_first().strip()
            else:
                room["occupancy_info"] = ""
            if order_node.xpath(bk.ROOM_BED_TYPE):
                room["bed_type"] = pe.remove_line_break(
                    order_node.xpath(
                        bk.ROOM_BED_TYPE
                    ).xpath('string(.)').extract_first()
                )
            else:
                room["bed_type"] = ""
            ori_room_desc = "".join(info_node.xpath(bk.ROOM_DESC).extract())
            room["room_desc"] = (
                pe.remove_line_break(
                    re.sub("我们网站上仅剩\d+间空房！", "", ori_room_desc)
                        .replace("刚刚有人订过", "")
                        .replace("选择床型：", "可选床型：")
                        .replace("•", "")
                )
                    .replace("\n和\n", "和")
                    .replace("\n和\n", "和")
                    .replace("-\n", "")
                    .replace("\n平方米", "平方米")
                    .split("其他设施包括")[0]
            )
            room["facilities"] = [
                {"facility": detail.replace("• ", "").strip()}
                for detail in info_node.xpath(
                    bk.ROOM_FACILITIES
                ).extract()
            ]
            rooms.append(room)
        introduction = pe.remove_line_break(
            response.xpath(bk.INTRODUCTION).xpath("string(.)").extract()
        ).replace("位置超赞\n-\n查看地图\n", "")
        polices = pe.find_polices(response)
        attractions = [
            {
                "name": pe.remove_line_break(landmark.xpath("string(.)").extract()).split("\n")[
                    0
                ],
                "distance": pe.remove_line_break(landmark.xpath("string(.)").extract())
                    .split("\n")[-1]
                    .replace("km", "公里"),
            }
            for landmark in response.xpath(bk.LANDMARKS)
        ]
        main_facilities = [
            {"facility": name.strip()}
            for name in set(response.xpath(bk.MAIN_FACILITIES).extract())
            if name.strip() != ""
        ]
        facilities = [
            {"facility": name.strip()}
            for name in set(
                pe.remove_line_break(
                    response.xpath(bk.FACILITIES).xpath("string(.)").extract_first()).split(
                    "\n")
            )
            if name not in useless_facilities
        ]
        gallery = [
            {"image_url": ori_url}
            for ori_url in response.xpath('.').re(r"highres_url: '(.*?)'")
        ]
        city_name = response.xpath('.').re(r"city_name: '(.*?)'")
        ori_hotel_name = response.xpath(
            bk.ORI_HOTEL_NAME).extract_first().strip().split('（')
        if len(ori_hotel_name) == 1:
            hotel_name = hotel_name_en = ori_hotel_name[0]
        else:
            hotel_name, hotel_name_en = ori_hotel_name[1][:-
            1], ori_hotel_name[0]
        hotel_address = pe.remove_line_break(
            response.xpath(
                bk.HOTEL_ADDRESS
            ).extract()
        )
        loader.add_value("rooms", rooms)
        loader.add_value("introduction", introduction)
        loader.add_value("polices", polices)
        loader.add_value("attractions", attractions)
        loader.add_value("facilities", main_facilities)
        loader.add_value("all_facilities", facilities)
        loader.add_value("gallery", gallery)
        if city_name:
            loader.add_value("city_name", city_name)
        loader.add_value("name", hotel_name)
        loader.add_value("name_en", hotel_name_en)
        loader.add_value("address", hotel_address)
        loader.add_value("bk_url", url)
        loader.add_value("capture_urls_id", '')
        loader.add_value('spider_name', spider_name)
        parse_result = loader.load_item()
        parse_dict = dict(parse_result)
        parse_info = [k for k, v in parse_dict.items() if not v or v == ['']]
        parse_info.remove('capture_urls_id')
        if parse_info:
            logger.warning(f'[{hotel_name}]数据解析完成,其中空字段为{parse_info}')
        yield parse_result

    def start_tripadvisor(self, url_dict):
        city_name = url_dict.get('city')
        country_name = url_dict.get('country')

        spider_name = url_dict.get('spider_name')
        url = 'https://www.tripadvisor.cn/Lvyou'
        allow_num = url_dict.get('allow_num')
        return Request(
            str(url),
            meta={
                'city_name': city_name,
                'allow_num': allow_num,
                'country_name': country_name,
                'spider_name': spider_name
            },
            callback=self.get_tripadvisor_country_url,
            dont_filter=True,
        )

    def get_tripadvisor_country_url(self, response):
        """
        获取coutry_name对应的url
        :param response:
        :return:
        """
        meta = response.meta
        city_name = meta.get('city_name')
        country_name = meta.get('country_name')
        country_url_list = response.selector.xpath('//*[@id="tab-body-wrapper-ipad"]//li/a').extract()
        country_url = [country_url for country_url in country_url_list if country_name in country_url]

        if country_url:
            country_url = re.findall('href="(.*?)"', country_url[0])[0]  # 国家首页URL
            # 需要的是国家酒店URL
            city_hotel_url = country_url.replace('Vacations', 'Hotels').replace('Tourism', 'Hotels')
            city_hotel_url = 'https://www.tripadvisor.cn' + city_hotel_url
            yield Request(
                str(city_hotel_url),
                meta=meta,
                callback=self.get_tripadvisor_city_url,
                dont_filter=True)
        else:
            lost_city_or_country.append({'city_name': city_name, 'country_name': country_name, 'err_msg': '没有此国家', })
            logger.info(lost_city_or_country)

    def get_tripadvisor_city_url(self, response):
        """
        进入城市酒店列表页,会带上一些过滤条件
        :param response:
        :return:
        """
        meta = response.meta
        city_name = meta.get('city_name')
        country_name = meta.get('country_name')
        city_url_list = response.selector.xpath(
            '//*[@id="taplc_hotels_leaf_geo_list_dusty_hotels_resp_0"]/div/div').extract()
        lost_city = meta.get('lost_city')
        filter_or_not = meta.get('filter_or_not')
        if filter_or_not == '1':  # 这里是开启过滤
            data = {
                'sl_opp_json': '{}',
                'plSeed': '1730470459',
                'offset': '0',
                'zfp': '',
                'zff': '',
                'trating': '4,5',
                'zft': '',
                'bs': '',
                'zfc': '9566,9572',
                'cat_tag': '9189',
                'amen': '',
                'df': '',
                'zfd': '',
                'distFrom': '',
                'zfb': '',
                'zfn': '',
                'ns': '',
                # 'pRange': '600,5000,RMB,ALL_IN_WITH_EXCLUSIONS',#价格参数
                'distFromPnt': '',
                'reqNum': '1',
                'isLastPoll': 'false',
                'sortOrder': 'popularity',  # 排序参数
                'paramSeqId': '9',
                'waitTime': '254',
                'changeSet': 'FILTERS,MAIN_META',
                'puid': 'XNqF-8CoATQAA0-cgzsAAAF6'
            }
        elif filter_or_not == '0':  # 这里是不开启过滤.
            data = {  # 这个data请求的参数是不带任何筛选条件的,就是会请求所有酒店
                'sl_opp_json': '{}',
                'plSeed': '1730470459',
                'offset': '0',
                'reqNum': '1',
                'isLastPoll': 'false',
                'paramSeqId': '9',
                'waitTime': '254',
                'changeSet': '',
                'puid': 'XNqF-8CoATQAA0-cgzsAAAF6'
            }
        headers = {
            'X-Puid': 'XNqF-8CoATQAA0-cgzsAAAF6',
            'Origin': 'https://www.tripadvisor.cn',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'text/html, */*',
            'Referer': 'https://www.tripadvisor.cn/Hotels-g298484-Moscow_Central_Russia-Hotels.html',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
        }
        if lost_city == '1':  # 如果抓取的是正常城市
            city_url = [city_url for city_url in city_url_list if city_name in city_url]
            if city_url:
                city_url = re.findall('href="(.*?)"', city_url[0])[0]  # 国家首页URL
                base_url = 'https://www.tripadvisor.cn'
                city_url = base_url + city_url
                data = data
                headers = headers
                meta['data'] = data
                meta['headers'] = headers
                yield scrapy.FormRequest(url=city_url, formdata=data,
                                         callback=self.get_tripadvisor_response,
                                         headers=headers,
                                         meta=meta,
                                         dont_filter=True,
                                         )
            else:
                lost_city_or_country.append({'city_name': city_name, 'country_name': country_name, 'err_msg': '没有城市', })
                logger.info(lost_city_or_country)
        elif lost_city == '0':  # 如果抓取的是缺失城市
            # 这里是部分缺失城市url
            lost_city_url_list = \
                [
                    {'city_name': '五渔村',
                     'city_url': 'https://www.tripadvisor.cn/Hotels-g187817-Cinque_Terre_Italian_Riviera_Liguria-Hotels.html',
                     'country_name': '意大利'},
                    {'city_name': '拉斯佩齐亚',
                     'city_url': 'https://www.tripadvisor.cn/Tourism-g187824-La_Spezia_Province_of_La_Spezia_Liguria-Vacations.html',
                     'country_name': '意大利'},
                    {'city_name': '巴斯',
                     'city_url': 'https://www.tripadvisor.cn/Hotels-g187346-Wiesbaden_Hesse-Hotels.html',
                     'country_name': '英国'},
                    {'city_name': '苏格兰', 'city_url': 'https://www.tripadvisor.cn/Hotels-g186485-Scotland-Hotels.html',
                     'country_name': '英国'},
                    {'city_name': '牛津',
                     'city_url': 'https://www.tripadvisor.cn/Hotels-g186361-Oxford_Oxfordshire_England-Hotels.html',
                     'country_name': '英国'},
                    {'city_name': '托斯卡纳', 'city_url': 'https://www.tripadvisor.cn/Hotels-g187893-Tuscany-Hotels.html',
                     'country_name': '意大利'},
                    {'city_name': '米克诺斯',
                     'city_url': 'https://www.tripadvisor.cn/Hotels-g189430-Mykonos_Cyclades_South_Aegean-Hotels.html',
                     'country_name': '希腊'},
                    {'city_name': '剑桥',
                     'city_url': 'https://www.tripadvisor.cn/Hotels-g186225-Cambridge_Cambridgeshire_England-Hotels.html',
                     'country_name': '英国'},
                    {'city_name': '阿维尼翁',
                     'city_url': 'https://www.tripadvisor.cn/Hotels-g187212-Avignon_Vaucluse_Provence_Alpes_Cote_d_Azur-Hotels.html',
                     'country_name': '法国'},

                    {'city_name': '毛里求斯',
                     'city_url': 'https://www.tripadvisor.cn/Hotels-g293816-Mauritius-Hotels.html',
                     'country_name': '毛里求斯'},
                    {'city_name': '函馆',
                     'city_url': 'https://www.tripadvisor.cn/Hotels-g298151-Hakodate_Hokkaido-Hotels.html',
                     'country_name': '日本'},
                    {'city_name': '卡萨布兰卡',
                     'city_url': 'https://www.tripadvisor.cn/Hotels-g293732-Casablanca_Grand_Casablanca_Region-Hotels.html',
                     'country_name': '摩洛哥'},
                    {'city_name': '马拉喀什',
                     'city_url': 'https://www.tripadvisor.cn/Hotels-g293734-Marrakech_Marrakech_Tensift_El_Haouz_Region-Hotels.html',
                     'country_name': '摩洛哥'},
                    {'city_name': '瓦尔扎扎特',
                     'city_url': 'https://www.tripadvisor.cn/Hotels-g304018-Ouarzazate_Souss_Massa_Draa_Region-Hotels.html',
                     'country_name': '摩洛哥'},
                    {'city_name': '舍夫沙万',
                     'city_url': 'https://www.tripadvisor.cn/Hotels-g304013-Chefchaouen_Tangier_Tetouan_Region-Hotels.html',
                     'country_name': '摩洛哥'},
                    {'city_name': '名古屋',
                     'city_url': 'https://www.tripadvisor.cn/Hotels-g298106-Nagoya_Aichi_Prefecture_Tokai_Chubu-Hotels.html',
                     'country_name': '日本'},
                    {'city_name': '轻井泽町',
                     'city_url': 'https://www.tripadvisor.cn/Hotels-g325581-Karuizawa_machi_Kitasaku_gun_Nagano_Prefecture_Koshinetsu_Chubu-Hotels.html',
                     'country_name': '日本'},
                    {'city_name': '清迈 ', 'city_url': 'https://www.tripadvisor.cn/Hotels-g293917-Chiang_Mai-Hotels.html',
                     'country_name': '泰国'},
                    {'city_name': '澳门', 'city_url': 'https://www.tripadvisor.cn/Hotels-g664891-Macau-Hotels.html',
                     'country_name': '中国'},
                    {'city_name': '伊豆',
                     'city_url': 'https://www.tripadvisor.cn/Hotels-g790340-Izu_Shizuoka_Prefecture_Tokai_Chubu-Hotels.html',
                     'country_name': '日本'},
                    {'city_name': '长滩岛',
                     'city_url': 'https://www.tripadvisor.cn/Hotels-g294260-Boracay_Malay_Aklan_Province_Panay_Island_Visayas-Hotels.html',
                     'country_name': '菲律宾'},
                    {'city_name': '苏梅岛',
                     'city_url': 'https://www.tripadvisor.cn/Hotels-g293918-Ko_Samui_Surat_Thani_Province-Hotels.html',
                     'country_name': '泰国'},
                    {'city_name': '非斯',
                     'city_url': 'https://www.tripadvisor.cn/Hotels-g293733-Fes_Fes_Boulemane_Region-Hotels.html',
                     'country_name': '摩洛哥'},
                    {'city_name': '马尔代夫',
                     'city_url': 'https://www.tripadvisor.cn/Hotels-g293953-Maldives-Hotels.html',
                     'country_name': '马尔代夫'},
                    {'city_name': '宿雾',
                     'city_url': 'https://www.tripadvisor.cn/Hotels-g294261-Cebu_Island_Visayas-Hotels.html',
                     'country_name': '菲律宾'},
                    {'city_name': '巴厘岛',
                     'city_url': 'https://www.tripadvisor.cn/Hotels-g294226-Bali-Hotels.html',
                     'country_name': '印度尼西亚'},
                    {'city_name': '美奈',
                     'city_url': 'https://www.tripadvisor.cn/Hotels-g1009804-Mui_Ne_Phan_Thiet_Binh_Thuan_Province-Hotels.html',
                     'country_name': '越南'},
                    {'city_name': '芭提雅',
                     'city_url': 'https://www.tripadvisor.cn/Hotels-g293919-Pattaya_Chonburi_Province-Hotels.html',
                     'country_name': '泰国'},
                    {'city_name': '香港',
                     'city_url': 'https://www.tripadvisor.cn/Hotels-g294217-Hong_Kong-Hotels.html',
                     'country_name': '中国'},
                    {'city_name': '台湾',
                     'city_url': 'https://www.tripadvisor.cn/Hotels-g293910-Taiwan-Hotels.html',
                     'country_name': '中国'},
                    {'city_name': '热海',
                     'city_url': 'https://www.tripadvisor.cn/Hotels-g298122-Atami_Shizuoka_Prefecture_Tokai_Chubu-Hotels.html',
                     'country_name': '日本'}]
            for lost_city in lost_city_url_list:
                city_name = lost_city.get('city_name')
                country_name = lost_city.get('country_name')
                meta['city_name'] = city_name
                meta['country_name'] = country_name
                meta['allow_num'] = '300'
                city_url = lost_city.get('city_url')
                data = data
                headers = headers
                meta['data'] = data
                meta['headers'] = headers
                yield scrapy.FormRequest(url=city_url, formdata=data,
                                         callback=self.get_tripadvisor_response,
                                         headers=headers,
                                         meta=meta,
                                         dont_filter=True,
                                         )

    def get_tripadvisor_response(self, response):
        meta = response.meta
        data = meta.get('data')
        headers = meta.get('headers')
        hotel_list = response.xpath(
            '//div[contains(@class,"prw_rup") and contains(@class,"prw_meta_hsx_responsive_listing")]/div').extract()
        for hotel in hotel_list:
            hotel = scrapy.Selector(text=hotel)
            hotel_url = hotel.xpath(tripadvisor_xp.HOTEL_URL).extract_first()
            base_url = 'https://www.tripadvisor.cn'
            hotel_url = base_url + hotel_url
            hotel_name = hotel.xpath(tripadvisor_xp.HOTEL_NAME).extract_first()
            hotel_en_name = hotel.xpath(tripadvisor_xp.HOTEL_EN_NAME).extract_first()
            hotel_en_name = hotel_en_name.split('-')[-2]
            price = response.xpath(tripadvisor_xp.PRICE).extract_first()
            price = price.replace('￥', '')
            hotel_desc = hotel.xpath('//div[@class="popindex"]//text()').extract_first()
            lost_desc = hotel.xpath(tripadvisor_xp.LOST_DESC).extract()
            meta['price'] = price
            meta['hotel_desc'] = hotel_desc
            meta['lost_desc'] = lost_desc
            meta['hotel_url'] = hotel_url
            meta['hotel_name'] = hotel_name
            booking_serach_url = f'https://www.booking.com/searchresults.zh-cn.html?ss={hotel_en_name}'
            # print(booking_serach_url)
            yield Request(
                url=booking_serach_url,
                callback=self.handle_booking_search_response,
                dont_filter=True,
                meta=meta,
            )

        offset = data['offset']
        # 如果这个参数!=0.就证明已经开始列表页抓取了
        if offset == '0':
            city_name = meta.get('city_name')
            allow_num = int(meta.get('allow_num'))
            country_name = meta.get('country_name')
            max_page_num = re.findall("中有 (\d+) 家符合您的筛选条件", response.text)
            if max_page_num:
                max_page_num = int(max_page_num[0])
                if max_page_num >= allow_num:
                    max_page_num = allow_num
                else:
                    pass  # 如果酒店数不够就全量获取

                city_max_hotel_num.append(
                    {'city_name': city_name, 'country_name': country_name,
                     'max_page_num': '当前最多酒店数' + str(max_page_num)})
                logger.info(city_max_hotel_num)
                max = math.ceil(int(max_page_num) / 30)
                for i in range(1, max):
                    data['offset'] = str(i * 30)
                    # time.sleep(2)
                    yield scrapy.FormRequest(url=response.url, formdata=data,
                                             callback=self.get_tripadvisor_response,
                                             headers=headers,
                                             meta=meta,
                                             dont_filter=True,
                                             )

    def handle_booking_search_response(self, response):
        meta = response.meta

        hotel_url = meta.get('hotel_url')
        booking_name = response.xpath(tripadvisor_xp.BOOKING_NAME).extract_first()
        booking_url = response.xpath(tripadvisor_xp.BOOKING_URL).extract_first()
        if booking_name:
            booking_name = booking_name.strip()
        if booking_url:
            booking_url = booking_url.strip()
        if booking_url is None:  # 这里没有url代表被发现,只能重新请求
            yield Request(
                url=response.url,
                callback=self.handle_booking_search_response,
                dont_filter=True,
                meta=meta,
            )
        else:
            booking_url = 'https://www.booking.com' + booking_url
            booking_url = booking_url.split('?')[0]
            meta['booking_url'] = booking_url
            meta['booking_name'] = booking_name
            yield Request(
                url=hotel_url,
                callback=self.xpath_tripadvisor_hotel_response,
                dont_filter=True,
                meta=meta,
            )

    def xpath_tripadvisor_hotel_response(self, response):
        meta = response.meta
        comment_data = parser_commits(html=response.text)
        comments = comment_data.get('comments')
        price = meta.get('price', 0)
        hotel_desc = meta.get('hotel_desc', '未获取到酒店排名')
        lost_desc = meta.get('lost_desc')
        start_time = meta.get('start_time')
        end_time = meta.get('end_time')
        country_name = meta.get('country_name')
        city_name = meta.get('city_name')
        booking_url = meta.get('booking_url')
        booking_name = meta.get('booking_name')
        spider_name = meta.get('spider_name', 'tripadvisor')
        response_text = response.text
        star_level = re.findall('(\d) 星级住宿', response_text)
        latitude = re.findall('latitude":(\d+.\d+)', response_text)
        longitude = re.findall('longitude":(\S\d+.\d+|\d+.\d+)', response_text)
        room_nums = re.findall('class="textitem" data-prwidget-name="text" data-prwidget-init.*?>(\d+)<',
                               response_text)
        image_list = re.findall('https:\/\/.*?jpg', response_text)

        filter_image_list = set([result for result in image_list if 'photo-w' in result or 'photo-m' in result])
        filter_image_list = set([result for result in filter_image_list if len(result) < 200])
        if star_level:
            star_level = star_level[0]
        else:
            star_level = '无酒店星级'
        loader = ItemLoader(item=TripAdvisor(), response=response)
        loader.add_xpath('hotel_name_ch', tripadvisor_xp.HOTEL_NAME_CH)
        loader.add_xpath('hotel_name_en', tripadvisor_xp.HOTEL_NAME_EN)
        loader.add_xpath('hotel_facility', tripadvisor_xp.HOTEL_FACILITY)
        loader.add_xpath('phone', tripadvisor_xp.PHONE)
        loader.add_value('lost_desc', lost_desc)
        loader.add_value('comments', comments)
        loader.add_xpath('comment_level', tripadvisor_xp.COMMENT_LEVLE)
        loader.add_value('spider_name', spider_name)
        loader.add_xpath('hotel_address', tripadvisor_xp.ADDRESS)
        loader.add_value('hotel_tripadvisor_url', response.url)
        loader.add_value('hotel_low_price', price)
        loader.add_value('start_time', start_time)
        loader.add_value('end_time', end_time)
        loader.add_value('city_name', city_name)
        loader.add_value('country_name', country_name)
        loader.add_value('hotel_desc', hotel_desc)
        loader.add_value('star_level', star_level)
        loader.add_value('latitude', latitude)
        loader.add_value('longitude', longitude)
        loader.add_value('booking_url', booking_url)
        loader.add_value('booking_name', booking_name)
        loader.add_value('room_nums', room_nums)
        loader.add_value('image_url', filter_image_list)
        loader.add_value('image_url', filter_image_list)

        yield loader.load_item()
