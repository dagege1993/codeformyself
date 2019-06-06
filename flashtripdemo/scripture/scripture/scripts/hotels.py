#!/usr/bin/env python
# coding: utf8

# import os

import yarl
import json
import redis
import uvloop
import asyncio
import logging

from aioutils import Pool
from aiohttp import ClientSession
from googletrans import Translator
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient

from scripture.utils import strip_tags
from scripture.utils.jsetadditional import JsetAdditional

# os.environ['no_proxy'] = '47.94.77.75'
# os.environ['http_proxy'] = 'socks5://127.0.0.1:1080'
# os.environ['https_proxy'] = 'socks5://127.0.0.1:1080'

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

m = MongoClient('mongodb://127.0.0.1:27017')
t = Translator(service_urls=['translate.google.cn'])

_redis = redis.Redis()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.ERROR
    )

log = logging.getLogger('hotel')

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

total = 0

async def translate(text):
    return t.translate(text, dest='zh-CN').text
    # return text

# async def jetsetter(pool):
#     # async for geo in m.jetsetter.geocode.find():
#         # pool.spawn(post_hotel(geo))
#     for jset in _redis.lrange('jetsetter:items', 0, 1000):
#         jset = json.loads(jset)
#         pool.spawn(jset_hotel(jset))

async def rxml(pool):
    async for hotel in mc.scripture.rxmls.find():
        pool.spawn(rxml_hotel(hotel))


def url(url):
    u = yarl.URL(url)
    q = u.query.copy()
    try:
        q.pop('searchGuid')
    except KeyError:
        pass
    return str(u.with_query(q))


async def rxml_hotel(hotel):
    addr = hotel['address']['address1'] or ''
    addr += hotel['address']['address2'] or ''
    addr += hotel['address']['address3'] or ''
    addr += hotel['address']['city'] or ''
    addr += hotel['address']['state'] or ''


async def jset_hotel(jset):
    city = jset['url'].split('/')[4].replace('-', ' ').title()
    if city not in cities:
        return
    if _redis.sadd('jetsetter:posted', jset['jet_id']) == 0:
        return
    geocode = await m.jetsetter.geocode.find_one({'jets_id': jset['jet_id']})
    if not geocode:
        geocode = {}
        hotel_id = ''
    else:
        location = geocode['geometry']['location']
        loc = geocode.get('loc') or [location['lng'], location['lat']]
        xml = await m.roomsxml.geo.find_one(
            {'loc': {'$near': loc, '$maxDistance': 0.00005}},
            {'hotel_id': 1, 'roomsxml_id': 1}
        )
        if xml:
            _id = xml.get('hotel_id') or xml.get('roomsxml_id')
            _hotel_id = await m.roomsxml.hotels.find_one({'_id': _id})
            hotel_id = _hotel_id['hotel_id']
        else:
            hotel_id = ''

    jset['hotel_id'] = hotel_id
    jset.update(geocode)

    return await request(await jset_payload(jset))

async def post_hotel(geo):
    jet = await m.jetsetter.spider.find_one({'jet_id': geo['jets_id']})
    city = jet['url'].split('/')[4].replace('-', ' ').title()
    if city not in cities:
        return
    xml = await m.roomsxml.geo.find_one(
        {'loc': {'$near': geo['loc'], '$maxDistance': 0.00005}},
        {'hotel_id': 1, 'roomsxml_id': 1})
    if xml:
        xml = {}
        _id = xml.get('roomsxml_id') or xml.get('hotel_id')
        hotel = await m.roomsxml.hotels.find_one({'_id': _id})
        if hotel:
            hotel_id = hotel['hotel_id']
        else:
            hotel_id = ''
    else:
        hotel_id = ''
    jet['city'] = city
    jet['hotel_id'] = hotel_id

    return await request(await jet_hotel(jet, geo))

async def jset_payload(jset):
    travel_tips = jset['travel_tips']
    if isinstance(travel_tips, list):
        travel_tips = strip_tags('\n'.join(travel_tips))
        travel_tips_zh = await translate(travel_tips)
        log.warn('list')
    elif isinstance(travel_tips, str) and travel_tips != '':
        travel_tips =  strip_tags(travel_tips)
        travel_tips_zh = await translate(travel_tips)
    else:
        log.warn(f'Unkown type<{type(travel_tips)}> of travel_tips: {jset["url"]}')  # noqa
        travel_tips = ''
        travel_tips_zh = ''
    location = jset.get('geometry', {}).get('location')
    if not location:
        location = {
            'lat': jset['latitude'],
            'lng': jset['longitude']
        }
    addition = JsetAdditional(jset['origin_body'])
    en = {
        'name': jset['name'],
        'address': jset.get(
            'formatted_address', ','.join(jset.get('how_to_get_there'))
        ),
        'introduction': strip_tags('\n'.join(jset['overview'])),
        'recommend_reason': strip_tags('\n'.join(jset['what_we_love'])),
        'info': travel_tips,
        'tips': strip_tags('\n'.join(jset['what_to_know']))
    }
    item = {
        'en': en,
        'city_name': addition.city(),
        'recommend_reason': await translate(en['recommend_reason']),
        'name': await translate(jset['name']),
        'name_en': jset['name'],
        'hotel_id': jset['hotel_id'],
        'address':  await translate(en['address']),
        'latitude': location['lat'],
        'longitude': location['lng'],
        'rating': addition.rating(),
        'comments_url': addition.url(),
        'comments_from': 'TripAdvisor',
        'gallery': addition.images(),
        'capture_url': jset['url'],
        'price': addition.price() or 0,
        'introduction': await translate(en['introduction']),
        'tips': await translate(en['tips']),
        'traffic_info': travel_tips_zh,
    }
    log.error(item['price'])
    return item

async def jet_hotel(jets, geocode):
    travel_tips = jets['travel_tips']
    if isinstance(travel_tips, list):
        travel_tips = strip_tags('\n'.join(travel_tips))
        travel_tips_zh = await translate(travel_tips)
    else:
        travel_tips = ''
        travel_tips_zh = ''
    en = {
        'name': jets['name'],
        'address': geocode['formatted_address'],
        'introduction': strip_tags('\n'.join(jets['overview'])),
        'merchant': '',
        'recommend_reason': strip_tags('\n'.join(jets['what_we_love'])),
        'tips': travel_tips,
        'info': strip_tags('\n'.join(jets['what_to_know']))
    }

    return {
        'name': await translate(jets['name']),
        'name_en': jets['name'],
        'hotel_id': jets['hotel_id'],
        'address':  await translate(geocode['formatted_address']),
        'latitude': geocode['loc'][1],
        'longitude': geocode['loc'][0],
        'ranking': '',
        'rating': '',
        'telephone': '',
        'website': '',
        'price': 0,
        'indtroduction': await translate(en['introduction']),
        'tips': await translate(en['info']),
        'traffic_info': travel_tips_zh,
        'recommend_reason': await translate(en['recommend_reason']),
        'cover_images': '',
        'capture_url': jets['url'],
        'en': en
    }

async def request(payload):
    host = 'http://47.94.77.75/api/v3/hotels'
    # host = 'http://192.168.2.101:8289/api/v3/hotels'
    global total
    async with ClientSession() as request:
        async with request.post(host, json=payload) as resp:
            log.error(await resp.json())
            total += 1
    return 'suc'


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    pool = Pool(10, loop=loop)
    try:
        loop.run_until_complete(jetsetter(pool=pool))
        pool.join()
    except KeyboardInterrupt:
        pass
    log.error(f'Count: {total}')
    # loop.close()
