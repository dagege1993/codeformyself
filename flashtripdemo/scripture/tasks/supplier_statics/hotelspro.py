# coding: utf8

# Standard Library
import json
from datetime import datetime

# Non Standard Library
from yarl import URL

import requests
from tasks import settings
from tasks.supplier_statics import Providers, BaseSupplier


class HotelsPro(BaseSupplier):
    supplier = Providers.hotelspro

    user = "WeegoCosmos"
    token = "qfHDw9ZL47kPCVrh"

    endpoint = URL("http://cosmos.metglobal.tech/api/static/v1/")

    def fetch(self, types, code=''):
        auth = requests.auth.HTTPBasicAuth(self.user, self.token)
        with requests.Session() as session:
            params = {"limit": 100}
            _next = "next"
            endpoint = self.endpoint / (types + "/" + code)
            while True:
                if not _next:
                    break
                for i in range(3):
                    response = session.get(
                        endpoint,
                        params=params,
                        auth=auth,
                    )
                    if response.status_code == 200:
                        break
                assert response.status_code == 200, response.text
                resp = json.loads(response.text)
                if isinstance(resp, dict):
                    _next = resp.get("next")
                    if isinstance(_next, int):
                        params["next"] = _next
                    elif isinstance(_next, str):
                        params["next"] = URL(_next).query.get("next")
                    for item in resp["results"]:
                        yield item
                elif isinstance(resp, list):
                    _next = False
                    yield resp[0]

    def destinations(self):
        for dest in self.fetch("destinations"):
            self.save(dest, table="destinations")

    def countries(self):
        for country in self.fetch("countries"):
            self.save(country, table="country")

    def regions(self):
        for region in self.fetch("regions"):
            self.save(region, table="regions")

    def get_province_by_region_codes(self, codes):
        for code in codes:
            region = self.table("regions").find_one({"code": code})
            if not region:
                continue
            if region["kind"] in ["province", "state"]:
                return region["name"]

    def hotels(self):
        for hotel in self.fetch("hotels"):
            doc = self.format_doc(hotel)
            self.save(doc)
    
    def hotel(self, code, online=False):
        for hotel in self.fetch("hotels", code):
            doc = self.format_doc(hotel)
            self.save(doc, online=online)
            return doc
    
    def format_doc(self, hotel):
        doc = dict(hotel)
        if hotel["stars"]:
            doc["wgstar"] = int(hotel["stars"])
        else:
            doc["wgstar"] = 0
        doc["location"] = {
            "type": "Point",
            "coordinates": [hotel["longitude"], hotel["latitude"]],
        }
        city = self.table("destinations").find_one(
            {"code": hotel["destination"]}
        )
        doc["city"] = {"code": hotel["destination"]}
        if city:
            doc["city"]["name"] = city.get("name")
        else:
            self.logger.critical(
                "city name missing: city code(%s) ", hotel["destination"]
            )
        country = self.table("countries").find_one(
            {"code": hotel["country"]}
        )
        doc["country"] = {"code": hotel["country"]}
        if country:
            doc["country"]["name"] = country.get("name")
        else:
            self.logger.critical(
                "country name missing: country code(%s) ", hotel["country"]
            )
        if doc["regions"]:
            doc["province"] = self.get_province_by_region_codes(
                doc["regions"]
            ) or ""
        if hotel["images"]:
            doc["images"] = [
                img["original"]
                for img in hotel["images"]
                if img.get("original")
            ]

        doc["updated_at"] = datetime.strptime(
            hotel["updated_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        if 'code' not in doc:
            doc['code'] = str(doc.get('hotel_id', ''))
        return doc

if __name__ == "__main__":
    from tasks.utils.database import databases

    HotelsPro(databases("scripture")).regions()
