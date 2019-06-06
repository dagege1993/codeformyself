# coding: utf8

import os
import asyncio
from lxml import etree

import phonenumbers as pm

from pycountry import countries

from motor.motor_asyncio import AsyncIOMotorClient as MotorClient


class Room:

    def __init__(self, xml):
        self._xml = etree.fromstring(xml)
        self.__parsed = None
        self._parse()

    def _parse(self):
        self.hotel_id = self._get('/HotelElement/Id')
        self.name = self._get('/HotelElement/Name')
        self.region = {
            'id': self._get('/HotelElement/Region/Id'),
            'name': self._get('/HotelElement/Region/Name'),
            'city_id': self._get('/HotelElement/Region/CityId')
        }
        self.type = self._get('/HotelElement/Type')
        self.country = self._get('/HotelElement/Address/Country')
        tel = self._get('/HotelElement/Address/Tel')
        self.address = {
            'address1': self._get('/HotelElement/Address/Address1'),
            'address2': self._get('/HotelElement/Address/Address2'),
            'address3': self._get('/HotelElement/Address/Address3'),
            'city': self._get('/HotelElement/Address/City'),
            'state': self._get('/HotelElement/Address/State'),
            'zip': self._get('/HotelElement/Address/Zip'),
            'country': self.country,
            'telephone': self._format_telephone(tel),
            'fax': self._get('/HotelElement/Address/Fax'),
            'email': self._get('/HotelElement/Address/Email'),
            'url': self._get('/HotelElement/Address/Url'),
        }
        self.starts = self._get('/HotelElement/Starts')
        self.latitude = self._get('/HotelElement/GeneralInfo/Latitude')
        self.longitude = self._get('/HotelElement/GeneralInfo/Longitude')
        self.photos = [
            {
                'url': self._get('/HotelElement/Photo/Url'),
                'width': self._get('/HotelElement/Photo/Width'),
                'height': self._get('/HotelElement/Photo/Height'),
                'bytes': self._get('/HotelElement/Photo/Bytes'),
                'caption': self._get('/HotelElement/Photo/Caption'),
                'thumbnail_url': self._get('/HotelElement/Photo/ThumbnailUrl'),
                'thumbnail_width': self._get(
                    '/HotelElement/Photo/ThumbnailWidth'),
                'thumbnail_height': self._get(
                    '/HotelElement/Photo/ThumbnailHeight'),
                'thumbnail_bytes': self._get(
                    '/HotelElement/Photo/ThumbnailBytes'),
                'photo_type': self._get('/HotelElement/Photo/PhotoType'),
            }
        ]
        self.description = {
            'language': self._get('/HotelElement/Description/Language'),
            'type': self._get('/HotelElement/Description/Type'),
            'text': self._get('/HotelElement/Description/Text'),
        }
        self.rating = {
            'system': self._get('/HotelElement/Rating/System'),
            'score': self._get('/HotelElement/Rating/Score'),
            'description': self._get('/HotelElement/Rating/Description'),
        }
        self.rank = self._get('/HotelElement/Rank')
        self.__parsed = True

    def _format_telephone(self, tel):
        try:
            cc = countries.get(name=self.country.capitalize()).alpha_2
        except Exception:
            if not self.country:
                return tel
            elif self.country.lower() == 'russia':
                cc = 'RU'
            else:
                return tel
        try:
            return pm.format_number(
                pm.parse(tel, cc),
                pm.PhoneNumberFormat.E164
            )
        except Exception:
            return tel

    def _get(self, xp):
        try:
            return self._xml.xpath(xp)[0].text
        except Exception:
            return ''

    def to_dict(self):
        if not self.__parsed:
            self._parse()
        return {
            'hotel_id': self.hotel_id,
            'name': self.name,
            'region': self.region,
            'type': self.type,
            'address': self.address,
            'starts': self.starts,
            'location': [self.longitude, self.latitude],
            'photos': self.photos,
            'description': self.description,
            'rating': self.rating,
            'rank': self.rank
        }


async def update(queue, loop):
    while loop.is_running():
        item = await queue.get()
        await m.roomsxml.hotels.update_one(
            {'hotel_id': item.hotel_id},
            {'$set': item.to_dict()}
        )
    print('Stopped!')


async def loader(queue, loop):
    path = '/home/songww/文档/hotels'
    for xmlfile in os.listdir(path):
        with open(os.path.join(path, xmlfile)) as xml:
            room = Room(xml.read())
            await queue.put(room)

    print('Empty!')
    await asyncio.sleep(10)
    loop.stop()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    m = MotorClient('mongodb://127.0.0.1:27017')
    q: asyncio.Queue = asyncio.Queue(maxsize=50, loop=loop)
    loop.run_until_complete(asyncio.gather(
        loader(q, loop),
        update(q, loop),
        update(q, loop),
        update(q, loop),
        update(q, loop),
        update(q, loop),
        update(q, loop),
        update(q, loop),
        update(q, loop),
        update(q, loop),
        update(q, loop),
        update(q, loop),
        update(q, loop)
    ))
