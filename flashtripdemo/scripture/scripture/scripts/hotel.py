# coding: utf8

import re
import asyncio

from asyncio import Queue
# from urllib.parse import urlencode

import pandas

from yarl import URL
from logzero import logger
from pymongo import MongoClient

from scripture import settings
from scripture.models.hotel import Hotel
from scripture.models.cities import Cities

Q = Queue(10)


class Hotels(object):

    _HCOM_ID_RE = re.compile(r'/ho([0-9]+)')
    _CITY_EN_RE = re.compile(r'([a-zA-Z ]+)')

    def dumps(self, infile, outfile, cities=None):
        result = [hotel.to_dict() for hotel in self.__prepare(infile, cities)]
        df = pandas.DataFrame.from_dict(result)
        return df.to_excel(
            outfile,
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

    def uploads(self, infile, cities=None, with_hotel=True, with_rooms=True):
        steps = []
        loop = asyncio.get_event_loop()
        if with_hotel:
            steps.append('to_hub')
        if with_rooms:
            steps.append('to_hub_hotelroom')
        if not steps:
            logger.error('Nothing to do!')
        loop.run_until_complete(
            asyncio.gather(
                self.__step_do(hotel, steps)
                for hotel in self.__prepare(infile, cities)
            )
        )


    async def __step_do(self, model, steps):
        for step in steps:
            jsn = await getattr(model, step)()
            logger.debug(f'{step} -- {json.dumps(jsn, indent=2)}')

    def __prepare(self, infile, cities):
        scripture = MongoClient(settings.MONGO).scripture
        df = pandas.read_csv(infile, error_bad_lines=False)
        # keys = df.keys().tolist()
        cities = cities and Cities.from_json(cities) or Cities()
        cities.hub = MongoClient(settings.HUB_MONGO).hub
        for idx, row in df.iterrows():
            isnull = row.isnull()
            if isnull.get('ta'):
                continue
            bonotel = not isnull.get('bonotel', True) and \
                int(row.bonotel) or None
            roomsxml = not isnull.get('roomsxml', True) and \
                int(row.roomsxml) or None
            hotelspro = not isnull.get('hotelspro', True) and \
                str(row.hotelspro) or None
            hotelbeds = not isnull.get('hotelbeds', True) and \
                int(row.hotelbeds) or None
            jactravel = not isnull.get('jactravel', True) and \
                int(row.jactravel) or None
            ta = row.get('ta')
            hcom = row.get('hotel_URL')
            if pandas.isnull(hcom):
                continue
            try:
                hcom_id = self.__parse_hcom_id(hcom)
            except AttributeError:
                continue
            try:
                _city = row.get('city') or row.get('城市')
                city_name = self._CITY_EN_RE.match(_city).group(1)
                city = cities.name(city_name.strip())
                yield Hotel(
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
            except (KeyError, IndexError, TypeError) as e:
                logger.critical('hcom(%s), city(%s)', hcom_id, _city)
                logger.exception(e)

    @classmethod
    def __parse_hcom_id(cls, url):
        u = URL(url)
        return u.query.get('hotel-id') or \
            cls._HCOM_ID_RE.match(u.path).group(1)
