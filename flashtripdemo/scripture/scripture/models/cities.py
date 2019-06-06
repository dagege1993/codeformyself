# coding: utf8

import json


class Cities(dict):

    @classmethod
    def from_json(cls, jsn_file):
        with open(jsn_file) as fileobj:
            newcls = cls(json.load(fileobj))
        return newcls

    def name(self, city):
        if city in self:
            city = self[city]
        f = self.hub.meta_cities.find_one({'name_en': city})
        return str(f['name'])

    def oid(self, city):
        if city in self:
            city = self['city']
        f = self.hub.meta_cities.find_one({'name_en': city})
        return str(f['_id'])

    @property
    def hub(self):
        return self._db

    @hub.setter
    def hub(self, hub):
        self._db = hub
