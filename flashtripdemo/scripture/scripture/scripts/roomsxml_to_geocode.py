#!/usr/bin/env python
# coding: utf8

from __future__ import unicode_literals

from aiogmaps.exceptions import HTTPError
from aiogmaps import Client
from scripture import settings
# from pymongo import MongoClient
import motor.motor_asyncio
from aiosocks.connector import ProxyConnector, ProxyClientRequest

import asyncio
import aiohttp

proxies = {
    'http': 'socks5://127.0.0.1:1080',
    'https': 'socks5://127.0.0.1:1080'
}

conn = ProxyConnector(remote_resolve=True)

loop = asyncio.get_event_loop()

queue = asyncio.Queue(maxsize=20, loop=loop)


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


class STOP:
    def stop(self):
        pass


async def deal(m, gmap):
    asyncio.sleep(1)
    while True:
        hotel = await queue.get()
        if isinstance(hotel, STOP):
            print('Stopped!')
            break
        if await m.roomsxml.geo.find_one({'roomsxml_id': hotel['_id']}):
            print('Exist!')
            continue
        try:
            geos = await gmap.geocode(
                get_address(hotel['address'], hotel['name'])
            )
        except HTTPError as e:
            print(e)
            geos = None
        if not geos:
            geo = {}
        else:
            geo = geos[0]
        geo['roomsxml_id'] = hotel['_id']
        await m.roomsxml.geo.insert_one(geo)
        print('Added!')


async def run(m, gmap):

    c = m.roomsxml.hotels.find({}, {'address': 1, 'name': 1}).skip(80000)
    async for hotel in c:
        await queue.put(hotel)
    await queue.put(STOP())
    print('Stop signal is send!')


if __name__ == '__main__':
    with aiohttp.ClientSession(
        connector=conn, request_class=ProxyClientRequest, loop=loop
    ) as request:
        m = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO)
        gmap = Client(
            key=settings.GOOGLE_GEO_KEY,
            request=request,
            requests_kwargs={
                'proxy': 'socks5://127.0.0.1:1080'
            }
        )

        # loop.run_until_complete(run(m, gmap, queue))
        loop.create_task(run(m, gmap))
        loop.create_task(deal(m, gmap))
        loop.create_task(deal(m, gmap))
        loop.create_task(deal(m, gmap))
        loop.create_task(deal(m, gmap))
        loop.create_task(deal(m, gmap))
        loop.create_task(deal(m, gmap))
        loop.create_task(deal(m, gmap))
        loop.create_task(deal(m, gmap))
        loop.create_task(deal(m, gmap))
        loop.create_task(deal(m, gmap))
        loop.create_task(deal(m, gmap))
        loop.create_task(deal(m, gmap))
        loop.create_task(deal(m, gmap))
        loop.create_task(deal(m, gmap))
        loop.create_task(deal(m, gmap))
        loop.create_task(deal(m, gmap))
        loop.run_forever()
