#!/usr/bin/env python

from api.types.consts import const
from api.utils.singleton import singleton
from api.types.exception import BasePremiumException


@singleton
class Config(dict):
    def __init__(self):
        self.__can_import = True
        self.__init_default()
        dict.__init__(self)

    def __getattr__(self, item, default=""):
        if item in self:
            return self[item]
        return default

    @property
    def can_import(self):
        return self.__can_import

    def import_dict(self, **kwargs):
        if self.__can_import:
            for k, v in kwargs.items():
                self[k] = v
            self.__can_import = False
        else:
            raise BasePremiumException('ConfigImportError')

    def __init_default(self):
        self[const.DEBUG] = False
        self[const.AUTO_RELOAD] = True

    def has_item(self, item):
        return item in self

    def clear(self):
        self.__can_import = True
        dict.clear(self)
        self.__init_default()

    @staticmethod
    def __get_key_dict(sub_set, key):
        if key in sub_set:
            sk_dict = sub_set[key]
        else:
            sk_dict = {}
            sub_set[key] = sk_dict
        return sk_dict


configs = Config()
