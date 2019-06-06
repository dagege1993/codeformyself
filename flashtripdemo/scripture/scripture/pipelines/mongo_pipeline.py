# coding: utf8

import hashlib
import logging
import re
import json

from bson import ObjectId
from datetime import datetime, timedelta
from yarl import URL
import redis
import requests

from twisted.internet import defer
from txmongo.connection import ConnectionPool
from scripture.settings import REDIS_URL, PRICES_DING_TOKEN
from web import settings as web_setting
from scripture.utils import price_compare_check
import time

redis_url = URL(REDIS_URL)
db = int(redis_url.path.split("/")[1])

period = web_setting.COMPARE_TIME_PERIOD + 15000  # 每5秒查询一次，多保留15秒


class MongoPipeline:
    def __init__(self, settings):
        self.settings = settings
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls(crawler.settings)
        return pipeline

    @defer.inlineCallbacks
    def process_jset_item(self, item):
        created_at = datetime.now()
        jset_id = hashlib.md5(item["url"].encode("utf8")).hexdigest()
        item["jset_id"] = jset_id
        yield self.db.update_one(
            {"jset_id": jset_id},
            {
                "$set": item,
                "$setOnInsert": {"created_at": created_at},
                "$currentDate": {"updated_at": True},
            },
            upsert=True,
        )
        return item

    @defer.inlineCallbacks
    def process_tzoo_item(self, item):
        created_at = datetime.now()
        identity = {"tzoo_id": item["tzoo_id"]}
        result = yield self.db.update_one(
            identity,
            {
                "$set": item,
                "$setOnInsert": {"created_at": created_at},
                "$currentDate": {"updated_at": True},
            },
            upsert=True,
        )
        self.logger.debug(
            "Upsert tzoo %s, %s", item["tzoo_id"], result.raw_result
        )
        return item

    @defer.inlineCallbacks
    def process_booking_item(self, item):
        booking_id = item["hotels_id"]
        created_at = datetime.now()
        # item.add_value('summary',
        #                {
        #                    'key_facts': item.get_value('summary_key_facts')
        #                    # 'travellings': self._clean(take_all(resp, xp.SUMMARY_TRAVELLING)),
        #                    # 'transport': self._clean(take_all(resp, xp.SUMMARY_TRANSPORT))
        #                })
        item["summary"] = {"key_facts": item["summary_key_facts"]}
        item["title"] = item["title"].split("_")[0]
        _1024 = item.pop("pictures_1024")
        _1280 = item.pop("pictures_1280")
        td = []
        cl = []
        for e in _1280:
            td.append({"url", e})
            cl.append(re.findall("/(\d+)\.jpg", e)[0])
        for e in _1024:
            if re.findall("/(\d+)\.jpg", e)[0] in cl:
                pass
            else:
                td.append({"url": e})
        result = yield self.db.update_one(
            {"booking_id": booking_id},
            {
                "$set": dict(item),
                "$setOnInsert": {"created_at": created_at},
                "$currentDate": {"updated_at": True},
            },
            upsert=True,
        )
        self.logger.debug(
            "Update reviews of hotels %s, %s", booking_id, result.raw_result
        )

    def open_spider(self, spider):
        self.m = ConnectionPool(self.settings.get("MONGO"))
        if spider.name == "jetsetter":
            self.db = self.m.scripture.jsets
            self._processor = self.process_jset_item
        elif spider.name == "ustravelzoo":
            self._processor = self.process_tzoo_item
            self.db = self.m.scripture.tzoos
        elif spider.name == "hcom":
            self._processor = self.process_hotels_item
            self.db = self.m.scripture.hotels
            self.rooms_zh_db = self.m.scripture.hcom.zh.rooms
            self.rooms_en_db = self.m.scripture.hcom.en.rooms
        elif spider.name == "eventbrite":
            self._processor = self.process_eventbrite_item
            self.db = self.m.scripture.eventbrites
        elif spider.name == "booking":
            self._processor = self.process_booking_item
            self.db = self.m.scripture.bookings
        elif spider.name == "distributed_spider":
            self._processor = self.distributed_spider
            self.rds = redis.StrictRedis(
                host=redis_url.host, port=redis_url.port, db=db,
                password=redis_url.password
            )
        else:
            self._processor = lambda *args, **kwargs: None

    @defer.inlineCallbacks
    def process_hotels_item(self, item):
        locale = item.get("locale")
        hotels_id = item["hotels_id"]
        created_at = datetime.now()
        if locale == "cn":
            result = yield self.db.update_one(
                {"hotels_id": hotels_id},
                {
                    "$set": dict(item),
                    "$setOnInsert": {"created_at": created_at},
                    "$currentDate": {"updated_at": True},
                },
                upsert=True,
            )
            self.logger.debug(
                "set cn content for %s, %s", hotels_id, result.raw_result
            )
        elif locale == "en":
            del item["hotels_id"]
            update_result = yield self.db.update_one(
                {"hotels_id": hotels_id},
                {
                    "$set": {"en": dict(item)},
                    "$currentDate": {"updated_at": True},
                },
            )
            self.logger.debug(
                "Set english content for %s, %s.",
                hotels_id,
                update_result.raw_result,
            )
        elif locale is None:

            hotels_id = item["hotels_id"]

            if "rooms" in item or "en.rooms" in item:
                yield self._update_rooms(item)
            else:
                update_result = yield self._update_reviews(item)
                self.logger.debug(
                    "Update reviews. %s, %s",
                    hotels_id,
                    update_result.raw_result,
                )
        else:
            self.logger.error("Unknown locale %s", locale)

        return item

    @defer.inlineCallbacks
    def process_eventbrite_item(self, item):
        result = yield self.db.update_one(
            {"url": item["url"]},
            {
                "$set": item,
                "$setOnInsert": {"created_at": datetime.now()},
                "$currentDate": {"updated_at": True},
            },
            upsert=True,
        )
        self.logger.debug(
            "Upsert eventbrite %s, %s", item["url"], result.raw_result
        )
        return item

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        try:
            yield self._processor(item)
        except Exception as e:
            self.logger.error("Exception", exc_info=e)
            print('入库好像有问题', item)
            self.logger.info('item入库错误', item)
        return item

    @defer.inlineCallbacks
    def _update_reviews(self, item):

        hotels_id = item.pop("hotels_id")

        result = yield self.db.update_one(
            {"hotels_id": hotels_id},
            {"$set": item, "$currentDate": {"updated_at": True}},
        )
        self.logger.debug(
            "Update reviews of hotels %s, %s", hotels_id, result.raw_result
        )
        return item

    @defer.inlineCallbacks
    def _update_rooms(self, rooms):
        hotels_id = rooms.pop("hotels_id")
        key = list(rooms.keys())[0]  # 'rooms' or 'en.rooms'
        db = self.rooms_zh_db if key == "rooms" else self.rooms_en_db

        for room in rooms[key]:
            already_has = yield db.find_one(
                {
                    "hcom_id": hotels_id,
                    "room_type_code": room["room_type_code"],
                }
            )
            if already_has is None:
                room["_id"] = ObjectId()
                room["hcom_id"] = hotels_id
                room["created_at"] = datetime.now()
                room["updated_at"] = datetime.now()
                yield db.insert_one(room)
                self.logger.debug(
                    "hcom_id :%s add room_type_code: %s",
                    hotels_id,
                    room["room_type_code"],
                )
        return rooms

    @defer.inlineCallbacks
    def process_hotels_v2_item(self, item):
        locale = item.get("locale")
        hotels_id = item["hotels_id"]
        created_at = datetime.now()
        if locale == "cn":
            result = yield self.db.update_one(
                {"hotels_id": hotels_id},
                {
                    "$set": dict(item),
                    "$setOnInsert": {"created_at": created_at},
                    "$currentDate": {"updated_at": True},
                },
                upsert=True,
            )
            redis_conn = redis.StrictRedis(
                host=redis_url.host, port=redis_url.port, db=db
            )
            redis_conn.sadd("crawl_done_hcom", item.get("hotels_id"))
            self.logger.debug(
                "set cn content for %s, %s", hotels_id, result.raw_result
            )
        elif locale == "en":
            del item["hotels_id"]
            update_result = yield self.db.update_one(
                {"hotels_id": hotels_id},
                {
                    "$set": {"en": dict(item)},
                    "$currentDate": {"updated_at": True},
                },
                upsert=True,
            )
            self.logger.debug(
                "Set english content for %s, %s.",
                hotels_id,
                update_result.raw_result,
            )
        else:
            self.logger.error("unknown locale %s", locale)
        return item

    @defer.inlineCallbacks
    def process_booking_v2_item(self, item):
        created_at = datetime.now()
        result = yield self.db.update_one(
            {"bk_url": item.get("bk_url")},
            {
                "$set": dict(item),
                "$setOnInsert": {"created_at": created_at},
                "$currentDate": {"updated_at": True},
            },
            upsert=True,
        )
        _url = URL(item.get("bk_url"))
        hid = _url.path[7:]
        redis_conn = redis.StrictRedis(
            host=redis_url.host, port=redis_url.port, db=db
        )
        redis_conn.sadd("crawl_done_booking", hid)
        self.logger.debug(
            "Update info of hotels %s, %s",
            item.get("bk_url"),
            result.raw_result,
        )
        return item

    @defer.inlineCallbacks
    def process_booking_prices_item(self, item):
        created_at = datetime.now()
        cms_id = item.get("cms_id")[0]
        checkin = item.get("prices")[0]["checkin"]
        result = yield self.db.update_one(
            {"cms_id": cms_id, "prices.checkin": checkin},
            {
                "$set": {
                    "prices.$": item.get("prices")[0],
                    "min_price.$": item.get("min_price")[0],
                    "url": item.get("url", [""])[0],
                },
                "$setOnInsert": {"created_at": created_at},
                "$currentDate": {"updated_at": True},
            },
        )
        if not result.modified_count:
            result = yield self.db.update_one(
                {"cms_id": cms_id},
                {
                    "$push": {
                        "prices": item.get("prices")[0],
                        "min_price": item.get("min_price")[0],
                    },
                    "$setOnInsert": {"created_at": created_at},
                    "$currentDate": {"updated_at": True},
                },
                upsert=True,
            )
        self.logger.debug(
            "Update prices of bookings %s, %s", cms_id, result.raw_result
        )
        return item

    @defer.inlineCallbacks
    def process_ctrip_prices_item(self, item):
        created_at = datetime.now()
        cms_id = item.get("cms_id")[0]
        checkin = item.get("prices")[0]["checkin"]
        result = yield self.db.update_one(
            {"cms_id": cms_id, "prices.checkin": checkin},
            {
                "$set": {
                    "prices.$": item.get("prices")[0],
                    "url": item.get("url", [""])[0],
                },
                "$setOnInsert": {"created_at": created_at},
                "$currentDate": {"updated_at": True},
            },
        )
        if not result.modified_count:
            result = yield self.db.update_one(
                {"cms_id": cms_id},
                {
                    "$push": {"prices": item.get("prices")[0]},
                    "$set": {"url": item.get("url", [""])[0]},
                    "$setOnInsert": {"created_at": created_at},
                    "$currentDate": {"updated_at": True},
                },
                upsert=True,
            )
        self.logger.info(
            "Update prices of ctrip %s, %s", cms_id, result.raw_result
        )
        return item

    @defer.inlineCallbacks
    def process_compair_price(self, item):
        created_at = datetime.now()
        datas = {"created_at": created_at}
        for k, v in item.items():
            if k == "prices":
                datas["prices"] = v
                continue
            if isinstance(v, list) and v:
                datas[k] = v[0]
            else:
                datas[k] = v
        compair_prices = datas.get("prices")
        compair_price = [
                            e["price"] for e in compair_prices if e["compair"] == "booking"
                        ] or datas.get("compair_price")
        if compair_price and isinstance(compair_price, list):
            compair_price = compair_price[0]
        weego_price = datas.get("weego_price")
        datas.pop("url")
        if datas.get("uid"):
            uid = datas.pop("uid")
            result = yield self.db.update_one(
                {"_id": ObjectId(uid)}, {"$set": datas}
            )
        else:
            result = yield self.db.insert_one(datas)
        self.logger.info(f"Insert compair price : {result}")
        redis_payload = {
            'prices': datas.get("prices"),
            'compair': datas.get('compair'),
            'compair_room_type': datas.get('compair_room_type'),
            'compair_price': datas.get('compair_price')
        }
        query_key = f"scripture::compare::{datas['cms_id']}::{datas['checkin']}::{datas['checkout']}"
        self.rds.psetex(query_key, period, json.dumps(redis_payload))
        self.logger.info(f"\nquery_key: {query_key}\ndatas: {datas}\nredis_payload: {redis_payload}")
        # 增加无报价时处理
        return price_compare_check(datas, created_at, item)

    @defer.inlineCallbacks
    def handle_tripadvisor(self, item):
        hotel_info = dict(item)

        # print(hotel_info)
        hotel_name_ch = hotel_info.get('hotel_name_ch', ['当前酒店名字缺失'])[0].strip()
        hotel_name_en = hotel_info.get('hotel_name_en', ['当前酒店名字缺失'])[0]
        if hotel_name_en == '当前酒店名字缺失' and hotel_name_ch != '当前酒店名字缺失':
            hotel_name_en = hotel_name_ch
            hotel_name_ch = '当前酒店中文名字缺失'

        image_list = hotel_info.get('image_url')
        if image_list is None:
            gallery = []

        else:
            image_list = list(set(image_list))
            image_dict = {}
            for image in image_list:
                image_split = image.split('/')
                image_dict[image_split[-2] + image_split[-2]] = image
            image_url = (list(image_dict.values()))
            gallery = [{'image_url': image} for image in image_url]
        hotel_address = ''.join(hotel_info.get('hotel_address'))
        hotel_tripadvisor_url = hotel_info.get('hotel_tripadvisor_url')[0]
        city_name = hotel_info.get('city_name')[0]
        country_name = hotel_info.get('country_name')[0]
        star_level = hotel_info.get('star_level', ['未获取到酒店星级'])[0]
        lost_desc = hotel_info.get('lost_desc', [''])
        lost_desc = ''.join(lost_desc)
        comment_level = hotel_info.get('comment_level', ['未获取到评论等级'])[0]
        hotel_desc = hotel_info.get('hotel_desc', ['未获取根据旅行者名次'])[0]
        latitude = hotel_info.get('latitude', ['未获取到当前维度'])[0]
        longitude = hotel_info.get('longitude', ['未获取到当前经度'])[0]
        booking_name = hotel_info.get('booking_name', ['未解析到booking酒店名称'])[0]
        booking_url = hotel_info.get('booking_url', ['未解析到booking酒店链接'])[0]
        hotel_facility = hotel_info.get('hotel_facility', ['未获取到酒店设施'])
        comments = hotel_info.get('comments')
        phone = hotel_info.get('phone', ['未获取到当前酒店电话号码'])[0]
        room_nums = hotel_info.get('room_nums', ['未获取到房间数'])[0]
        hotel_facility.append('房间数:' + str(room_nums))
        # hotel_low_price = hotel_info.get('hotel_low_price')[0]
        # print(hotel_info)
        # yield self.db.insert_one(hotel_info)
        yield self.db.update_one(
            {
                "hotel_tripadvisor_url": hotel_tripadvisor_url
            },
            {"$set": {
                "hotel_name_ch": hotel_name_ch,
                "hotel_name_en": hotel_name_en,
                "hotel_address": hotel_address,
                "hotel_tripadvisor_url": hotel_tripadvisor_url,
                # "hotel_low_price": hotel_low_price,
                "city_name": city_name,
                "country_name": country_name,
                "star_level": star_level,
                "lost_desc": lost_desc,
                "comment_level": comment_level,
                "latitude": latitude,
                "longitude": longitude,
                "booking_name": booking_name,
                "booking_url": booking_url,
                "hotel_desc": hotel_desc,
                "hotel_facility": hotel_facility,
                "gallery": gallery,
                "comments": comments,
                "phone": phone,
            },
                "$setOnInsert": {"created_at": datetime.now()},
                "$currentDate": {"updated_at": True}},
            upsert=True,
        )

        return item

    @defer.inlineCallbacks
    def distributed_spider(self, item):
        spider_name = item.pop("spider_name")[0]
        if spider_name == "hcom_page":
            self.db = self.m.scripture.hotels
            yield self.process_hotels_v2_item(item)
        elif spider_name == "booking_page":
            self.db = self.m.scripture.bookings
            yield self.process_booking_v2_item(item)
        elif spider_name == "booking_prices":
            self.db = self.m.scripture.statics.booking.prices
            yield self.process_booking_prices_item(item)
        elif spider_name == "compair":
            self.db = self.m.scripture.compair
            yield self.process_compair_price(item)
        elif spider_name == "ctrip_prices":
            self.db = self.m.scripture.statics.ctrip.prices
            yield self.process_ctrip_prices_item(item)
        elif spider_name == "tripadvisor":
            self.db = self.m.scripture.tripadvisor_lostdesc
            yield self.handle_tripadvisor(item)
        return item
