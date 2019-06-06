#!python
# coding: utf8

from pymongo import MongoClient
from lxml import etree

mongo = MongoClient('mongodb://localhost:27017')

db = mongo.jetsetter
id_column = 'jets_id'
# db = mongo.travelzoo
# id_column = 'tzoo_id'

# found = 0
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

# cities = [city.lower() for city in cities]


def get_tag(h):
    t = h.xpath('//div[@id="product-gallery"]/div/div[@class="property-header"]/div[@class="property-market-category"]/div/text()')
    if t:
        return t[0]
    return ''


def get_name(h):
    name = h.xpath('//div[@id="product-gallery"]/div/div[@class="property-header"]/h1/text()')
    if name:
        return name[0]
    return ''


def get_rating(h):
    rating = h.xpath('//div[@id="at-a-glance"]/div/div[@class="reviews-preview"]/div[@class="ta-rating-summary"]/div[@class="rating"]/text()')
    if rating:
        return rating[0]
    return ''


xyz = []

for hotel in db.spider.find():
    geo = db.geocode.find_one(
        {id_column: hotel[id_column]}, {'loc': 1}
    )
    if not geo:
        # print('Geocode is empty:', hotel['tzoo_id'])
        continue
    rx_id = mongo.roomsxml.geo.find_one(
        # {'loc': {'$near': geo['loc'], '$maxDistance': 0.00001}}
        {'loc': {'$near': geo['loc'], '$maxDistance': 0.0001}}
        # {'loc': geo['loc']}
    )
    if not rx_id:
        # print('Not found', hotel['tzoo_id'])
        continue
    # rx = mongo.roomsxml.hotels.find_one({'_id': rx_id['roomsxml_id']})
    # print('Found', rx['name'])
    # found += 1
    city = hotel['url'].split('/')[4].replace('-', ' ').title()
    if city not in cities:
        continue
    html = etree.HTML(hotel['origin_body'])
    xyz.append({
        'city': city,
        'tag': get_tag(html),
        'name': get_name(html),
        'rating': get_rating(html)
    })

import pandas
pandas.DataFrame(xyz).to_excel('jset.xlsx')
