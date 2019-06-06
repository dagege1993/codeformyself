# coding: utf8

# Standard Library
import time
import typing
from hashlib import sha256

# Non Standard Library
from yarl import URL
from celery.utils.log import get_task_logger

import requests
from tasks.utils.database import databases
from tasks.supplier_statics import Providers, BaseSupplier

logger = get_task_logger('tasks')


class HotelBeds(BaseSupplier):
    """获取HotelBeds的静态数据，并更新到数据库.
    """

    supplier = Providers.hotelbeds

    endpoint = URL("https://api.hotelbeds.com/hotel-content-api/1.0/")

    imagebase = URL("http://photos.hotelbeds.com/giata/original/")

    key = "5c3djnfxkpxuhsd5emcsep6j"
    secret = "Jc25QB5RDP"

    def images(self, images):
        return [str(self.imagebase / img["path"]) for img in images]

    @property
    def signature(self):
        string = "".join([self.key, self.secret, str(int(time.time()))])
        sha = sha256(string.encode("utf8"))
        return sha.hexdigest()

    @property
    def headers(self):
        return {
            "Accept-Encoding": "Gzip",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Signature": self.signature,
            "Api-Key": self.key,
        }

    @property
    def last_update_time(self):
        return None
        newest = self.table("hotels").find().sort("last_modified", -1)[0]
        return newest["last_modified"]

    def fetch(self, types: str = "hotels", code = "") -> typing.Iterable:
        """这里是文档.
        param types: 需要获取的数据类型

        Returns
        """
        with requests.Session() as session:
            params = {
                "from": 1, "to": 1000, "language": "ENG", "fields": "all"
            }
            if self.last_update_time:
                params["lastUpdateTime"] = self.last_update_time

            total = 2001
            while total >= params["to"]:
                response = session.get(
                    str(self.endpoint / types),
                    params=params,
                    headers=self.headers,
                )
                resp = response.json()
                total = resp["total"]
                params["to"] += 1000
                params["from"] += 1000
                yield resp[types]
    
    def fetch_one(self, types: str = "hotels", code_list: list = []) -> typing.Iterable:
        with requests.Session() as session:
            params = {"language": "ENG", "fields": "all"}
            for code in code_list:
                params['codes'] = str(code)
                response = session.get(
                    str(self.endpoint / types),
                    params=params,
                    headers=self.headers,
                )
                resp = response.json()
                resp = resp.get(types)
                if resp:
                    yield resp
                else:
                    yield [500]

    def hotels(self, hotels_by_code: list = None):
        if hotels_by_code:
            logger.info(f'根据hotels_by_code:{hotels_by_code},更新了静态数据库')
            for hotel in hotels_by_code:
                if hotel == 500:
                    continue
                self._save_hotel(hotel)
        else:
            for hotels in self.fetch("hotels"):
                for hotel in hotels:
                    self._save_hotel(hotel)
    
    def hotel(self, code, online=False):
        for hotel in self.fetch_one('hotels', [code]):
            self._save_hotel(hotel[0], online)

    def _save_hotel(self, hotel, online=False):
        images = hotel.get("images", [])
        hotel["_images"] = images
        hotel["images"] = self.images(images)
        hotel["name"] = hotel["name"]["content"]
        hotel["description"] = hotel.get("description", {}).get(
            "content"
        )
        hotel["country"] = {"code": hotel["countryCode"]}
        hotel["city"] = {"name": hotel["city"]["content"].title()}
        hotel["address"] = hotel["address"]["content"]
        if hotel.get("postalCode"):
            province = self.get_province_by_postal_code(
                hotel["postalCode"], hotel["country"]["code"]
            )
            if province:
                hotel["province"] = province
        cc: str = hotel.get("categoryCode", "0")[0]
        hotel["wgstar"] = cc.isnumeric() and int(cc) or 0
        try:
            hotel["latitude"] = hotel["coordinates"]["latitude"]
            hotel["longitude"] = hotel["coordinates"]["longitude"]
        except KeyError:
            pass
        for phone in hotel.get("phones", []):
            if phone["phoneType"].upper().startswith("PHONE"):
                hotel["phone"] = phone["phoneNumber"]
        self.save(hotel, "hotels", online=online)
