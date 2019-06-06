#! python
# coding: utf8

import phonenumbers as pm
from pymongo import MongoClient
from pycountry import countries

mongo = MongoClient('mongodb://127.0.0.1:27017')


for h in mongo.roomsxml.hotels.find({'address.telephone': {'$exists': True}}):
    try:
        cn = countries.get(name=h['address']['country'].capitalize()).alpha_2
    except KeyError as e:
        print(e)
        continue
    try:
        tel = pm.format_number(
            pm.parse(h['address']['telephone'], cn),
            pm.PhoneNumberFormat.E164
        )
    except pm.phonenumberutil.NumberParseException:
        print('Bad telephone:', h['address']['telephone'])
        continue
    t = mongo.roomsxml.hotels.update_one(
        {'hotel_id': h['hotel_id']},
        {'$set': {'company.telephone': tel}}
    )
