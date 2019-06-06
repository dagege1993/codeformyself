# coding: utf8

# Standard Library
import enum
import json
import logging
import requests
from typing import Dict, Union
from datetime import datetime
from functools import partial

from bson import ObjectId
from celery.utils.log import get_task_logger
from tasks.application import app  # noqa
from tasks.utils.database import databases  # noqa
# First Party
from tasks import settings
from tasks.supplier_statics.hotel_name import fetch_ctrip_name
from tasks.supplier_statics.postal_code import get_province_by_postal_code
from tasks.supplier_statics.supplier_images import ImageSaver
from tasks.utils.notifiers import DingtalkMessage, DingtalkNotifier
from tasks.errors import NotifyFailed
from tasks import settings

DB = databases("scripture")
HUB = databases("hub")
key_list = ["latitude", "longitude", 'telephone', "website"]


class Providers(enum.Enum):
    bonotel = "bonotel"
    roomsxml = "roomsxml"
    hotelbeds = "hotelbeds"
    hotelspro = "hotelspro"
    jactravel = "jactravel"
    relux = "relux"
    relux_rooms = 'relux.rooms'


class BaseSupplier(object):

    supplier: enum.Enum

    logger = get_task_logger('tasks')

    def __init__(self, db):
        self.db = db

        try:
            self.image_saver = ImageSaver(self.supplier.value)
        except AttributeError:
            pass

    def table(self, table: str, supplier: Union[enum.Enum, str] = None):
        if not supplier:
            supplier = self.supplier
        if isinstance(supplier, str):
            return self.db.get_collection(f"statics.{table}.{supplier}")
        elif isinstance(supplier, enum.Enum):
            return self.db.get_collection(f"statics.{table}.{supplier.value}")

    @staticmethod
    def ensure_serializable(value):
        if value is None:
            return None
        if isinstance(value, dict):
            return {
                k: BaseSupplier.ensure_serializable(v)
                for k, v in value.items()
            }
        elif isinstance(value, (tuple, list)):
            return [BaseSupplier.ensure_serializable(v) for v in value]
        elif isinstance(value, (str, bytes, float, int, datetime, ObjectId)):
            return value

        else:
            return value.text

    def with_location(self, doc):
        try:
            doc["location"] = {
                "type": "Point",
                "coordinates": [doc["longitude"], doc["latitude"]],
            }
        except KeyError:
            pass

    def save_images(self, ori_doc: Dict, doc: Dict):
        try:
            if ori_doc:
                ori_images = [
                    img for img in (ori_doc.get("cdn_images") or []) if img
                ]
            else:
                ori_images = []
            doc["cdn_images"] = self.image_saver.upload_images(
                [img for img in (doc.get("images") or []) if img], ori_images
            )
        except KeyError:
            pass

    def save_ctrip_name(self, ori_doc: Dict, doc: Dict):
        if ori_doc and ori_doc.get("ctrip_name"):
            return
        update_name.delay(
            name=doc["name"], code=doc["code"], supplier=self.supplier.value
        )

    def get_province_by_postal_code(self, postal_code, country_code):
        return get_province_by_postal_code(postal_code, country_code)

    def with_country_id(self, doc):
        collection = self.db.statics.hotels[self.supplier.value]
        if self.supplier.value == "hotelbeds":
            h = collection.find_one(
                {
                    "country.code": doc["country"]["code"],
                    "wg_country_id": {"$exists": 1},
                }
            )
        elif self.supplier.value == "relux":
            h = {'wg_country_id': ObjectId('5abdbff6fc0e264f9bb1d317')}
        else:
            h = collection.find_one(
                {
                    "country.code": doc["country"].get("name") or doc["country"].get("code"),
                    "wg_country_id": {"$exists": 1},
                }
            )
        if not h:
            self.logger.error("wg_country_id is missing.")
            return
        doc["wg_country_id"] = h["wg_country_id"]
    
    def pre_save_check(self, document, table="hotels"):
        ori_document = (
            self.table(table, self.supplier).find_one(
                {"code": document["code"]}
            )
        )
        change = False
        if not ori_document:
            change = False
        elif self.supplier == Providers.relux_rooms:
            ori_rooms = ori_document.get('rooms_cn')
            if ori_rooms != document.get('rooms_cn'):
                change = True
                self.logger.info(f"{document['code']} rooms_cn change")
        else:
            self.updata_cms(ori_document, document)
            old_name = ori_document.get("name", '').lower().strip()
            old_address = ori_document.get("address", '').lower().strip()
            new_name = document.get("name", '').lower().strip()
            new_address = document.get("address", '').lower().strip()
            if new_name and new_address and (old_name != new_name or old_address != new_address):
                text = f'''## {self.supplier}供应商酒店信息变更\n
 - 供应商酒店id: {document["code"]}
 - 原酒店名称: {ori_document.get("name")}
 - 新酒店名称: {document.get("name")}
 - 原酒店地址: {ori_document.get("address")}
 - 新酒店地址: {document.get("address")}'''
                msg = DingtalkMessage(title='供应商酒店信息变更', text=text)
                try:
                    DingtalkNotifier().send(msg, settings.DINGTALK_NOTIFY['provider'])
                except NotifyFailed as exc:
                    self.logger.error('钉钉告警失败', exc_info=exc)
        if table == "hotels":
            if "relux" not in self.supplier.value and document.get("wgstar", 0) >= 3:
                self.save_images(ori_document, document)
            if 'relux' not in self.supplier.value:
                self.save_ctrip_name(ori_document, document)
        return change

    def save(self, document, table="hotels", online=False):
        if table == "hotels":
            self.with_location(document)
            if self.supplier != Providers.relux_rooms:
                self.with_country_id(document)
        if online:
            change = self.pre_save_check(document, table)
        else:
            change = False
        uresult = self.table(table, self.supplier).update_one(
            {"code": document["code"]},
            {
                "$set": self.ensure_serializable(document),
                "$setOnInsert": {"created_at": datetime.now()},
                "$currentDate": {"updated_at": True},
            },
            upsert=True,
        )
        if change:
            update_relux_data.delay(document['code'])
        return self.pprint(uresult)

    def updata_cms(self, ori_document, document):
        col_poi_items = HUB.get_collection('poi_items')
        hotel_id = document["code"]
        quoter = settings.SUPPLIER_NAME_2_ID.get(self.supplier.value)
        cmsID = col_poi_items.find_one(
            {"quote_ids.hotel_id": str(hotel_id),
             "quote_ids.quoter": ObjectId(quoter)},
            {"_id": 1}
        )
        if not cmsID:
            return
        data = {}
        for key in key_list:
            _compare_functool = partial(self._compare_statics_data, ori_document=ori_document,
                                        document=document, cms_key=key, data=data)
            if key == "latitude" or key == "longitude":
                _compare_functool(statics_key=key)
            elif key == "telephone":
                if self.supplier in [
                    Providers.bonotel, Providers.roomsxml, Providers.hotelbeds, Providers.hotelspro
                ]:
                    _compare_functool(statics_key="phone")
                elif self.supplier == Providers.relux:
                    _compare_functool(statics_key="tel")
            elif key == "website":
                if self.supplier == Providers.roomsxml:
                    _compare_functool(statics_key=key)
                elif self.supplier == Providers.hotelbeds:
                    new_value = document.get("web") or document.get("website")
                    ori_value = ori_document.get("web") or ori_document.get("website")
                    if new_value and new_value != ori_value:
                        data[key] = new_value
                elif self.supplier == Providers.relux:
                    _compare_functool(statics_key="url")
        if data:
            data['id'] = str(cmsID.get('_id'))
            self.logger.info(f'更新了一家酒店[hotel_id = {document["code"]}]的数据,data:{data}')
            requests.post(
                f"{settings.CMS_API}/api/internal/hotels",
                json=data,
                headers={"accept-version": "6.0.0"}
            )

    def _compare_statics_data(self, ori_document, document, statics_key, cms_key, data):
        new_value = document.get(statics_key)
        if new_value and ori_document.get(statics_key) != new_value:
            data[cms_key] = new_value

    def pprint(self, result):
        result = {
            attr: getattr(result, attr)
            for attr in dir(result)
            if not attr.startswith("_")
        }
        self.logger.debug(json.dumps(result, indent=2, default=repr))
        return True

    def hotels(self):
        pass

    def regions(self):
        pass

    def destinations(self):
        pass

    def fetch(self, types="hotels"):
        pass

# Current Project
# from .jactravel import JacTravel
from .bonotel import Bonotel  # noqa
from .roomsxml import RoomsXML  # noqa
from .hotelbeds import HotelBeds  # noqa
from .hotelspro import HotelsPro  # noqa
from .relux import ReluxHotel, ReluxRooms, update_quotes  # noqa
from .jactravel import JacTravel
from .travelflex import TraveFlex


@app.task
def update_hotelbeds(hotels_by_code: list=None):
    return HotelBeds(DB).hotels(hotels_by_code)


@app.task
def update_roomsxml():
    rx = RoomsXML(DB)
    rx.regions()
    rx.hotels()


@app.task
def update_bonotel():
    bt = Bonotel(DB)
    bt.regions()
    bt.hotels()


@app.task
def update_hotelspro():
    hp = HotelsPro(DB)
    hp.countries()
    hp.regions()
    hp.destinations()
    hp.hotels()


@app.task
def update_name(name: str, code: str, supplier: str):
    logger = logging.getLogger(__name__)
    service = BaseSupplier(DB)
    table = service.table("hotels", supplier)
    ctrip_name = fetch_ctrip_name(name)
    if not ctrip_name:
        logger.error(f"[Empty] {name}")
        return
    table.update_one({"code": code}, {"$set": {"ctrip_name": ctrip_name}})


@app.task
def update_relux_hotels():
    rlx = ReluxHotel(DB)
    for language in ['eng', 'chi', 'jpn']:
        rlx.hotels(language)


@app.task
def update_relux_rooms():
    rlx = ReluxRooms(DB)
    for language in ['eng', 'chi', 'jpn']:
        rlx.rooms(language)

@app.task
def update_jactravel():
    jct = JacTravel(DB)
    jct.room_types()
    jct.meal_types()


@app.task
def update_online_hotel_statics_data():
    hp = HotelsPro(DB)
    hb = HotelBeds(DB)
    online_hotels = []
    for hotel in HUB['poi_items'].find(
         {"__t": "Hotel", "edit_status": {"$in": ["edited", "audited"]},
         "publish_status": "online"},
         {'quote_ids': '1'}
    ):
        online_hotels.append(hotel)
    for hotel in online_hotels:
        for quote in hotel['quote_ids']:
            if not quote['hotel_id']:
                print(hotel)
                continue
            if str(quote['quoter']) == settings.SUPPLIER_NAME_2_ID['hotelspro']:
                hp.hotel(quote['hotel_id'], online=True)
            elif str(quote['quoter']) == settings.SUPPLIER_NAME_2_ID['hotelbeds']:
                hb.hotel(quote['hotel_id'], online=True)


@app.task
def update_relux_data(code):
    return update_quotes(code)


@app.task
def update_traveflex_hotel_code():
    tf = TraveFlex()
    tf.get_tf_city_id()
    requests.post(f'{settings.QUOTES}/api/v6/travflex/location')
    return
