#!/usr/bin/env python
# coding: utf8
"""Entrypoint of scripture project
"""

import functools
import logging
import logging.config
# Standard Library
import re

import fire
import logzero
import yaml
from pymongo import MongoClient

from scripture import settings as cfg
# from scripture.scripts import similarity
from scripture.scripts import dump_data, hotel, pressure_test, uploads
from scripture.scripts.matching_crawled_hotels_to_available_hotels import \
    Matching
from scripture.scripts.validations import bad_capture_id, not_uploaded, start

# from scripture.scripts import countries


@functools.lru_cache(256)
def get_country_code_by_name(db, country_name):
    country = db.statics.countries.find_one(
        {"$or": [{"name_en": country_name}, {"name_alts": country_name}]}
    )
    if country:
        return country["code_cca2"]


def make_requests_by_hotel_names(self):
    dbname = getattr(self, "dbname", "hcom")
    try:
        from scrapy import Request

        db = MongoClient(cfg.AGENT_DB).get_database()
        scripture_db = MongoClient(cfg.MONGO).get_database()

        projection = {
            "_id": 1,
            "name": 1,
            "name_cn": 1,
            "city.name": 1,
            "country.name": 1,
            "address": 1,
            "wgstar": 1,
        }

        with open("data/countries.yml") as yml:
            countries = yaml.load(yml)

        for provider in ["bonotel", "jactravel", "hotelspro"]:
            cursor = db.statics.hotels[provider].find(
                {
                    "country.name": {"$in": list(countries[provider].keys())},
                    "wgstar": {"$gte": 3},
                },
                projection,
                no_cursor_timeout=True,
            )
            for item in cursor:
                if scripture_db[dbname].find_one(
                    {"statics_hotels_id": item["_id"]}
                ):
                    continue
                if get_country_code_by_name(item["country"]["name"]):
                    country_code = get_country_code_by_name(
                        item["country"]["name"]
                    )
                else:
                    continue
                yield Request(
                    "=".join([self._entrypoint_page, item["name"]]),
                    getattr(self, "parse") or self._hotel_parse,
                    meta={
                        "statics.hotels.id": item["_id"],
                        "statics.hotels.supplier": provider,
                        "crawl_rooms": False,
                        "crawl_reviews": False,
                        "country_code": country_code,
                        "address": item["address"],
                        "name": item["name"],
                    },
                )
        cursor = db.statics.hotels["hotelbeds"].find(
            {
                "country.code": {"$in": list(countries[provider].keys())},
                "wgstar": {"$gte": 3},
            },
            projection,
            no_cursor_timeout=True,
        )
        for item in cursor:
            crawled = scripture_db[dbname].find_one(
                {"statics_hotels_id": item["_id"]}
            )
            if crawled:
                continue
            yield Request(
                "=".join([self._entrypoint_page, item["name"]]),
                getattr(self, "parse") or self._hotel_parse,
                meta={
                    "statics.hotels.id": item["_id"],
                    "statics.hotels.supplier": "hotelbeds",
                    "crawl_rooms": False,
                    "crawl_reviews": False,
                    "country_code": item["country"]["code"],
                    "address": item["address"],
                    "name": item["name"],
                },
            )
    except Exception as e:
        print(e)


class Crawl(object):  # pylint: disable=R0903
    """Crawlers controller
    """

    def booking(self, *, func=None):

        from twisted.internet import reactor
        from scrapy.crawler import CrawlerRunner
        from scrapy.utils.project import get_project_settings
        from scripture.spiders.booking import BookingSpider as Spider

        if func and not func.startswith("--"):
            print("func is", func)
            func = globals().get(func) or locals().get(func)
            if func:
                make_requests = func
            else:
                import importlib

                make_requests = importlib.import_module(func)

        Spider.start_requests = make_requests
        Spider._entrypoint_page = (
            "https://www.booking.com/searchresults.zh-cn.html?ss"
        )
        Spider.dbname = "bookings"
        _settings = get_project_settings()
        runner = CrawlerRunner(_settings)
        runner.crawl(Spider)
        deamon = runner.join()
        deamon.addBoth(lambda _: reactor.stop())  # pylint: disable=E1101
        reactor.run()  # pylint: disable=E1101

    def hcom(self, *, func=None, csvfile=None, ids=""):
        """Start spider for crawl hcom
        """
        from twisted.internet import reactor
        from scrapy import Request
        from scrapy.crawler import CrawlerRunner
        from scrapy.utils.project import get_project_settings
        from scripture.spiders.hcom import HcomSpider

        if func and not func.startswith("--"):
            print("func is", func)
            func = globals().get(func) or locals().get(func)
            if func:
                make_requests = func
            else:
                import importlib

                make_requests = importlib.import_module(func)
        elif csvfile:
            print("csvfile is", csvfile)

            def make_requests(self):
                """Make request by csvfile
                """
                import numpy
                import pandas
                from yarl import URL

                HCOM_ID_RE = re.compile(r"/ho([0-9]+)")

                df = pandas.read_csv(csvfile)  # pylint: disable=C0103

                for _, item in df.iterrows():
                    hcom_url = (
                        (item.get("hotels_URL") != numpy.NAN)
                        and item.get("hotels_URL")
                        or item.get("hotels_url")
                    )
                    if not hcom_url:
                        self.logger.error("Bad items %s", item)
                        continue
                    self.logger.debug(f"Url({hcom_url})")
                    hcom_url = URL(hcom_url)
                    if ".hotels." not in hcom_url.host:
                        self.logger.error("Bad items %s", item)
                        continue
                    try:
                        hcom_id = hcom_url.query.get(
                            "hotel-id"
                        ) or HCOM_ID_RE.match(hcom_url.path).group(1)
                    except Exception as e:
                        self.logger.error(item)
                        self.logger.exception(e)
                        continue
                    if not hcom_id:
                        self.logger.error("Bad url %s", hcom_url)
                        continue
                    yield Request(
                        "https://www.hotels.cn/ho{}".format(hcom_id),
                        self._hotel_parse,
                    )

        elif ids != "" and ids is not None:

            def make_requests(self):
                """Make reqeust by id of hcom
                """
                for hcom_id in ids:
                    yield Request(
                        "https://www.hotels.cn/ho{}".format(hcom_id),
                        self._hotel_parse,
                    )

        else:
            return (
                "Please provide a function to make request, or provide a"
                "csv file that contain url list."
            )

        HcomSpider.start_requests = make_requests
        HcomSpider._entrypoint_page = (
            "https://www.hotels.cn/search.do?q-destination",
        )
        _settings = get_project_settings()
        runner = CrawlerRunner(_settings)
        runner.crawl(HcomSpider)
        deamon = runner.join()
        deamon.addBoth(lambda _: reactor.stop())  # pylint: disable=E1101
        reactor.run()  # pylint: disable=E1101


if __name__ == "__main__":
    from scripture import settings

    logging.config.dictConfig(settings.LOGGERS)
    logging.getLogger().setLevel(logging.DEBUG)
    logzero.loglevel(logging.DEBUG)
    fire.Fire(
        {
            "test": lambda: None,
            "crawl": Crawl,
            "validate": {"uploaded": start, "not-uploaded": not_uploaded},
            "bad_capture_id": bad_capture_id,
            "hotel": hotel.Hotels,
            # 'similarity': similarity,
            "dumps": dump_data,
            "uploads": uploads,
            "pressure": pressure_test.main,
            "matching": Matching
            # 'countries': countries
        }
    )
