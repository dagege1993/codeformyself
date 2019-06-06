# coding: utf8

from __future__ import print_function

from pymongo import MongoClient
from scripture import settings
import Levenshtein

mongo = MongoClient(settings.MONGO)


def fetch_travelzoo():
    return mongo.travelzoo.spider.find(
        {'origin.dct': 'Hotels'},
        {'name': 1}
    )


def fetch_rooms():
    return mongo.roomsxml.hotels.find(
        {},
        {'name': 1, 'latitude': 1, 'longitude': 1, 'address': 1}
    )


def fetch_jetsetter():
    return mongo.jetsetter.spider.find({}, {'name': 1})


def save(room, tzoo):
    return mongo.travelzoo.similar.insert_one({
        'name': room,
        'roomsxml': tzoo
    })

if __name__ == '__main__':
    for room in fetch_travelzoo():
        if 'name' not in room:
            continue
        print('Hotel name:', room['name'])
        names = []
        found = False
        for tzoo in fetch_rooms():
            if 'name' not in tzoo:
                continue
            sim = Levenshtein.ratio(tzoo['name'], room['name'])
            names.append((tzoo['name'], sim))
        k_sim = sorted(names, key=lambda x: x[1], reverse=True)[:10]
        tzoo_names = []
        for k, sim in k_sim:
            tzoo = mongo.travelzoo.spider.find_one(
                {'name': k},
                {'latitude': 1, 'longitude': 1, 'where': 1}
            )
            try:
                lat_ex = abs(float(tzoo['latitude']) - float(room['latitude']))
                lng_ex = float(tzoo['longitude']) - float(room['longitude'])
            except:
                continue
            if lat_ex < 0.01 and abs(lng_ex) < 0.1:
                tzoo_names.append(k)
                found = True
        else:
            if not found:
                z = list(set(list(map(lambda x: x[0], k_sim))))
                save(room['name'], z)
            else:
                save(room['name'], list(set(tzoo_names)))
                found = False
