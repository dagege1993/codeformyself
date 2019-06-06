# coding: utf8
"""为供应商提供的酒店提供更详细的静态数据.
"""

# Standard Library
import re
import logging
from functools import lru_cache

import requests
from logzero import logger
from tasks.utils.database import databases


class Empty(Exception):
    pass


class Matching:
    def multi(self):
        """TODO: Docstring for function.

        Args:
            arg1 (TODO): TODO

        Returns: TODO

        """
        scripture = databases("scripture")
        collections = [scripture.bookings, scripture.hotels, scripture.ctrips]
        for collection in collections:
            for crawled_hotel in collection.find(no_cursor_timeout=True):
                self.one(crawled_hotel, collection.name)

    def one(self, crawled_hotel, collection_name):
        if "en" not in crawled_hotel:
            if "country" not in crawled_hotel:
                logger.error(
                    "Country is missing. ObjectId(%s)", crawled_hotel["_id"]
                )
                return None
            country_name = crawled_hotel["country"]
            if "city" not in crawled_hotel:
                logger.error(
                    "City is missing. ObjectId(%s)", crawled_hotel["_id"]
                )
                return None
            city = crawled_hotel["city"]
            if "name" not in crawled_hotel:
                logger.error(
                    "Name is missing. ObjectId(%s)", crawled_hotel["_id"]
                )
                return None
            name = crawled_hotel["name"]
            if "address" not in crawled_hotel:
                logger.error(
                    "Address is missing. ObjectId(%s)", crawled_hotel["_id"]
                )
                return None
            address = crawled_hotel["address"]
            if "latitude" not in crawled_hotel:
                logger.error(
                    "Latitude is missing. ObjectId(%s)", crawled_hotel["_id"]
                )
                return None
            latitude = crawled_hotel["latitude"]
            if "longitude" not in crawled_hotel:
                logger.error(
                    "longitude is missing. ObjectId(%s)", crawled_hotel["_id"]
                )
                return None
            longitude = crawled_hotel["longitude"]
            country = self._find_country_by_cn_name(country_name)
        else:
            if "country" not in crawled_hotel["en"]:
                logger.error(
                    "Country is missing. ObjectId(%s)", crawled_hotel["_id"]
                )
                return None
            country_name = crawled_hotel["en"]["country"]
            if "city" not in crawled_hotel["en"]:
                logger.error(
                    "City is missing. ObjectId(%s)", crawled_hotel["_id"]
                )
                return None
            city = crawled_hotel["en"]["city"]
            if "name" not in crawled_hotel["en"]:
                logger.error(
                    "Name is missing. ObjectId(%s)", crawled_hotel["_id"]
                )
                return None
            name = crawled_hotel["en"]["name"]
            if "address" not in crawled_hotel["en"]:
                logger.error(
                    "Address is missing. ObjectId(%s)", crawled_hotel["_id"]
                )
                return None
            address = crawled_hotel["en"]["address"]
            if "latitude" not in crawled_hotel["en"]:
                logger.error(
                    "Latitude is missing. ObjectId(%s)", crawled_hotel["_id"]
                )
                return None
            latitude = crawled_hotel["en"]["latitude"]
            if "longitude" not in crawled_hotel["en"]:
                logger.error(
                    "Longitude is missing. ObjectId(%s)", crawled_hotel["_id"]
                )
                return None
            longitude = crawled_hotel["en"]["longitude"]
            country = self._find_country_by_en_name(country_name)
        if not country:
            country = self._find_country_by_partial_name(country_name)
        if not country:
            logger.error(
                'Country("%s") of Hotel(%s) not found.', country_name, name
            )
            return None
        country_code = country["code_cca2"]
        try:
            destination = self._destination_matching(
                country_code=country_code,
                latitude=latitude,
                longitude=longitude,
                address=address,
            )
        except Exception as e:
            logger.exception(e)
            return None
        if not destination:
            logger.critical(
                "Bad destination of Hotel(%s) at " "Country(%s) with City(%s)",
                name,
                country_name,
                city,
            )
            return None

        try:
            matches = self._hotel_matching(
                name=name,
                address=address,
                longitude=longitude,
                latitude=latitude,
                phone=None,
                wg_destination_id=destination.get("destination_id"),  #
                wg_city_id=destination.get("city_id"),
                wg_province_id=destination.get("province_id"),
                wg_country_id=destination.get("country_id"),
            )
        except Empty:
            logger.critical(
                "Similarities of Hotel(%s) at Destination(%s) is empty.",
                name,
                destination,
            )
            return None
        except Exception as e:
            logger.critical(
                "Falied to got matched hotels. "
                "Hotel('%s'), Destination(%s)",
                name,
                destination,
                exc_info=e,
            )
            return None
        for _matched in matches:
            logger.info(
                self._set_relationships(
                    _matched["provider"],
                    _matched["oid"],
                    collection_name,
                    str(crawled_hotel["_id"]),
                )
            )
        return True

    def _destination_matching(
        self, country_code, address, latitude, longitude
    ):
        response = requests.get(
            "http://172.16.3.152/api/v1/destination/",
            # "http://127.0.0.1:4020/api/v1/destination/",
            params={
                "country_code": country_code,
                "address": address,
                "lat": latitude,
                "lng": longitude,
            },
        )
        if response.status_code == 404:
            raise Empty(response.text)
        if response.status_code != 200:
            raise Exception(response.text)
        try:
            json_response = response.json()
        except Exception:
            raise Exception(response.text)
        if json_response["status"] != 200:
            raise Exception(json_response)
        return json_response["data"][0]["wg_result"]

    def _hotel_matching(
        self,
        name: str,
        address: str,
        longitude: str,
        latitude: str,
        phone: str = None,
        wg_destination_id: str = None,  #
        wg_city_id: str = None,
        wg_province_id: str = None,
        wg_country_id: str = None,
    ):
        if (
            (not wg_destination_id)
            and (not wg_city_id)
            and (not wg_province_id)
            and (not wg_country_id)
        ):
            raise Exception(
                "wg_destination_id or wg_city_id or wg_province_id"
                " or wg_country_id must be provide."
            )
        params = {
            "name": name,  # 酒店名称 - en
            "address": address,  # 酒店地址 - en
            "longitude": longitude,  # 数值或者字符串
            "latitude": latitude,
        }
        if wg_destination_id and wg_destination_id != "None":
            params["wg_destination_id"] = wg_destination_id  #
        if wg_city_id and wg_city_id != "None":
            params["wg_city_id"] = wg_city_id
        if wg_province_id and wg_province_id != "None":
            params["wg_province_id"] = wg_province_id
        if wg_country_id and wg_country_id != "None":
            params["wg_country_id"] = wg_country_id
        response = requests.get(
            "http://172.16.3.152/api/v1/examiner/",
            # "http://127.0.0.1:4020/api/v1/examiner/",
            params=params,
        )
        if response.status_code == 404:
            raise Empty(response.text)
        if response.status_code != 200:
            raise Exception(response.text)
        try:
            json_response = response.json()
        except Exception as e:
            raise Exception(response.text) from e
        if json_response["status"] != 200:
            raise Exception(response.text)
        return json_response["data"]

    def _set_relationships(
        self, collection, object_id, rel_collection, rel_object_id
    ):
        agent = databases("agent")
        has_relationship = agent.get_collection(collection).find_one(
            {
                "relation_to_crawled.rel_collection": rel_collection,
                "relation_to_crawled.rel_object_id": rel_object_id,
            }
        )
        if has_relationship:
            return True
        updated = agent.get_collection(collection).update_one(
            {"_id": object_id},
            {
                "$push": {
                    "relation_to_crawled": {
                        "rel_collection": rel_collection,
                        "rel_object_id": rel_object_id,
                    }
                }
            },
        )
        return updated.raw_result

    @lru_cache(64)
    def _find_country_by_partial_name(self, partial_name):
        return databases("agent").statics.countries.find_one(
            {"name_alts": re.compile(partial_name)}
        )

    @lru_cache(64)
    def _find_country_by_cn_name(self, cn_name):
        return databases("agent").statics.countries.find_one(
            {"name_cn": cn_name}
        )

    @lru_cache(64)
    def _find_country_by_en_name(self, en_name):
        return databases("agent").statics.countries.find_one(
            {"name_en": en_name}
        )
