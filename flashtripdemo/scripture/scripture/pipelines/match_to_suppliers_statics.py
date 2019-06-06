# coding: utf8

# Standard Library
import json
import logging

from scripture.celery_task import CeleryTask


class MatchingPipeline:
    def __init__(self, settings):
        self.settings = settings
        self.logger = logging.getLogger(__name__)
        self.celery_task = CeleryTask(
            broker=settings.get("CELERY_BROKER"),
            backend=settings.get("CELERY_BACKEND"),
        )

    def open_spider(self, spider):
        if spider.name == "hcom":
            self.collection_name = "hotels"
            self._hotel_id_feild = "hotels_id"
        elif spider.name == "booking":
            self.collection_name = "bookings"
            self._hotel_id_feild = "hooking_id"
        else:
            self.collection_name = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_item(self, item, spider):
        if self.collection_name:
            self.celery_task(
                "tasks.hotel_matching",
                self.collection_name,
                json.dumps({self._hotel_id_feild: item[self._hotel_id_feild]}),
            )
            # celery.call()
        pass
