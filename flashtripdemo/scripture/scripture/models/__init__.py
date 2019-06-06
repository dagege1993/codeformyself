# coding: utf8
from scrapy import Item, Field


class BaseModels(Item):
    spider_name = Field()
    url = Field()


from .hotels import Hotels

__all__ = [
    'Hotels',
]
