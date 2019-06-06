#! python
# coding: utf8


from pymongo import MongoClient   # , GEO2D
from scripture import settings

local_mongo = MongoClient('mongodb://127.0.0.1:27017')
ali_mongo = MongoClient(settings.MONGO)

cities = [
    'Amsterdam',
    'Barcelona',
    'Berlin',
    'Boston',
    'Chicago',
    'Hong Kong',
    'Kyoto',
    'London',
    'Los Angeles',
    'Macau',
    'Melbourne',
    'Munich',
    'New York City',
    'Osaka',
    'Paris',
    'Rome',
    'San Francisco',
    'Seattle',
    'Seoul',
    'Singapore',
    'Sydney',
    'Taipei',
    'Tokyo',
    'Washington',
    'Zurich',
]

# for hotel in local_mongo.roomsxml.hotels.find():
#     geocode = local_mongo.roomsxml.geo.find_one({
#         'hotel_id': hotel['_id'],
#         'geometry': {'$exists': True}
#     })
#     if geocode:
#         if 'loc' not in geocode:
#             lat = geocode['geometry']['location']['lat']
#             lng = geocode['geometry']['location']['lng']
#             hotel['loc'] = [lng, lat]
#         hotel['geocode'] = geocode
#     del hotel['_id']
#     ali_mongo.scripture.rxmls.insert_one(hotel)
# for hotel in ali_mongo.scripture.rxmls.find():
#     city = hotel['address']['city']  # .title()
#     if not city:
#         continue
#     city = city.title()
#     fltd = list(filter(lambda x: x in city or city in x, cities))
#     if not fltd:
#         continue
#     del hotel['_id']
#     try:
#         local_mongo.roomsxml.onlines.insert_one(hotel)
#     except:
#         pass


# print(local_mongo.roomsxml.onlines.create_index('hotel_id', unique=True))
# print(local_mongo.roomsxml.onlines.create_index([('loc', GEO2D)]))

# match = 0
# mismatch = 0
# for jset in ali_mongo.scripture.jsets.find():
#     city = jset['name'].split('(')[1].split(',')[0]
#     try:
#         metry = jset['geocode']['geometry']
#         lng = metry['location']['lng']
#         lat = metry['location']['lat']
#         has_same = local_mongo.roomsxml.onlines.find_one({
#             'geocode.loc': [lng, lat]
#             # 'geocode.loc': {
#             #     '$near': [lng, lat],
#             #     '$maxInstance': 0.000001
#             # }
#         })
#     except Exception as e:
#         # try:
#         #     ali_mongo.scripture.jsets.update_one(
#         #         {'jset_id': jset['jset_id']},
#         #         {'$set': {'loc': []}}
#         #     )
#         # except Exception as exc:
#         #     print(exc)
#         print(e)
#         has_same = None
#     if not has_same:
#         mismatch += 1
#     else:
#         match += 1
#         # local_mongo.jsets.lonely.insert_one(jset)
# #     ali_mongo.scripture.jsets.update_one(
# #         {'jset_id': jset['jset_id']},
# #         {'$set': {'loc': [lng, lat]}}
# #     )
# #
# # print(ali_mongo.scripture.jsets.create_index([('loc', GEO2D)]))
# print('Match:', match)
# print('Mismatch:', mismatch)
#
# for hotel in local_mongo.roomsxml.onlines.find():
#     del hotel['_id']
#
#     if 'geocode' in hotel:
#         has_same = ali_mongo.scripture.jsets.find_one({
#             'loc': hotel['geocode']['loc']
#             # 'loc': {
#             #     '$near': hotel['geocode']['loc'],
#             #     '$maxInstance': 0.000001
#             # }
#         })
#     else:
#         has_same = None
#
#     if not has_same:
#         # print('Add', hotel['hotel_id'])
#         local_mongo.rxmls.lonely.insert_one(hotel)
#     else:
#         # print(hotel['hotel_id'])
#         pass
