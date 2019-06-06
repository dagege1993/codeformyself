# coding: utf8
"""一些酒店是从jetsetter抓取的，缺失很多重要的信息.

该脚本把从hotels.cn抓取的缺失信息填入MongoDB.
"""

import csv
import atexit
import asyncio
import logging

from asyncio import Queue
from itertools import chain
from functools import partial

import fire
import ujson
import uvloop
import logzero
from yarl import URL
from bson import ObjectId
from aiohttp import ClientSession
from motor.motor_asyncio import AsyncIOMotorClient as AioMongoClient

from scripture import settings
from scripture.models.hotel import Hotel

loop = uvloop.new_event_loop()
asyncio.set_event_loop(loop)

hub = AioMongoClient(settings.HUB_MONGO).get_database()
scripture = AioMongoClient(settings.MONGO).get_database()

queue = Queue(10)

logfmt = logzero.LogFormatter(
    fmt='%(color)s[%(levelname)s %(asctime)s %(name)s]%(end_color)s %(message)s',  # noqa
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logzero.setup_logger(
    name='upload',
    logfile='fill.log',
    formatter=logfmt,
    fileLoglevel=logging.DEBUG
)

# logger.setLevel(level=logging.INFO)


def parse_hcom_id(url):
    """Parse id of hcom from url of hcom."""
    return url.split('?')[0].split('ho')[-1].strip().strip('/')


async def publish(f):
    """Main."""
    count = 0
    with open(f) as csvfile:
        reader = csv.DictReader(
            csvfile,
            quotechar='"',
            delimiter=',',
            quoting=csv.QUOTE_ALL,
            skipinitialspace=True
        )
        for row in reader:
            count += 1
            if count <= 765:
                continue
            hcom_id = parse_hcom_id(row['hotel_URL'])
            if hcom_id.isnumeric() and row['cms ID']:
                await queue.put((row['cms ID'], hcom_id))
            else:
                logger.debug('%s Ignored(%s)', count, row)


async def recover(poi_id):
    """Mark poi as published if process is existed by exception."""
    return await hub.poi_items.update_one(
        {'_id': poi_id},
        {'$set': {'published': True}}
    )


async def consume():
    """Consume queue.

    from queue get cmsid and hcom_id
    parse
    push to cms
    """
    count = 0
    while not queue.empty():
        count += 1
        cms, hcom = await queue.get()
        poi = await hub.poi_items.find_one({'_id': ObjectId(cms)})
        if not poi:
            logger.debug('%d Bad ObjectId("%s")', count, cms)
            continue
        # if poi['edit_status'] == 'editing' and \
        #     poi['publish_status'] == 'offline':
        if poi['published'] is True:
            # logger.debug('%d Skipped ObjectId("%s")', count, cms)
            await hub.poi_items.update_one(
                {'_id': poi['_id']},
                {'$set': {'published': False}}
            )

        def func():
            result = loop.run_until_complete(recover(poi['_id']))
            logger.debug('Recovered: %s, %s', poi['_id'], result.raw_result)

        # atexit.register(func)
        # hcom = await scripture.hotels.find_one({'hotels_id': hcom})
        capture_id = poi['capture_id']
        if not capture_id:
            capture_id = str(ObjectId())
            await hub.poi_items.update_one(
                {'_id': ObjectId(cms)},
                {'$set': {'capture_id': capture_id}}
            )
        hotel_initial = partial(Hotel,
                                hotels_cn_id=hcom,
                                capture_id=capture_id)
        hotel = await loop.run_in_executor(None, hotel_initial)
        item = hotel.to_dict()
        payload = {'capture_id': capture_id}

        if not poi['latitude']:
            payload['latitude'] = item.pop('latitude', None)

        if not poi['longitude']:
            payload['longitude'] = item.pop('longitude', None)

        if not poi['website']:
            payload['website'] = item.pop('website', None)

        if not poi['telephone']:
            payload['telephone'] = item.pop('telephone', None)

        if poi['address']:
            payload['address'] = item.pop('address', None)

        gallery = poi.get('gallery', [])

        seen = set()

        payload['gallery'] = [
            image
            for image in chain(gallery, item.get('gallery', []))
            if seen.add(URL(image['image_url']).path)
        ]

        # rooms = poi[]
        # Patch rooms -- upload rooms directly?.

        p = None
        policies = poi.get('policy', [])
        payload['policy'] = list()
        for policy in policies:
            if policy['type'] == '入住政策':
                p = policy
                break
        for plc in item['policy']:
            if plc['type'] == '入住政策':
                if p is not None:
                    plc['content'] = p['content']
            payload['policy'].append(plc)

        payload['attractions'] = item['attractions']
        payload['facilities'] = item['facilities']

        # capture_id = item['capture_id']
        params = {'capture_id': capture_id}
        headers = {'accept-version': '5.0.0'}

        up = '/'.join([hotel.host, 'hotels'])
        async with ClientSession() as session:
            async with session.post(up, json=payload, headers=headers) as resp:
                text = await resp.text()
                assert resp.status == 200, {
                    'json': payload,
                    'resp': '\n'.join([str(resp.status), text])
                }
                json = ujson.loads(text)
                assert json['status'] == 200, {'json': payload, 'resp': text}
                logger.debug(
                    '%d Post Hotel(%s): CaptureId("%s"), json("%s")',
                    count,
                    cms,
                    capture_id,
                    payload,
                )
                logger.debug(
                    'HttpStatus(%d), ResponseStatus(%d), ResponseBody(%s)',
                    resp.status,
                    json['status'],
                    text
                )

        logger.info(
            f"%d Successful to update hotel by CaptureId('{capture_id}')",
            count
        )

        # await asyncio.sleep(60)

        ro = '/'.join([hotel.host, 'hotels', 'hotelrooms', capture_id])
        async with ClientSession(headers=headers) as session:
            async with session.post(ro, json=item, params=params) as resp:
                text = await resp.text()
                assert resp.status == 200, {
                    'json': item,
                    'resp': '\n'.join([str(resp.status), text])
                }
                json = ujson.loads(text)
                assert json['status'] == 200, {'json': item, 'resp': text}
                logger.debug(
                    '%d Post rooms: CaptureId("%s"), json("%s")',
                    count,
                    capture_id,
                    item,
                )
                logger.debug(
                    'HttpStatus(%d), ResponseStatus(%d), ResponseBody(%s)',
                    resp.status,
                    json['status'],
                    text
                )

        logger.info(
            f"%d Successful to update hotel rooms by CaptureId('{capture_id}')",  # noqa
            count
        )
        logger.info(f'%d CMS ObjectId("{cms}")', count)
        await asyncio.sleep(60)
        # await recover(poi['_id'])
        # atexit.unregister(func)


def main(f):
    """Run with asyncio.

    Create future for publisher and make consume run in loop.
    """
    asyncio.ensure_future(publish(f))
    loop.run_until_complete(consume())


if __name__ == '__main__':
    fire.Fire(main)
