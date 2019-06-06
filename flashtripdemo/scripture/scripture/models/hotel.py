# coding: utf8

# from gevent import monkey; monkey.patch_socket()  # noqa

import re
import os

import time
import asyncio
import logging
import requests
import itertools
import functools

import oss2
import aiohttp

from yarl import URL
from pymongo import MongoClient
from lxml.etree import HTML
from w3lib.html import replace_tags
from concurrent.futures import ThreadPoolExecutor

from scripture import settings
from scripture.utils import strip_tags
from scripture.utils.jsetadditional import JsetAdditional
from scripture.models.gallery import Gallery
from scripture.exceptions import *   # noqa

from tasks.tripadvisor import TripAdvisor


logger = logging.getLogger(__name__)


class Hotel:

    def __init__(self, db=None, hotel_id='', jset_id='', hotels_cn_id='',
                 bonotel='', hotelspro='', hotelbeds='',
                 jactravel='', city=None, capture_url=None, comments_url=None,
                 capture_id=None):

        if not hotel_id and not jset_id and not hotels_cn_id:
            raise HotelNotFound('<>')  # noqa

        self.city = city

        self._capture_url_ = capture_url
        self._capture_id = capture_id

        self.db = db or MongoClient(settings.MONGO).scripture

        self.captured_urls_host = 'http://scripture.weegotr.com/captured_from'
        self._doc = {
            'capture_id': capture_id,
            'capture_url': capture_url,
            'hotels_id': hotels_cn_id,
            'quote_ids': []
        }
        if bonotel:
            self._doc['quote_ids'].append(
                {
                    'hotel_id': bonotel,
                    'quoter': '59b20729a389295de92f4952'
                }
            )
        if hotel_id:
            self._doc['quote_ids'].append(
                {
                    'hotel_id': hotel_id,
                    'quoter': '59afe1e0a389295de92f47f8'
                }
            )
        if hotelspro:
            self._doc['quote_ids'].append(
                {
                    'hotel_id': hotelspro,
                    'quoter': '59b0b048a389295de92f4815'
                }
            )
        if hotelbeds:
            self._doc['quote_ids'].append(
                {
                    'hotel_id': hotelbeds,
                    'quoter': '59c1f0f8e1812033000e1de8'
                }
            )
        if jactravel:
            self._doc['quote_ids'].append(
                {
                    'hotel_id': jactravel,
                    'quoter': '59b0b035a389295de92f4814'
                }
            )

        self.__loaded_from_jset = False
        self.__loaded_from_rxml = False
        self.__loaded_from_hotels_cn = False

        self.__comments_url = comments_url

        self._jset_id = jset_id
        self._hotel_id = hotel_id
        self._hotels_cn_id = hotels_cn_id

        if hotel_id:
            self.from_rxml(hotel_id)
        if jset_id:
            self.from_jset(jset_id)
        if hotels_cn_id:
            self.from_hotels_cn(hotels_cn_id)

        if os.environ.get('SCRIPTURE') == 'SANDBOX':
            self.host = 'http://172.17.1.201:8289/api'
        elif os.environ.get('SCRIPTURE') == 'DEV':
            self.host = 'http://10.16.52.40:8289/api'
            # self.host = 'http://192.168.2.101:8289/api/v3'
            # self.host = 'http://192.168.2.167:8289/api/v3'
        else:
            self.host = 'http://172.17.0.212:8289/api'

        self.headers = {'accept-version': '5.0.0'}

    def from_rxml(self, hotel_id):
        hotel = self.db.rxmls.find_one({'hotel_id': hotel_id})
        if not hotel:
            raise RoomsxmlNotFound(hotel_id)  # noqa

        self._doc['hotel_id'] = hotel_id
        self.__loaded_from_rxml = True
        if self.__loaded_from_jset:
            return
        self._doc['city_name'] = self.city or hotel['address']['city']
        self._doc['address'] = self.get_address(hotel)
        self._doc['latitude'] = hotel['latitude']
        self._doc['longitude'] = hotel['longitude']
        self._doc['rank'] = hotel['rank']
        self._doc['roomsxml_name'] = hotel['name']
        self._doc['roomsxml_address'] = self._doc['address']
        self._doc['name'] = hotel['name']
        self._doc['name_en'] = hotel['name']
        self._doc['introduction'] = strip_tags(
            hotel['description']['text'])
        if not self._capture_id:
            self._doc.update(
                self.capture_url(hotel_id=hotel_id, jset_id=self._jset_id)
            )

        u = self.telephone_and_website(
            self._doc['capture_id'],
            ', '.join([self._doc['name'], self._doc['address']])
        )
        if u:
            logger.debug(u)
            self._doc.update(u)
        else:
            logger.debug(
                'Bad telephone and website, %s',
                self._doc['address']
            )

    def from_jset(self, jset_id):
        jset = self.db.jsets.find_one({'jset_id': jset_id})
        if not jset:
            raise JsetNotFound(jset_id)  # noqa

        intro = strip_tags(jset['overview'])
        tips = strip_tags(jset['what_to_know'])
        recommend = strip_tags(jset['what_we_love'])
        travel_tips = strip_tags(jset['travel_tips'])
        if isinstance(travel_tips, list):
            travel_tips = '\n'.join(travel_tips)

        add = JsetAdditional(jset['origin_body'])

        location = jset.get('geocode', {}).get('geometry', {}) \
            .get('location', {})

        self._doc['en'] = {
            'name': jset['name'].split('(')[0].strip(),
            'address': self.get_address(jset),
            'introduction': '\n'.join(intro),
            'recommend_reason': '\n'.join(recommend),
            'info': travel_tips,
            'tips': '\n'.join(tips),
        }

        self._doc['city_name'] = self.city or add.city()
        self._doc['recommend_reason'] = recommend
        self._doc['jset_name'] = self._doc['en']['name']
        self._doc['jset_name_en'] = self._doc['en']['name']
        self._doc['name'] = self._doc['en']['name']
        self._doc['name_en'] = self._doc['en']['name']
        self._doc['address'] = self._doc['en']['address']
        self._doc['latitude'] = location.get('lat') or jset['latitude']
        self._doc['longitude'] = location.get('lng') or jset['longitude']
        self._doc['rating'] = add.rating()
        self._doc['comments_url'] = self.__comments_url or add.url()
        self._doc['comments_from'] = 'TripAdvisor'
        self._doc['gallery'] = add.images()
        self._doc['cover_image_url'] = self._doc['gallery'][0]['image_url']
        if not self._capture_id:
            self._doc.update(self.capture_url(jset_id=jset_id))
        self._doc['price'] = add.price() or 0
        self._doc['introduction'] = intro
        self._doc['tips'] = tips
        self._doc['traffic_info'] = travel_tips
        self._doc['jset_id'] = jset_id

        self.__loaded_from_jset = True

        u = self.telephone_and_website(
            self._doc['capture_id'],
            self._doc['address']
        )

        if u:
            logger.debug(u)
        else:
            logger.debug(
                'Bad telephone and website, %s',
                self._doc['address']
            )
        self._doc.update(u)

    def from_hotels_cn(self, hotels_cn_id):

        def format_address(address):
            addr = [
                address['street'],
                address['locality'],
                address['region'],
                address['postal_code'],
                address['country']
            ]
            return ', '.join(filter(None, addr))

        def format_comments(comments):
            return [
                {
                    'description': comm['description'],
                    'locale': 'en',
                    'published_at': comm['reviewDate'],
                    'published_by': comm['reviewerName'],
                    'rating': comm['rating'],
                    'title': comm['summary']
                } for comm in comments if comm['rating'] >= 3
            ]

        def format_image_url(url):
            u = URL(url).with_host('img1.weegotr.com') \
                .with_scheme('http')
            return str(u)

        hotels = self.db.hotels.find_one({'hotels_id': hotels_cn_id})
        if not hotels:
            raise HotelNotFound(f'Hotels.cn<{hotels_cn_id}>')  # noqa
        self._doc['city_name'] = self.city or \
            hotels.get('city') or \
            hotels['address'].get('city')
        self._doc['hotels_name'] = hotels['name'] \
            .rsplit('-', 1)[0] \
            .strip() \
            .split('(')[0] \
            .strip()
        self._doc['hotels_name_en'] = hotels['en'] \
            .get('name', '') \
            .rsplit(',', 1)[0]
        if not self._doc['hotels_name_en']:
            logger.warning(
                'English name of HCOM %s is empty',
                hotels['hotels_id']
            )
        self._doc['name'] = self._doc['hotels_name'].split('(')[0]
        self._doc['name_en'] = self._doc['hotels_name_en']
        self._doc['address'] = format_address(hotels['en']['address'])
        self._doc['comments_url'] = self.__comments_url or \
            hotels.get('tripadvisor')
        _comments = format_comments(hotels['reviews']['TripAdvisor'])
        _rating = hotels.get('rating')
        if not _comments or not _rating:
            try:
                scripture = requests.get(
                    'http://scripture.weegotr.com/api/v1/comments/ta',
                    params={'url': self._doc['comments_url']}
                ).json()
                scripture['comments']
            except Exception as e:
                logger.error(
                    'Failed to fetch comments of %s from %s',
                    hotels.get('hotels_id'),
                    self._doc['comments_url']
                )
                # raise e
                scripture = {}
        self._doc['comments'] = _comments or scripture.get('comments')
        self._doc['comments_from'] = 'TripAdvisor'
        self._doc['rating'] = _rating or scripture.get('average_rating')
        self._doc['price'] = hotels.get('price', 0)
        pictures = hotels.get('pictures', hotels['en'].get('pictures', []))
        with ThreadPoolExecutor(max_workers=100) as executor:
            self._doc['gallery'] = list(
                executor.map(
                    lambda pic: Gallery(format_image_url(pic['url'])),
                    pictures,
                    chunksize=100
                )
            )
        if not self._doc['gallery']:
            logger.warn('Gallery of %s is empty', hotels['hotels_id'])
        else:
            self._doc['cover_image_url'] = self._doc['gallery'][0]['image_url']
        if not self._capture_id:
            self._doc.update(self.capture_url(hotels_cn_id=hotels_cn_id))
        try:
            self._doc['latitude'] = hotels['latitude']
            self._doc['longitude'] = hotels['longitude']
        except KeyError:
            logger.warning(
                'latitude or longitude is missing. %s',
                hotels_cn_id
            )
        self._doc['hotels_en'] = {
            'name': self._doc['hotels_name_en'],
            'address': format_address(hotels['en']['address'])
        }
        self._doc['en'] = self._doc['hotels_en']
        self._doc['services'] = '\n'.join(
            itertools.chain(
                *hotels.get('in_store_service_facilities', {}).values()
            )
        )
        chkin = list(filter(
            lambda key: key.startswith('入住时间'),
            hotels.get('summary', {}).get('key_facts') or []
        ))
        chkout = list(filter(
            lambda key: key.startswith('退房时间'),
            hotels.get('summary', {}).get('key_facts') or []
        ))

        _other_fees = '\n'.join(hotels['notice'].get('其它费用') or []).strip()
        _man_fees = '\n'.join(hotels['notice'].get('强制消费') or []).strip()

        self._doc['policy'] = [
            {
                'type': '入住政策',
                'content': '\n'.join([
                    chkin[0] if chkin else '',
                    chkout[0] if chkout else ''
                ])
            }
        ]
        if _other_fees:
            self._doc['policy'].append({
                'type': '其它费用', 'content': _other_fees
            })
        if _man_fees:
            self._doc['policy'].append({
                'type': '强制消费', 'content': _man_fees
            })

        def format_attraction(attraction):
            try:
                name, distance = attraction.split('(', 1)
            except ValueError:
                name = attraction
                distance = ''
            return {
                'name': name.strip(),
                'distance': distance.strip(')').strip()
            }

        self._doc['attractions'] = [
            att for att in [
                format_attraction(around) for around in hotels.get('around', [])
            ]
            if att
        ]

        self._doc['facilities'] = [
            {'facility': facility} for facility in hotels.get('amenities', [])
        ]

        # self._doc['transport'] = hotels['summary'].get('transport')
        self._doc['traffic_info'] = []

        self._doc['rooms'] = [
            HcomRoom(room, self.db)
            for room in self.db.hcom.zh.rooms.find({'hcom_id': hotels_cn_id})
        ]

        self.__loaded_from_hotels_cn = True

        self._doc['telephone'] = hotels.get('telephone')
        try:
            u = self.telephone_and_website(
                self._doc['capture_id'],
                ', '.join([self._doc['name'], self._doc['address']])
            )
        except Exception:
            u = {}
        if not u or not u['telephone'] or not u['website']:
            c = {}
            ta = TripAdvisor(self._doc['comments_url'])
            website = u.get('website') or ta.website()
            if website:
                c['website'] = website
                logger.debug('Website from tripadvisor %s', c['website'])
            tel = hotels.get('telephone') or u.get('telephone') \
                or ta.telephone()
            if tel:
                c['telephone'] = tel
                logger.debug(
                    'Telephone from tripadvisor %s',
                    c['telephone']
                )
            if not c:
                logger.debug(
                    'Bad telephone and website, %s',
                    self._doc['address']
                )
                self.db.contacts.delete_one({
                    'crawled_id': self._doc['capture_id']
                })
            else:
                logger.debug(c)
                c['crawled_id'] = self._doc['capture_id']
                self.db.contacts.update_one(
                    {'crawled_id': self._doc['capture_id']},
                    {
                        '$set': c
                    },
                    upsert=True
                )
            if c:
                self._doc.update(c)
        else:
            self._doc.update(u)

        self._doc['hotels_cn_id'] = hotels_cn_id
        self._doc['url'] = f'https://www.hotels.cn/ho{hotels_cn_id}'
        self._doc['hotels_cn_url'] = self._doc['url']

    def to_json(self):
        try:
            import ujson as json
        except ImportError:
            import json

        return json.dumps(self._doc)

    def to_dict(self, columns=[]):
        if columns and isinstance(columns, (list, tuple)):
            if 'capture_url' not in columns:
                columns.append('capture_url')
            if 'capture_id' not in columns:
                columns.append('capture_id')

            return {
                key: value
                for key, value in self._doc.items()
                if key in set(columns)
            }
        return self._doc

    async def to_hub(self, columns=None):
        if not columns:
            columns = []
        jsn = self.to_dict(columns).copy()
        jsn['name'] = jsn.get('hotels_name') \
            or jsn.get('jset_name')  \
            or jsn.get('roomsxml_name')
        jsn['name_en'] = jsn.get('hotels_name_en') \
            or jsn.get('jset_name_en') \
            or jsn.get('roomsxml_name')
        jsn.pop('rooms')
        host = self.host + '/hotels'
        logger.debug(f'Destination {host} with Json({jsn})')
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(host, json=jsn) as resp:
                return await resp.text()

    async def to_hub_hotel(self, columns=[]):
        jsn = self.to_dict(columns)
        capture_id = self._doc['capture_id']
        host = self.host + f'/hotels/{capture_id}'
        logger.debug(f'Destination {host} with Json({jsn})')
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.put(host, json=jsn) as resp:
                return await resp.text()

    async def to_hub_hotelroom(self):
        jsn = self.to_dict(columns=['rooms', 'hotel_id'])
        capture_id = jsn.get('capture_id')
        host = self.host + f'/hotels/hotelrooms/{capture_id}'
        for room in jsn['rooms']:
            logger.debug(
                f'Destination {host} with RoomName({room["room_type"]})')
        logger.debug(f'Destination {host} with Json({jsn})')
        params = {'capture_id': capture_id}
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(host, params=params, json=jsn) as resp:
                return await resp.text()

    def _capture_url(self, *, jset_id=None, hotel_id=None, tzoo_id=None,
                     ta_id=None, booking_id=None, hotels_cn_id=None):
        if jset_id:
            return self.db.jsets.find_one({'jset_id': jset_id})['url']
        if hotel_id:
            return '{}/id/{}'.format(self.captured_urls_host, hotel_id)
        if tzoo_id:
            return '{}/tzoo/{}'.format(self.captured_urls_host, tzoo_id)
        if ta_id:
            return '{}/ta/{}'.format(self.captured_urls_host, ta_id)
        if booking_id:
            return '{}/booking/{}'.format(self.captured_urls_host, booking_id)
        if hotels_cn_id:
            return '{}/hotelscn/{}'.format(
                self.captured_urls_host,
                hotels_cn_id
            )

    def capture_url(self, *, hotel_id=None, jset_id=None, tzoo_id=None,
                    ta_id=None, booking_id=None, hotels_cn_id=None):

        kwargs = {
            'hotel_id': hotel_id or self._hotel_id,
            'jset_id': jset_id,
            'tzoo_id': tzoo_id,
            'ta_id': ta_id,
            'booking_id': booking_id,
            'hotels_cn_id': hotels_cn_id
        }

        url_find = self.db.capture_urls.find_one
        url_update = self.db.capture_urls.update_one
        url_insert = self.db.capture_urls.insert_one

        found = url_find({
            '$or': [
                {k: {'$eq': v, '$exists': 1}}
                for k, v in kwargs.items()
                if v
            ]
        })

        kw = {k: v for k, v in kwargs.items() if v}

        if found:

            kw = {k: v for k, v in kw.items() if found.get(k) != v}

            kw != {} and url_update({'_id': found['_id']}, {'$set': kw})
            captured_id = str(found['_id'])
            url = f'http://scripture.weegotr.com/api/v1/crawled/{captured_id}'
            items = {
                'capture_url': self._capture_url_ or url,
                'capture_id': captured_id
            }
            logger.debug('Found %s, by %s, %s', items, kwargs, found)
            return items

        oid = url_insert(kw)
        captured_id = str(oid.inserted_id)
        url = f'http://scripture.weegotr.com/api/v1/crawled/{captured_id}'
        items = {
            "capture_url": self._capture_url_ or url,
            'capture_id': captured_id
        }
        logger.debug("Create %s", items)
        return items

    def get_address(self, doc):
        geocode = doc.get('geocode')
        if geocode \
                and (geocode.get('partial_match') is not True) \
                and 'formatted_address' in geocode:
            return geocode['formatted_address']
        address = doc.get('address')
        if not address:
            return None

        if isinstance(address, list):
            return ''.join(address[1:])

        if isinstance(address, dict):
            addr = []
            addr.append(address['address1'])
            addr.append(address['address2'])
            addr.append(address['address3'])
            return ', '.join(filter(None, addr))

    def telephone_and_website(self, crawled_id, addr, retry=False):
        # return {}
        contact = self.db.contacts.find_one({'crawled_id': crawled_id})
        if contact:
            return {
                'website': contact['website'],
                'telephone': contact['telephone']
            }
        try:
            resp = session.get(
                'https://www.google.com.sg/search',
                params={
                    'q': addr,
                    'hl': 'zh-CN'
                },
                headers={
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36'  # noqa
                },
                proxies={
                    'http': 'http://172.17.1.198:1118',
                    'https': 'http://172.17.1.198:1118'
                }
            )
        except requests.exceptions.ProxyError as exc:
            logger.error(
                'crawled_id %s addr %s retry %s Exception %s',
                crawled_id,
                addr,
                retry,
                exc
            )
            return
        if resp.status_code != 200:
            logger.error('Bad status:', resp.status_code)
            resp.close()
            return

        html = HTML(resp.text)
        telephone = html.xpath('//span[starts-with(text(), "+")]/text()')
        website = html.xpath('//a[contains(text(), "Website") or contains(text(), "网站")]/@href')  # noqa
        resp.close()
        tel = telephone and telephone[0] or ''
        site = website and website[0] or ''
        if not tel and not site and not retry:
            return self.telephone_and_website(
                crawled_id, addr.split(',')[0], retry=True)
        self.db.contacts.insert_one({
            'telephone': tel, 'website': site, 'crawled_id': crawled_id
        })
        contact = {'telephone': tel, 'website': site}
        time.sleep(1)
        return contact


class HcomRoom(dict):

    __ZH_KEY_MAPPING = {
        '舒适设施/服务': 'serve',
        '实用': 'useful',
        '网络': 'network',
        '娱乐': 'recreation',
        '餐饮': 'dining',
        '浴室': 'bathroom'
    }

    __EN_KEY_MAPPING = {
        'Practical': 'useful',
        'Comfort': 'serve',
        'Internet': 'network',
        'Entertainment': 'recreation',
        'Food & Drink': 'dining',
        'Bathroom': 'bathroom'
    }

    _RE_ROOM_SIZE = re.compile('(平方米|平方英尺|-sq-foot|-sq-meter)')

    def __init__(self, doc, db):
        self.db = db
        self.hcom_id = doc.get('hcom_id', '')
        self['capture_id'] = str(doc['_id'])
        self['room_type'] = doc['name'].split('(')[0]
        self['occupancy_info'] = doc['occupancy']
        self['room_size'] = self.get_roomsize(doc['description'][:2])
        if 'bed_types_str' in doc:
            self['bed_type'] = doc['bed_types_str']
        elif doc['description']:
            self['bed_type'] = self.get_bedtype(
                doc['description'][0],
                doc['bed_types']
            )
        else:
            self['bed_type'] = ''
        self['bed_size'] = self.format_bedsize(doc['bed_metrics'])
        self['room_desc'] = '\n'.join(doc['description'])
        self['facilities'] = [{'facility': value} for value in doc['amenities']]

        with ThreadPoolExecutor(max_workers=100) as executor:
            self['gallery'] = list(
                executor.map(
                    lambda img: Gallery(img['url']),
                    doc['images']
                )
            )
        self['add_bed_type'] = [
            {'type': extra['type'], 'size': extra['metric']}
            for extra in doc['bed_extra_types']
        ]
        try:
            self['room_type_en'] = self.get_en_name(doc['room_type_code'])
        except KeyError:
            logger.error('room_type_code dosent exits, %s', self['capture_id'])
        self.update(self.service(doc['description']))

    def get_roomsize(self, desc):
        for line in desc:
            if self._RE_ROOM_SIZE.search(line):
                return line
        return ''

    def get_bedtype(self, desc, types=[]):
        if list(filter(lambda t: t in desc, types)):
            return desc
        if '单人床' in desc or '双人床' in desc or '大床' in desc:
            return desc
        return ''

    def get_en_name(self, room_code):
        room = self.db.hcom.en.rooms.find_one({
            'hcom_id': self.hcom_id,
            'room_type_code': room_code
        })
        return room.get('name', '') if room else ''

    def format_bedsize(self, bedsize):
        if not bedsize:
            return ''
        return replace_tags(bedsize, '\n')

    def service(self, desc):
        _srvs = {}
        for d in desc:
            try:
                _key, value = d.split('-')
            except Exception:
                continue
            key = self.__ZH_KEY_MAPPING.get(_key.strip()) or \
                self.__EN_KEY_MAPPING.get(_key.strip())
            if not key:
                continue
            _srvs[key] = value
        return _srvs
