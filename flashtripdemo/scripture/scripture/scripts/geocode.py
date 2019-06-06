#!python
# coding: utf8

import asyncio
import logging
import coloredlogs
from aiohttp import ClientSession

from aiogmaps import Client
from aiogmaps.exceptions import HTTPError
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient

from aiosocks.connector import ProxyConnector, ProxyClientRequest

from aioutils import Pool
from scripture import settings

coloredlogs.install(level='DEBUG')
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

proxy_adapter = {
    'connector': ProxyConnector(remote_resolve=True),
    'request_class': ProxyClientRequest
}

proxies = {
    'http': 'socks5://127.0.0.1:1080',
    'https': 'socks5://127.0.0.1:1080'
}

loop = asyncio.get_event_loop()

m = MongoClient(settings.MONGO)

pool = Pool(50, loop)


def get_address(addr, name):
    _addr = ''
    if addr['address1']:
        _addr += addr['address1']
    else:
        _addr += name
    if addr['address2'] and addr['address2'] != addr['city']:
        _addr += ', ' + addr['address2']
    if addr['address3'] and addr['address3'] != addr['city']:
        _addr += ', ' + addr['address3']
    if addr['state']:
        _addr += ', ' + addr['state']
    if addr['city']:
        _addr += ', ' + addr['city']
    if addr['country']:
        _addr += ', ' + addr['country']

    return _addr


async def run(gmap, loop):
    bad_records = m.roomsxml.geo.find({'partial_match': {'$exists': True}})
    async for rec in bad_records:
        pool.spawn(handle(rec, gmap))
    # pool.join()


async def geocode(addr):
    try:
        geos = await gmap.geocode(addr)
        if not geos:
            return None
        return geos[0]
    except HTTPError as e:
        log.exception(e)
        return None


async def handle(record, gmap):
    hotel = await m.roomsxml.hotels.find_one({'_id': record['hotel_id']})
    geo = await m.roomsxml.geocode.find_one(
        {'roomsxml_id': record['hotel_id']})
    geo.pop('_id')
    if ('geometry' not in geo) and hotel['address']['address1']:
        geo = await geocode(hotel['address']['address1'])
    if (not geo) or ('partial_match' in geo):
        log.debug('partial match')
        addr = get_address(hotel['address'], hotel['name'])
        geo = await geocode(addr)
    if not geo:
        log.error('Geocode is empty!')
        return
    if 'partial_match' in geo:
        log.error('partial match again: %s', hotel['hotel_id'])
    geo['roomsxml_id'] = hotel['_id']
    geo['hotel_id'] = hotel['_id']
    geo['loc'] = [geo['geometry']['location']['lng'],
                  geo['geometry']['location']['lat']]
    up = await m.roomsxml.geo.replace_one(
        {'hotel_id': hotel['_id']},
        geo
    )
    log.info("%s's state: %s", hotel['name'], up.modified_count)
    return up


with ClientSession(**proxy_adapter) as request:
    gmap = Client(
        key=settings.GOOGLE_GEO_KEY,
        request=request,
        requests_kwargs={'proxy': 'socks5://127.0.0.1:1080'}
    )
    try:
        loop.run_until_complete(run(gmap, loop))
        pool.join()
    except KeyboardInterrupt:
        loop.stop()
