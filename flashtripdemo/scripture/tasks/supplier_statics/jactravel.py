# coding: utf8

# Standard Library
import time
import typing
from hashlib import sha256
from datetime import datetime
import xml.etree.ElementTree as ET

# Non Standard Library
from yarl import URL

import requests
from tasks.utils.database import databases
from tasks.supplier_statics import Providers, BaseSupplier

class JacTravel(BaseSupplier):

    supplier = Providers.jactravel

    room_meal_entry_point = "http://search.fitruums.com/1/PostGet/NonStaticXMLAPI.asmx"

    user = "WeegoXMLTest"
    pswd = "TestXML2018"

    def room_types(self):
        with requests.Session() as sess:
            params = {
                "userName": self.user,
                "password": self.pswd,
                "language": "en"
            }
            resp = sess.get(f"{self.room_meal_entry_point}/GetRoomTypes", params=params)
            root = ET.fromstring(resp.content.decode('utf-8'))
            scripture = databases("scripture")
            for child in root[0]:
                scripture['statics.hotels.jactravel.roomTypes'].update_one(
                    {'code': str(child[0].text)},
                    {
                        '$set': {
                            'code': str(child[0].text),
                            'id': str(child[0].text),
                            'room_type': str(child[1].text),
                            'sharedRoom': str(child[2].text),
                            'sharedFacilities': str(child[3].text),
                        },
                        "$setOnInsert": {"created_at": datetime.now()},
                        "$currentDate": {"last_modified": True},
                    },
                    upsert=True,
                )

    def meal_types(self):
        with requests.Session() as sess:
            params = {
                "userName": self.user,
                "password": self.pswd,
                "language": "en"
            }
            resp = sess.get(f"{self.room_meal_entry_point}/GetMeals", params=params)
            root = ET.fromstring(resp.content.decode('utf-8'))
            scripture = databases("scripture")
            for child in root[0]:
                datas = {
                    'id': child[0].text,
                    'code': str(child[0].text),
                    'meal_type': child[1].text,
                    'lables': []
                }
                for lable in child[2]:
                    datas['lables'].append({'lable_id': lable[0].text, 'lable_content': lable[1].text})
                scripture['statics.hotels.jactravel.mealTypes'].update_one(
                    {'code': datas['code']},
                    {
                        '$set': datas,
                        '$setOnInsert': {'created_at': datetime.now()},
                        "$currentDate": {"last_modified": True}
                    },
                    upsert=True
                )