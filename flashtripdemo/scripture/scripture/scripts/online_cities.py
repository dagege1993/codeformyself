# coding: utf8

import requests
from pymongo import MongoClient
from pypinyin import lazy_pinyin
from datetime import datetime

from scripture import settings

HOST = 'http://47.94.77.75'
CITIES_URI = '/api/v3/cities'

mc = MongoClient(settings.MONGO)


def cities(request=requests):
    data = request.get(HOST + CITIES_URI).json()['data']
    _cities = []
    for continent in data.values():
        for country in continent.values():
            for city in country:
                country_name = city['country']['name']
                _cities.append({
                    'country_code': city['country']['code'],
                    'country_en_name': city['country']['name_en'],
                    'country_zh_name': country_name,
                    'country_pinyin': ' '.join(lazy_pinyin(country_name)),
                    'zh_name': city['name'],
                    'en_name': city['name_en'],
                    'pinyin': ' '.join(lazy_pinyin(city['name'])),
                })

    return _cities


def update(city):
    qualifier = {
        'zh_name': city['zh_name'],
        'country_zh_name': city['country_zh_name']
    }
    mc.scripture.cities.update_one(
        qualifier,
        {
            '$set': city,
            '$setOnInsert': {'created_at': datetime.now()},
            "$currentDate": {'updated_at': True},
        },
        upsert=True
    )

for city in cities():
    update(city)
