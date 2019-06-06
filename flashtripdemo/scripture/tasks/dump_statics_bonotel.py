# coding: utf8

import csv
import enum
import json
import asyncio
import pathlib

from datetime import datetime

import uvloop
from yarl import URL
from lxml import objectify, etree
from aiohttp import ClientSession, BasicAuth

from motor.motor_asyncio import AsyncIOMotorClient as AioMotorClient
from pymongo.database import Database


class Providers(enum.Enum):
    bonotel = 'bonotel'
    roomsxml = 'roomsxml'
    hotelbeds = 'hotelbeds'
    hotelspro = 'hotelspro'
    jactravel = 'jactravel'


def ensure_can_be_serialized(value):
    if value is None:
        return None
    if isinstance(value, dict):
        return {k: ensure_can_be_serialized(v) for k, v in value.items()}
    elif isinstance(value, (tuple, list)):
        return [ensure_can_be_serialized(v) for v in value]
    elif isinstance(value, (str, bytes, float, int, datetime)):
        return value
    else:
        return value.text
    return value


class BaseStatics(object):
    db: Database
    username: str
    provider: Providers
    endpoint: URL
    collection: str

    def __init__(self, db):
        self.db = db
        self.table = self.db.get_collection(self.collection)

    async def save_if_not_exists(self, document):
        doc = ensure_can_be_serialized(document)

        has = await self.table.find_one({'code': doc['code']}, {})
        if has:
            return

        return self.pprint(await self.table.insert_one(doc))

    def pprint(self, result):
        result = {
            attr: getattr(result, attr)
            for attr in dir(result)
            if not attr.startswith('_')
        }
        print(json.dumps(result, indent=2, default=repr))
        return True


class DumpStaticsBonotel(BaseStatics):
    username = 'weegoLive_xml'

    provider = Providers.bonotel

    collection = 'statics.hotels.bonotel'

    endpoint = URL(
        'http://api.bonotel.com/index.cfm/user/weegoLive_xml/action'
    )

    async def regions(self):
        endpoint = 'http://api.bonotel.com/XMLCache/region0.xml'
        async with ClientSession() as request:
            async with request.get(endpoint) as response:
                xml = await response.text()
        countries = objectify.fromstring(xml.encode())
        for country in countries.country:
            country_code = country.countryCode
            country_name = country.countryName
            for state in country.state:
                state_code = state.state_code
                state_name = state.state_name
                for city in state.city:
                    print({
                        'country_code': country_code,
                        'country_name': country_name,
                        'state_code': state_code,
                        'state_name': state_name,
                        'city_code': city.city_code,
                        'city_name': city.city_name,
                    })

    async def hotels(self):
        # endpoint = 'http://api.bonotel.com/XMLCache/hotelAll0.xml'
        # async with ClientSession() as request:
        #     async with request.get(endpoint, timeout=600) as response:
        #         xml = await response.text()
        try:
            # hotels = objectify.fromstring(xml.encode())
            with open('/tmp/bonotel.xml', 'r') as xml:
                hotels = objectify.fromstring(xml.read().encode())
        except etree.XMLSyntaxError as exc:
            print('SyntaxError', exc)
            # with open('/tmp/bonotel.xml', 'w') as b:
            #     b.write(xml)
            return
        for hotel in hotels.hotel:
            doc = {
                'code': hotel.hotelCode,
                'name': hotel.name,
                'address': hotel.address,
                'address2': hotel.address2,
                'city': {
                    'name': hotel.city,
                    'code': hotel.cityCode,
                },
                'state': {
                    'name': hotel.state,
                    'code': hotel.stateCode,
                },
                'country': {
                    'name': hotel.country,
                    'code': hotel.countryCode,
                },
                'postal_code': hotel.postalCode,
                'phone': hotel.phone,
                'fax': hotel.fax,
                'latitude': hotel.latitude,
                'longitude': hotel.longitude,
                'rating': hotel.starRating,
                'images': [image for image in hotel.images.image],
                'cancel_policies': hotel.cancelPolicies,
                'limitation_policies': hotel.limitationPolicies,
                'description': hotel.description,
                'facilities': hotel.facilities,
                'recreation': hotel.recreation
            }

            await self.save_if_not_exists(doc)


class DumpStaticsRXML(BaseStatics):

    collection = 'statics.hotels.roomsxml'

    @classmethod
    def address(cls, address1, address2, address3):
        _addr = []
        if address1:
            _addr.append(address1.text)
        if address2:
            _addr.append(address2.text)
        if address3:
            _addr.append(address3.text)
        addr = ','.join(_addr)
        addr.strip(',')
        return addr

    @classmethod
    def images(cls, elements):
        imgs = []
        for image in elements:
            imgs.append(f'www.roomsxml.com{image.Url.text}')
        return imgs

    @classmethod
    def descriptions(cls, elements):
        descs = []
        for desc in elements:
            if desc.Text:
                descs.append(desc.Text.text)
        return '\n'.join(descs)

    @classmethod
    def amenities(cls, elements):
        _amenities = []
        for amenity in elements:
            _amenities.append(amenity.Text)
        return _amenities

    @classmethod
    def rating(cls, elements):
        return ' '.join([elements.Score.text, elements.System.text])

    async def hotels(self):
        xmldir = '/home/songww/HotelDetailXML'
        d = pathlib.Path(xmldir)
        for xmlfile in d.glob('*.xml'):
            hotel = objectify.fromstring(xmlfile.read_bytes())
            h = {
                'code': hotel.Id,
                'name': hotel.Name,
                'region': {
                    'code': hotel.Region.Id,
                    'name': hotel.Region.Name
                },
                'city': {
                    'code': hotel.Region.CityId,
                    'name': hotel.Address.City
                },
                'state': {
                    'name': hotel.Address.State
                },
                'country': {
                    'name': hotel.Address.Country
                },
                'type': hotel.Type,
                'address': self.address(
                    hotel.Address.Address1,
                    hotel.Address.Address2,
                    hotel.Address.Address3
                ),
                'postal_code': hotel.Address.Zip,
                'phone': hotel.Address.Tel,
                'fax': hotel.Address.Fax,
                'email': hotel.Address.Email,
                'website': hotel.Address.Url,
                'rank': hotel.Rank
            }
            try:
                h['amenities'] = self.amenities(hotel.Amenity)
            except AttributeError:
                pass
            try:
                h['images'] = self.images(hotel.Photo)
            except AttributeError:
                pass
            try:
                h['description'] = self.descriptions(hotel.Description)
            except AttributeError:
                pass
            try:
                h['latitude'] = hotel.GeneralInfo.Latitude
                h['longitude'] = hotel.GeneralInfo.Longitude
            except AttributeError:
                pass
            try:
                h['stars'] = hotel.Stars
            except AttributeError:
                pass
            try:
                h['rating'] = self.rating(hotel.Rating)
            except AttributeError:
                pass

            await self.save_if_not_exists(h)


class DumpStaticsIvector(BaseStatics):

    collection = 'statics.hotels.jactravel'

    async def hotels(self):
        with open('/home/songww/下载/Property.txt') as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter='|')
            for row in csvreader:
                doc = {
                    'code': row['PropertyReferenceID'],
                    'name': row['PropertyName'],
                    'city': {
                        'name': row['TownCity']
                    },
                    'country': {'name': row['Country']},
                    'address': row['Address1'],
                    'address2': row['Address2'],
                    'postal_code': row['PostcodeZip'],
                    'phone': row['Telephone'],
                    'fax': row['Fax'],
                    'latitude': row['Latitude'],
                    'longitude': row['Longitude'],
                    'region': row['Region'],
                    'type': row['PropertyType'],
                    'rating': row['Rating'],
                    'images': [
                        row[f'Image{x}URL'] for x in range(1, 11)
                        if row[f'Image{x}URL']
                    ],
                    'description': row['Description']
                }

                await self.save_if_not_exists(doc)


class DumpStaticsHotelspro(BaseStatics):

    collection = 'statics.hotels.hotelspro'

    async def hotels(self):
        with open('/home/songww/下载/Hotelspro单体酒店列表.csv') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                state = row['Parent Dest']
                doc = {
                    'code': row['Hotel Code'],
                    'giata_code': row['Giata ID'],
                    'name': row['Hotel Name'],
                    'city': {
                        'code': row['Dest Code'],
                        'name': row['Destination'],
                    },
                    'state': {'name': state != 'Null' and state or None},
                    'country': {'name': row['Country']},
                    'star': row['Stars'],
                    'address': row['Hotel Address'],
                    'score': row['Score Availabilty']
                }
                await self.save_if_not_exists(doc)


class DumpStaticsHotelsProV2(DumpStaticsHotelspro):

    endpoint = URL('http://cosmos.metglobal.tech/api/static/v1/')

    async def fetch(self, types='destinations'):
        auth = BasicAuth('WeegoTravel', 'MwCLCFoNGIxHiYDp')
        async with ClientSession(auth=auth) as session:
            params = {'limit': 100}
            _next = 'next'
            endpoint = self.endpoint / (types + '/')
            while True:
                if not _next:
                    break
                async with session.get(endpoint, params=params) as resp:
                    assert resp.status == 200, await resp.text()
                    try:
                        _resp = json.loads(await resp.text())
                        print(_resp)
                    except Exception:
                        print(await resp.text())
                params['next'] = _next = _resp.get('next')
                for item in _resp[types]:
                    yield item

    def country(self, country):
        return self.db.statics.countries.hotelspro.find_one({'code': country})

    def destination(self, destination):
        return self.db.statics.destination \
            .hotelspro.find_one({'code': destination})

    async def countries(self):
        async for countries in self.fetch('countries'):
            for country in countries:
                self.pprint(
                    await self.db.statics.countries
                    .update(
                        {'code': country['code']},
                        {'$set': countries},
                        upsert=True
                    )
                )

    async def destinations(self):
        async for destinations in self.fetch('destinations'):
            await self.db.statics.countries.insert_many(destinations)

    async def hotels(self):

        async def parse(hotel, con_limition):
            doc = dict(hotel)
            if hotel['stars']:
                doc['wgstar'] = int(hotel['stars'])
            doc['location'] = {
                'type': 'Point',
                'coordinates': [hotel['longitude'], hotel['latitude']]
            }
            city = await self.db.statics.destinations.hotelspro.find_one({
                'code': hotel['destination']
            })
            doc['city'] = {
                'code': hotel['destination'],
                'name': city['name'],
            }
            country = await self.db.statics.countries.hotelspro.find_one({
                'code': hotel['country']
            })
            doc['country'] = {
                'code': hotel['country'],
                'name': country['name'],
            }
            if hotel['images']:
                doc['images'] = [img['original'] for img in hotel['images']]

            doc['updated_at'] = datetime.strptime(
                hotel['updated_at'],
                '%Y-%m-%dT%H:%M:%S.%fZ'
            )
            r = await self.save_if_not_exists(doc)
            con_limition.release()
            return r

        # async for dest in self.fetch('destinations'):
        #     self._destinations[dest['code']] = dest

        # async for country in self.fetch('countries'):
        #     self._countries[country['code']] = country

        # print(self._destinations)
        # print(self._countries)

        limition = asyncio.Semaphore(200)

        # collection = self.db.get_collection('statics.hotels.hotelspro')
        # self.pprint(await collection.drop())
        async for hotels in self.fetch('hotels'):
            for hotel in hotels:
                await limition.acquire()
                asyncio.ensure_future(parse(hotel, limition))
                await asyncio.sleep(0)
        print('Wait for complete.')
        await asyncio.sleep(10)


class DumpStaticsHotelsProV3(DumpStaticsHotelsProV2):

    async def countries(self):
        exported = pathlib.Path('/home/songww/hp_exported')
        self.pprint(
            await self.db.statics.countries.hotelspro.drop()
        )
        for f in exported.glob('countries-*.json'):
            jsn = json.load(f.open())
            self.pprint(
                await self.db.statics.countries.hotelspro.insert_many(jsn)
            )

    async def destinations(self):
        collection = self.db.get_collection('statics.destinations.hotelspro')
        self.pprint(await collection.drop())
        for destinations in await self.fetch('destinations'):
            self.pprint(await collection.insert_many(destinations))

    async def fetch(self, types=''):
        exported = pathlib.Path('/home/songww/hp_exported')
        for f in exported.glob(f'{types}-*.json'):
            jsn = json.load(f.open())
            yield jsn

    async def save_if_not_exists(self, document):
        doc = ensure_can_be_serialized(document)
        update_result = await self.table.update_one(
            {'code': doc['code']},
            {'$set': doc},
            upsert=True
        )
        return self.pprint(update_result)


if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()

    dbc = AioMotorClient('mongodb://scripture_write:AYDBVmJqXEue353z@'
                         'dds-2ze2ae2045feb3e41.mongodb.rds.aliyuncs.com:3717,'
                         'dds-2ze2ae2045feb3e42.mongodb.rds.aliyuncs.com:3717/'
                         'scripture?replicaSet=mgset-4931065')

    scripture = dbc.get_database()

    loop.run_until_complete(
        DumpStaticsHotelsProV3(db=scripture).hotels()
    )
