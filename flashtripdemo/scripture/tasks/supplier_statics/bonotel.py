# coding: utf8

import requests
from lxml import objectify

# Current Project
from . import Providers, BaseSupplier


class Bonotel(BaseSupplier):

    supplier = Providers.bonotel

    username = "weegoLive_xml"

    def regions(self):
        for country in self.fetch("regions").country:
            country_code = country.countryCode
            country_name = country.countryName
            for state in country.state:
                try:
                    state_code = state.stateCode.text
                except AttributeError:
                    state_code = None
                try:
                    state_name = state.stateName.text
                except AttributeError:
                    state_name = None
                for city in state.city:
                    try:
                        city_code = city.cityCode.text
                    except AttributeError:
                        continue
                    region = {
                        "country_code": country_code,
                        "country_name": country_name,
                        "state_code": state_code,
                        "state_name": state_name,
                        "code": city_code,
                        "city_name": city.cityName,
                    }
                    self.save(region, table="regions")

    def hotels(self):
        for hotel in self.fetch("hotels").hotel:
            doc = {
                "code": int(hotel.hotelCode.text),
                "name": hotel.name.text,
                "address": hotel.address.text,
                "address2": hotel.address2.text,
                "city": {"name": hotel.city.text, "code": hotel.cityCode.text},
                "state": {
                    "name": hotel.state.text, "code": hotel.stateCode.text
                },
                "country": {
                    "name": hotel.country.text, "code": hotel.countryCode.text
                },
                "postal_code": hotel.postalCode.text,
                "phone": hotel.phone.text,
                "fax": hotel.fax.text,
                "latitude": float(hotel.latitude.text.replace(",", "")),
                "longitude": float(hotel.longitude.text.replace(",", "")),
                "rating": hotel.starRating,
                "images": [
                    image.text for image in hotel.images.image if image.text
                ],
                "cancel_policies": hotel.cancelPolicies.text,
                "limitation_policies": hotel.limitationPolicies.text,
                "description": hotel.description.text,
                "facilities": hotel.facilities.text,
                "recreation": hotel.recreation.text,
            }

            if doc["state"]["name"]:
                doc["province"] = doc["state"]["name"]
            elif doc["state"]["code"]:
                region = self.table("regions").find_one(
                    {"state_code": doc["state"]["code"]}
                )
                if region["state_name"]:
                    doc["province"] = region["state_name"]
                    doc["state"]["name"] = region["state_name"]
            if (not doc["state"]["name"]) and doc["postal_code"]:
                province = self.get_province_by_postal_code(
                    doc["postal_code"], doc["country"]["code"]
                )
                if province:
                    doc["province"] = province

            if not doc["city"]["name"]:
                region = self.table("regions").find_one(
                    {"city_code": doc["city"]["code"]}
                )
                if region:
                    doc["city"]["name"] = region["city_name"]

            star = doc["rating"].text[0]
            if star.isnumeric():
                doc["wgstar"] = int(star)
            else:
                doc["wgstar"] = 0

            self.save(doc)

    def fetch(self, types="hotels"):
        typem = {"hotels": "hotelAll", "regions": "region"}
        endpoint = f"http://api.bonotel.com/XMLCache/{typem[types]}0.xml"
        for i in range(3):
            resp = requests.get(endpoint)
            assert resp.status_code == 200, resp.text
            if resp.text and resp.status_code == 200:
                break
        assert resp.text is not None, resp.text
        parser = objectify.makeparser(huge_tree=True)
        return objectify.fromstring(resp.text.encode(), parser=parser)
