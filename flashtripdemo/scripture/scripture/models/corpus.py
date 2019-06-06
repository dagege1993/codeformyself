# coding: utf8

import logging

from pymongo import MongoClient
from scripture import settings
from scripture.utils import split

from gensim import corpora


class Corpus:

    logger = logging.getLogger(__name__)

    def __init__(
        self,
        dic: corpora.Dictionary,
        city: str,
        mongoc: MongoClient=None,
        city_id=None
    ) -> None:
        self.dic = dic
        self.city = city
        self.m = mongoc or MongoClient(settings.MONGO)
        self.mc = MongoClient(settings.MONGO)
        self.city_id = city_id

    def __iter__(self):
        for addr in self._names():
            yield self.dic.doc2bow(addr)

    def _names(self):
        if self.city.startswith(('East', 'South', 'West', 'North')):
            self.city = self.city.split(' ', 1)[-1]
        # c = self.m.scripture.cities.find_one({'en_name': self.city})
        c = self.mc.scripture.cities.find_one({'en_name': self.city})

        if not self.city_id and (c is None or 'city_id' not in c):
            self.logger.warn('Bad city %s %s', self.city_id, self.city)
            return []
        self.city_id = self.city_id or c['city_id']
        if isinstance(self.city_id, (str, bytes, int)):
            query = {'region.city_id': str(self.city_id)}
        elif isinstance(self.city_id, (list, tuple)):
            query = {'region.city_id': {'$in': list(self.city_id)}}
        for h in self.m.scripture.rxmls.find(query):
            yield split(
                h['name'],
                replace={'-': ' ', '&amp': 'and', '&': 'and'},
                drop={'.': None, ',': 0, '(': 0}
            )

    @classmethod
    def names(cls, city, mongo=None, city_id=None):
        return cls(None, city, mongo, city_id)._names()

    def to_vec(self, string):
        return self.dic.doc2bow((x for x in split(string) if x))

    def to_id(self, idx):
        if isinstance(self.city_id, (str, bytes, int)):
            query = {'region.city_id': str(self.city_id)}
        elif isinstance(self.city_id, (list, tuple)):
            query = {'region.city_id': {'$in': list(self.city_id)}}
        return self.m.scripture.rxmls.find(
            query,
            {'hotel_id': 1}
        )[idx]['hotel_id']
