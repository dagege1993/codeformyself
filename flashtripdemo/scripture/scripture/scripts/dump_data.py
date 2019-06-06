# coding: utf8
"""
Created by songww
"""

import re
import json
import logging

from typing import Any, Dict, List
from itertools import chain

import pandas
import requests

from yarl import URL
# from lxml.etree import HTML
# from bson import ObjectId
from pymongo import MongoClient

from scripture import settings
from scripture.models.hub_hotel import HubHotel
from scripture.exceptions import HotelNotFound


__all__ = ['published_hotels', 'similarities']

HCOM_ID_RE = re.compile(r'/ho([0-9]+)')
CITY_EN_RE = re.compile(r'([a-zA-Z ]+)')
request = requests.Session()   # pylint: disable=C0103

logging.basicConfig(
    format='%(asctime)s - %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)


def flatten(lists: List[List[Any]]) -> List[Any]:
    """flatten"""
    return list(chain(*lists))


def patch_url(url: str) -> str:
    """patch url of image"""
    return str(URL(url).with_scheme('http').with_host('img3.weegotr.com'))


def gallery(photos: List[Dict[str, str]]) -> List[str]:
    """patch url of images"""
    return [patch_url(photo['url']) for photo in photos]


def checkin_en(dct):
    """checkin time in english"""
    try:
        return next(
            filter(
                lambda key: key.lower().startswith('check-in'),
                dct.get('summary', {}).get('key_facts', [])
            )
        )
    except StopIteration:
        return None
    except TypeError:
        return None


def checkin_zh(dct):
    """checkin time in chinese"""
    try:
        return next(
            filter(
                lambda key: key.startswith('入住时间'),
                dct.get('summary', {}).get('key_facts', [])
            )
        )
    except StopIteration:
        return None
    except TypeError:
        return None


def checkout_en(dct):
    """checkout time in english"""
    try:
        return next(
            filter(
                lambda key: key.lower().startswith('check-out'),
                dct.get('summary', {}).get('key_facts', [])
            )
        )
    except StopIteration:
        return None
    except TypeError:
        return None


def checkout_zh(dct):
    """checkout time in chinese"""
    try:
        return next(
            filter(
                lambda key: key.startswith('退房时间'),
                dct.get('summary', {}).get('key_facts', [])
            )
        )
    except StopIteration:
        return None
    except TypeError:
        return None


title_line = (   # pylint: disable=C0103
    '入住时间(中)',
    '入住时间(英)',
    '退房时间(中)',
    '退房时间(英)',
    '店内服务(中)',
    '店内服务(英)',
    '封面图',
    '图册',
    '酒店ID',
    '酒店名称(中)',
    '酒店名称(英)',
    '城市参考(中)',
    '城市参考(英)',
    'Roomsxml房型参考信息',
    '评论抓取地址'
)

SCRIPTURE_MONGO = 'mongodb://scripture_write:AYDBVmJqXEue353z@dds-2zefca1b050149b42.mongodb.rds.aliyuncs.com:3717,dds-2zefca1b050149b41.mongodb.rds.aliyuncs.com:3717/scripture?replicaSet=mgset-3027583'   # noqa pylint disable=C0301
HUB_MONGO = 'mongodb://hub_write:hvAnfbwByFMG27tT@dds-2zefca1b050149b42.mongodb.rds.aliyuncs.com:3717,dds-2zefca1b050149b41.mongodb.rds.aliyuncs.com:3717/hub?replicaSet=mgset-3027583'   # noqa pylint: disable=C0301
scripture = MongoClient(SCRIPTURE_MONGO).scripture  # pylint: disable=c0103
hub = MongoClient(HUB_MONGO).hub  # pylint: disable=c0103

# documents = [title_line]
#
# cursor = scripture.capture_urls \
#     .find({'hotels_cn_id': {'$exists': True}}) \
#     .sort('$natural', 1)
#
# try:
#     for matched in cursor:
#         hotels_cn_id = matched['hotels_cn_id']
#         hotels_cn = scripture.hotels.find_one({'hotels_id': hotels_cn_id})
#         poi = hub.poi_items.find_one({'hotel_id': matched['hotel_id']})
#         if not poi:
#             print('Bad hotel id', matched['hotel_id'])
#             continue
#         documents.append((
#             checkin_zh(hotels_cn),
#             checkin_en(hotels_cn['en']),
#             checkout_zh(hotels_cn),
#             checkout_en(hotels_cn['en']),
#             flatten(
#                 hotels_cn.get('in_store_service_facilities', {}).values()
#             ),
#             flatten(
#                 hotels_cn['en'] \
#                 .get('in_store_service_facilities', {}) \
#                 .values()
#             ),
#             # flatten(),
#             poi.get('cover_image_url'),
#             gallery(hotels_cn.get('pictures', [])),
#             matched['hotel_id'],
#             hotels_cn['name'],
#             hotels_cn['en']['name'],
#             hotels_cn.get('city') or hotels_cn['name'].split('-')[-1].strip(),
#             hotels_cn['en']['city'],
#             list(poi.get('room_images_ref', {}).values()),
#             hotels_cn.get('tripadvisor')
#         ))
#
# except CursorNotFound:
#     print('Breaked after', len(documents))
# except Exception as exc:
#     print(exc.args)
#     print(len(documents))
#     print(hotels_cn['url'])
#     print(exc.with_traceback())
# else:
#     pandas.DataFrame(documents).to_excel('/home/songww/hotels_cn.xlsx')
#     print('Success', len(documents))


def parse_hcom_id(url):
    u = URL(url)
    return u.query.get('hotel-id') or HCOM_ID_RE.match(u.path).group(1)


def similarities(csvfile: str,
                 output: str = None,
                 sim_db: str = None,
                 loglevel: str = 'DEBUG',
                 url_column: str = 'hotels_URL'):
    """similarities"""

    logger = logging.getLogger('data.dump_similarities')  # noqa pylint: disable=W0621

    logger.setLevel(loglevel.upper())

    m = MongoClient()  # pylint: disable=C0103
    similar_db = m.scripture.get_collection(sim_db)
    mc = MongoClient(settings.MONGO)  # pylint: disable=C0103
    df = pandas.DataFrame.from_csv(csvfile)
    iters = df.iterrows()
    id_hotels_cn = []
    id_city_mapping = {}
    id_comment_mapping = {}
    for city, obj in iters:
        hotels_id = parse_hcom_id(obj[url_column])
        id_hotels_cn.append(hotels_id)
        id_city_mapping[hotels_id] = city
        id_comment_mapping[hotels_id] = obj['TA_url']

    matched = set()
    has_matched = set()
    result = []

    for x in similar_db.find(  # pylint: disable=C0103
        {
            'hotels_id': {'$in': id_hotels_cn},
            'similarity.0.1': {'$gte': 85}
        },
        no_cursor_timeout=True
    ):
        has_matched.add(x['hotels_id'])
        if (x['hotels_id'] + x['similarity'][0][0]) in matched:
            continue
        matched.add(x['hotels_id'] + x['similarity'][0][0])
        h = HubHotel(
            db=mc.scripture,
            hotels_cn_id=x['hotels_id'],
            hotel_id=x['similarity'][0][0],
            comments_url=id_comment_mapping[x['hotels_id']]
        )
        res = h.to_dict()
        res['city'] = id_city_mapping[x['hotels_id']]
        res['hotels_name'] = res['hotels_name'].split('(')[0]
        res['hotels_id'] = x['hotels_id']
        res['url'] = f'https://www.hotels.cn/ho{x["hotels_id"]}'  # noqa

        result.append(res)

    for x in mc.scripture.hotels.find(
        {'hotels_id': {'$in': id_hotels_cn, '$nin': list(has_matched)}},
        no_cursor_timeout=True
    ):
        h = HubHotel(
            db=mc.scripture,
            hotels_cn_id=x['hotels_id'],
            comments_url=id_comment_mapping[x['hotels_id']]
        )
        res = h.to_dict()
        res['city'] = id_city_mapping[x['hotels_id']]
        res['hotels_name'] = res['hotels_name'].split('(')[0]
        res['hotels_id'] = x['hotels_id']
        res['url'] = f'https://www.hotels.cn/ho{x["hotels_id"]}'  # noqa

        result.append(res)

    df = pandas.DataFrame.from_dict(result)
    df.to_excel(
        output,
        columns=[
            'hotel_id',
            'hotels_id',
            'roomsxml_name',
            'roomsxml_address',
            'hotels_name',
            'hotels_name_en',
            'city_name',
            'address',
            'telephone',
            'website',
            'url',
            'comments',
            'comments_from',
            'comments_url',
            'cover_image_url',
            'gallery',
            'introduction',
            'latitude',
            'longitude',
            'price',
            'rank',
            'rating',
            'policy',
            'attractions',
            'facilities',
            'rooms'
        ]
    )


def published_hotels():
    logger = logging.getLogger('data.dumps')
    mc = MongoClient(settings.MONGO)
    hub = MongoClient(settings.HUB_MONGO).hub
    result = []
    for online_hotel in hub.poi_items.find(
        {'__t': 'Hotel', 'published': True},
        no_cursor_timeout=True
    ):
        matched = mc.scripture.capture_urls.find_one({
            'hotel_id': online_hotel['hotel_id']
        })
        if not matched:
            logger.warning('Not matched hotel_id %s', online_hotel['hotel_id'])
            continue
        if not matched.get('hotels_cn_id'):
            logger.debug(
                'Not matched with hotels.cn, %s',
                online_hotel['hotel_id']
            )
            continue
        try:
            h = HubHotel(
                db=mc.scripture,
                hotels_cn_id=matched['hotels_cn_id'].strip(),
                hotel_id=online_hotel['hotel_id'],
                comments_url=online_hotel['comments_url'],
                city=online_hotel.get('city_name')
            )
        except HotelNotFound as e:
            logger.exception(e)
            continue
        res = h.to_dict()
        res['hotels_name'] = res['hotels_name'].split('(')[0]
        res['hotels_id'] = matched['hotels_cn_id']
        res['url'] = 'https://www.hotels.cn/ho' + matched['hotels_cn_id']

        result.append(res)

    df = pandas.DataFrame.from_dict(result)
    df.to_excel(
        '/home/songww/published1.xlsx',
        columns=[
            'hotel_id',
            'hotels_id',
            'roomsxml_name',
            'roomsxml_name',
            'hotels_name',
            'hotels_name_en',
            'city_name',
            'address',
            'telephone',
            'website',
            'url',
            'capture_url',
            'comments',
            'comments_from',
            'comments_url',
            'cover_image_url',
            'gallery',
            'introduction',
            'latitude',
            'longitude',
            'price',
            'rank',
            'rating',
            'policy',
            'attractions',
            'facilities',
            'rooms'
        ]
    )


def givenlist(matches=[], to_excel=''):
    logger = logging.getLogger('data.dumps')
    mc = MongoClient(settings.MONGO)
    hub = MongoClient(settings.HUB_MONGO).hub
    result = []
    for match in matches:
        try:
            h = HubHotel(
                db=mc.scripture,
                hotels_cn_id=match['hotels_cn_id'].strip(),
                hotel_id=match.get('hotel_id'),
                comments_url=match['comments_url'],
                city=match.get('city')
            )
        except HotelNotFound as e:
            logger.exception(e)
            continue
        res = h.to_dict()
        res['hotels_name'] = res['hotels_name'].split('(')[0]
        res['hotels_id'] = match['hotels_cn_id']
        res['url'] = 'https://www.hotels.cn/ho' + match['hotels_cn_id']

        result.append(res)
    __to_excel(result, to_excel)


class Cities(dict):

    @classmethod
    def from_json(cls, jsn_file):
        with open(jsn_file) as fileobj:
            newcls = cls(json.load(fileobj))
        return newcls

    def name(self, city):
        if city in self:
            city = self[city]
        f = self.hub.meta_cities.find_one({'name_en': city})
        return str(f['name'])

    def oid(self, city):
        if city in self:
            city = self['city']
        f = self.hub.meta_cities.find_one({'name_en': city})
        return str(f['_id'])

    @property
    def hub(self):
        if not hasattr(self, '_db'):
            self._db = MongoClient(settings.HUB_MONGO).hub
        return self._db

    @hub.setter
    def hub(self, hub):
        self._db = hub


def excel(infile, outfile, cities=None):
    logger = logging.getLogger('data.dumps.excel')
    scripture = MongoClient(settings.MONGO).scripture
    df = pandas.DataFrame.from_csv(infile)
    keys = df.keys().tolist()
    cities = cities and Cities.from_json(cities) or Cities()
    result = []
    for idx, row in df.iterrows():
        isnull = row.isnull()
        if isnull.ta:
            continue
        bonotel = not isnull.get('bonotel', True) and int(row.bonotel) or None
        roomsxml = not isnull.get('roomsxml', True) and int(row.roomsxml) or None
        hotelspro = not isnull.get('hotelspro', True) and str(row.hotelspro) or None
        hotelbeds = not isnull.get('hotelbeds', True) and int(row.hotelbeds) or None
        jactravel = not isnull.get('jactravel', True) and int(row.jactravel) or None
        city = cities.name(CITY_EN_RE.match(row.city).group(1))
        ta = row.ta
        hcom = row.hotels
        hcom_id = parse_hcom_id(hcom)
        try:
            result.append(
                HubHotel(
                    db=scripture,
                    hotel_id=roomsxml,
                    hotels_cn_id=hcom_id,
                    bonotel=bonotel,
                    hotelspro=hotelspro,
                    hotelbeds=hotelbeds,
                    jactravel=jactravel,
                    comments_url=ta,
                    city=city
                )
            )
        except KeyError as e:
            logger.critical(hcom_id)
            logger.exception(e)
    # mc.scripture
    return __to_excel(result, outfile)


def __to_excel(result, xlsx):
    df = pandas.DataFrame.from_dict(result)
    df.to_excel(
        xlsx,
        columns=[
            'hotel_id',
            'hotels_id',
            'jactravel',
            'bonotel',
            'hotelbeds',
            'hotelspro',
            'roomsxml_name',
            'roomsxml_name',
            'hotels_name',
            'hotels_name_en',
            'city_name',
            'address',
            'telephone',
            'website',
            'url',
            'capture_url',
            'comments',
            'comments_from',
            'comments_url',
            'cover_image_url',
            'gallery',
            'introduction',
            'latitude',
            'longitude',
            'price',
            'rank',
            'rating',
            'policy',
            'attractions',
            'facilities',
            'rooms'
        ]
    )


if __name__ == '__main__':
    logger = logging.getLogger('data.dumps')
