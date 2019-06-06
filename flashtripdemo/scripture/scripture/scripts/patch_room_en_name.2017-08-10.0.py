# coding: utf8

from collections import Counter, defaultdict

from bson import ObjectId
from pymongo import MongoClient

from scripture import settings

hub = MongoClient(settings.HUB_MONGO).hub
scripture = MongoClient(settings.MONGO).scripture


hotels = Counter()
cursor = hub.poi_hotel_rooms.find(
    {'capture_id': {'$exists': 1}, 'room_type_en': {'$eq': ''}},
    no_cursor_timeout=True
)

for room in cursor:
    hotels[str(room['hotel'])] += 1


def get_en_name(code, en):
    for en_room in en:
        if en_room['room_type_code'] == code:
            return en_room['name']


changed = defaultdict(list)
for hotel, _ids in hotels.items():
    try:
        _id = hub.poi_items.find_one({'_id': ObjectId(hotel)})['capture_id']
    except Exception:
        continue
    hcom_id = scripture.capture_urls \
        .find_one({'_id': ObjectId(_id)})['hotels_cn_id']
    hcom = scripture.hotels.find_one({'hotels_id': hcom_id})
    if not hcom:
        print('Empty hcom', hcom_id)
        continue
    ccnt = 0
    for room in hcom.get('rooms', []):
        if 'room_type_code' not in room:
            print('Bad room', room['_id'])
        elif str(room['_id']) in _ids:
            room_type_en = get_en_name(
                room['room_type_code'],
                hcom['en'].get('rooms', [])
            )
            if room_type_en:
                changed[str(hcom['_id'])].append(str(room['_id']))
                u = hub.poi_hotel_rooms.update_one(
                    {'capture_id': str(room['_id'])},
                    {'$set': {'room_type_en': room_type_en}}
                )
                print(u.raw_result)
            else:
                print('Not found', room['_id'])
        else:
            print('New', room['_id'])
