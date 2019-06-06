# coding: utf8


class Provider(object):
    def __init__(self, database):
        self.db = database
        self._fetch()

    def parse(self):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()
