# coding: utf8

# Standard Library
import time
import typing
from hashlib import sha256

# Non Standard Library
from yarl import URL

import requests


class HotelBeds():
    supplier = "hotelbeds"

    endpoint = URL("https://api.hotelbeds.com/hotel-content-api/1.0/")

    imagebase = URL("http://photos.hotelbeds.com/giata/original/")

    key = "5c3djnfxkpxuhsd5emcsep6j"
    secret = "Jc25QB5RDP"

    def images(self, images):
        return [str(self.imagebase / img["path"]) for img in images]

    @property
    def signature(self):
        string = "".join([self.key, self.secret, str(int(time.time()))])
        sha = sha256(string.encode("utf8"))
        return sha.hexdigest()

    @property
    def headers(self):
        return {
            "Accept-Encoding": "Gzip",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Signature": self.signature,
            "Api-Key": self.key,
        }

    def fetch(self, types: str = "hotels", code_list: list = []) -> typing.Iterable:
        with requests.Session() as session:
            params = {"language": "ENG", "fields": "all"}
            for code in code_list:
                params['codes'] = str(code)
                response = session.get(
                    str(self.endpoint / types),
                    params=params,
                    headers=self.headers,
                )
                resp = response.json()
                resp = resp.get(types)
                if resp:
                    yield resp
                else:
                    yield [500]

    def hotels(self, code_list: list):
        return [
            hotels[0] for hotels in self.fetch("hotels", code_list)
            ]
