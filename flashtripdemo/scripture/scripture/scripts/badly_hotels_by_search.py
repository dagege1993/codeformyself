#! python
# coding: utf8

# import random

import os
import requests

from yarl import URL

from pymongo import MongoClient  # , DESCENDING
from pymongo.errors import CursorNotFound
# from bson import Code

from scripture import settings


local_m = MongoClient()
online_m = MongoClient(settings.MONGO)

ua = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'


def get_addr(address):
    addr = []
    addr.append(address['address1'])
    addr.append(address['address2'])
    addr.append(address['address3'])
    addr.append(address['city'])
    addr.append(address['state'])
    addr.append(address['country'])
    return ', '.join(filter(None, addr))


def get_names(rec):
    names = []
    names.append(rec['name'])
    alias = rec['notice'].get('alias') or []
    names.extend(alias)
    return list(filter(None, names))


def search_by_name(name, city=None, hotel_id=None):
    if 'Formerly' in name:
        n, o = name.split('Formerly')
        return search_by_name(n.strip('()'), city), \
            search_by_name(o.strip('()'), city)
    dest = city and '{} {}'.format(name, city) or name  # x = x ? '1' + x : '1'
    params = {
        'q-destination': dest,
        'as-shown': True,
        'q-rooms': 1,
        'q-room-0-adults': 1
    }
    resp = requests.get(
        'https://www.hotels.cn/search.do',
        params=params,
        headers={'user-agent': ua},
        allow_redirects=False
    )
    if resp.status_code == 200:
        # print(resp.status_code, name, resp.url)
        pass
    elif resp.status_code == 302:
        redirect_uri = resp.headers['Location']
        # print(resp.status_code, redirect_uri)
        if redirect_uri.startswith('/disambiguation.html'):
            # print('Not Found! [', name, ']')
            pass
        elif redirect_uri.startswith(('/hotel/ho', '/hotel/details.html')):
            # print('-->', redirect_uri)
            hotels_id = URL(redirect_uri).query['hotel-id']
            o = os.popen(f'grep -m 1 -h "/ho{hotels_id}/" hotels/*.xml')
            line = o.read()
            try:
                url = line.split('<loc>')[1].split('</loc>')[0]
            except IndexError:
                print('Bad id:', hotels_id, 'Bad line:', line)
                return
            with open('hotelscn_mapping.txt', 'a') as urls:
                wline = hotel_id and f'{hotel_id} {url}\n' or f'{url}\n'
                urls.write(wline)
            o.close()
        else:
            print(resp.status_code, dest, redirect_uri)
    else:
        print('!!Bad', dest, resp.status_code)
    resp.close()


# for rng in range(21):
#     sample_ids = set()
#     _min = rng * 5
#     _max = (rng + 1) * 5
#     c = local_m.scripture.hotelscn_similarities.find({
#         '$and': [
#             {'similarity': {'$ne': []}},
#             {'similarity.0.1': {'$gte': _min}},
#             {'similarity.0.1': {'$lt': _max}}
#         ]
#     })
#     print(f"In range {_min} <= similarity < {_max}:")
#     cnt = c.count()
#     if cnt == 0:
#         print('Amount: 0')
#         continue
#     t = (cnt < 20 and cnt) or 20
#     rand_indexes = random.sample(range(c.count() + 1), t)
#     for idx in rand_indexes:
#         hotels_id = c[idx]['hotels_id']
#         if hotels_id in sample_ids:
#             continue
#         sample_ids.add(hotels_id)
#         h = online_m.scripture.hotels.find_one({'hotels_id': hotels_id})
#         name = h['en']['name']
#         country = h['en']['address'].get('country', h['address']['country'])
#         addr = [
#             h['en']['address']['street'],
#             h['en']['address']['locality'],
#             h['en']['address']['region'],
#             h['en']['address']['postal_code'],
#             country,
#         ]
#         addr = ', '.join(filter(None, addr))
#         print(f"  ID of Hotels.cn: {hotels_id}")
#         print(f"  Address: {addr}")
#         print(f"  Names: {get_names(h['en'])}")
#         similarities = local_m.scripture.hotelscn_similarities \
#             .find({'hotels_id': hotels_id}) \
#             .sort('similarity.0.1', DESCENDING)
#         print(f"  {similarities.count()} Similarities:")
#         for similarity in similarities:
#             for s in similarity['similarity']:
#                 hotel = online_m.scripture.rxmls.find_one({'hotel_id':
#                 str(s[0])})   # noqa
#                 name = hotel.get('name')
#                 print(f'    {s[1]}: {name} | {get_addr(hotel["address"])}')
#
#     print(f"Amount: {len(sample_ids)}")


# goodly = local_m.scripture.hotelscn_similarities.group(
#     ['hotels_id'],
#     {'similarity': {'$ne': []}, 'similarity.0.1': {'$gte': 80}},
#     {},
#     Code('''function(obj, prev) {}''')
# )
# good_hotels = list(map(lambda x: x['hotels_id'], goodly))
# badly = local_m.scripture.hotelscn_similarities.group(
#     ['hotels_id'],
#     {'similarity': {'$ne': []}, 'hotels_id': {'$nin': good_hotels}},
#     {},
#     Code('''function(obj, prev) {}''')
# )
# badly_hotels = list(map(lambda x: x['hotels_id'], badly))
#
# for idx in random.sample(range(len(badly_hotels) + 1), 100):
#     hotels_id = badly_hotels[idx]
#     hotel = online_m.scripture.hotels.find_one(
#         {'hotels_id': hotels_id},
#         {'en': 1}
#     )
#     names = get_names(hotel['en'])
#     addr = [
#         hotel['en']['address']['street'],
#         hotel['en']['address']['locality'],
#         hotel['en']['address']['region'],
#         hotel['en']['address']['postal_code'],
#         hotel['en']['address']['country']
#     ]
#     addr = ', '.join(filter(None, addr))
#     print(f"ID of Hotels.cn: {hotels_id}")
#     print(f"Address: {addr}")
#     print("Names:")
#     for name in names:
#         print(f'    - {name}')
#     addr = ', '.join(filter(None, addr))
#     similarities = local_m.scripture.hotelscn_similarities \
#         .find({'hotels_id': hotels_id}) \
#         .sort('similarity.0.1', DESCENDING)
#
#     print(f"{similarities.count()} Similarities:")
#
#     for similarity in similarities:
#         for s in similarity['similarity']:
#            hotel = online_m.scripture.rxmls.find_one({'hotel_id': str(s[0])})
#             name = hotel.get('name')
#             print(f'    - {s[1]}: {name} | {get_addr(hotel["address"])}')
#         print()


online_cities = dict(
    map(
        lambda c: [c['city_id'], c['en_name']],
        online_m.scripture.cities.find({'city_id': {"$exists": 1}})
    )
)

processed = set()

def do():
    c = online_m.scripture.rxmls.find({
        'region.city_id': {'$in': list(online_cities.keys())},
        'hotel_id': {'$nin': list(processed)}
    })
    # for idx in random.sample(range(c.count() + 1), 100):
    for hotel in c:
        # hotel = c[idx]
        # similarites = local_m.scripture.hotelscn_similarities.find({
        #     'similarity': {
        #         '$elemMatch': {
        #             '$elemMatch': {
        #                 '$in': [hotel['hotel_id']]
        #             }
        #         }
        #     }
        # })
        # t = []
        # for x in similarites:
        #     is_matched = False
        #     for s in x['similarity']:
        #         if s[1] > 80:
        #             # print('Not badly!')
        #             is_matched = True
        #             break
        #         # t.append(s[1])
        #     if is_matched:
        #         break
        #     # else:
        #     #     t.append('')
        # else:
        #     # Is badly
        #     # print('Amount:', similarites.count())
        #     # print('Name:', hotel['name'])
        #     # print('Addr:', get_addr(hotel['address']))
        #     # print('Similarities:')
        #     # for y in t:
        #     #     print('    -', y)
        #     city = None
        #     if len(hotel['name'].split()) == 1:
        #         city = online_cities[hotel['region']['city_id']]
        #     search_by_name(hotel['name'], city)
        city = online_cities[hotel['region']['city_id']]
        search_by_name(hotel['name'], city, hotel['hotel_id'])
        processed.add(hotel['hotel_id'])

def safe_call(func):
    try:
        func()
    except CursorNotFound:
        return safe_call(func)


if __name__ == '__main__':
    safe_call(do)
