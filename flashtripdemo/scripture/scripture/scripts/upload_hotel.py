#! python
# coding: utf8

import re
import logging

# import fire

from yarl import URL
from pymongo import MongoClient
from pymongo.errors import CursorNotFound
from datetime import datetime, timedelta

from scripture import settings
from scripture.exceptions import HotelNotFound
from scripture.models.hub_hotel import HubHotel

logging.basicConfig(
    format='%(asctime)s %(name)s %(levelname)s %(message)s',
    level=logging.INFO
)

logger = logging.getLogger('upload.hotels')

local = MongoClient()
m = MongoClient(settings.MONGO)
mc = MongoClient('mongodb://root:PGJ0ssznC8S2BKBuY@dds-2zefca1b050149b42.mongodb.rds.aliyuncs.com:3717,dds-2zefca1b050149b41.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-3027583')  # noqa

must_dropped = [
    'd218c8f0f90df6fe8f13463674d98f26',
    '77338959a0b6cbe411ed8e7fb3124d11',
    '5fa7e2788569ed7c28b819c1dcaa60cc'
]

where = {
    'similarity': {'$gt': []},
    'similarity.0.1': {'$gte': 80}
}

cities = {
    'Amsterdam': '17607',
    'Barcelona': '18350',
    'Berlin': '16534',
    'Boston': '19402',
    'Chicago': '19455',
    'Hong Kong': '16772',
    'Kyoto': '17246',
    'London': '52612',
    'Los Angeles': '19704',
    'Macau': '17366',
    'Melbourne': '15340',
    'Munich': '16609',
    'Osaka': '17286',
    'Paris': '16471',
    'Rome': '17149',
    'San Francisco': '19919',
    'Seattle': '19943',
    'Seoul': '18326',
    'Singapore': '18196',
    'Sydney': '15375',
    'Tokyo': '17303',
    'Washington D.C.': '20071',
    'Zurich': '18671'
}


def byNameSimilarities2():
    for similarity in local.scripture.jset_name_similarities2.find(where):
        if similarity['jset_id'] in must_dropped:
            continue
        hotel_id = similarity['similarity'][0][0]
        in_hub = mc.hub.poi_items.find_one({'hotel_id': str(hotel_id)})
        if in_hub:
            continue

        yield {'hotel_id': hotel_id, 'jset_id': similarity['jset_id']}


def updateCoverImage():
    import hashlib
    # for hotel in mc.hub.poi_items.find({"cover_image_url": {"$eq": ""}, })
    query = {
        "$and": [
            {"cover_image_url": {"$eq": ""}},
            {"capture_url": {'$ne': "", '$exists': True}},
            {'gallery': {'$exists': 1, '$ne': []}}
        ]
    }
    for hotel in mc.hub.poi_items.find(query):
        url = hotel.get('capture_url')
        if not url:
            continue
        if 'www.jetsetter.com' not in url:
            continue
        print(url)
        jset_id = hashlib.md5(url.encode('utf8')).hexdigest()
        hotel_id = hotel.get('hotel_id')
        if hotel_id:
            yield {'hotel_id': hotel_id, 'jset_id': jset_id}
        else:
            yield {'jset_id': jset_id}


def fillGallery():
    import re
    import hashlib
    url_from_jset = re.compile(r'www.jetsetter.com')
    curs = mc.hub.poi_items.find({
        'capture_url': url_from_jset,
        'gallery': {'$lte': []}
    })
    yield curs.count()
    for c in curs:
        jset_id = hashlib.md5(c['capture_url'].encode('utf8')).hexdigest()
        yield {'jset_id': jset_id, 'hotel_id': c['hotel_id']}


def onlyInRoomsXML():
    online_ids = list(cities.values())
    where = {'region.city_id': {'$in': online_ids}}
    yield m.scripture.rxmls.find(where).count()
    for hotel in m.scripture.rxmls.find(where):
        in_hub = mc.hub.poi_items.find_one({
            'hotel_id': str(hotel['hotel_id'])
        })
        if in_hub:
            continue
        yield {'hotel_id': hotel['hotel_id']}


def similarity_by_hotels_and_diff_jsets():
    captured_url_re = re.compile(r'^/id/\d+')
    olds = mc.hub.poi_items.find({
        'hotel_id': {'$ne': None},
        'capture_url': captured_url_re,
        'updatedAt': {'$lt': datetime.now() - timedelta(days=1)}
    })

    logger.info('Must be updated: %s', olds.count())

    mapping = mappings()

    logger.info('Poll has: %s', len(mapping.keys()))
    # for hotel_id, hotelscn in mappings().items():
    missed = 0
    for old in olds:
        hotel_id = old['hotel_id']
        if hotel_id not in mapping:
            missed += 1
            continue
        hotelscn = mapping[hotel_id]
        hotels_id = URL(hotelscn).path.split('/')[1].strip('ho')
        # m.scripture.capture_urls.update(
        #     {'hotel_id': hotel_id},
        #     {
        #         '$set': {'hotels_cn_id': hotels_id, 'hotel_id': hotel_id},
        #         '$setOnInsert': {'created_at': datetime.now()},
        #         "$currentDate": {'updated_at': True}
        #     },
        #     upsert=True
        # )
        yield {'hotel_id': hotel_id, 'hotels_cn_id': hotels_id}
    logger.info('-----------------------------')
    logger.info('Missed %s', missed)
    logger.info('-----------------------------')


def mappings():
    with open('hotelscn_mapping.txt') as mapping:
        m = {
            line.split()[0]: line.split()[1]
            for line in mapping.readlines()
            if line and not line.startswith('http')
        }
    return m


def service_and_checkin_checkout():
    cursor = m.scripture.capture_urls.find(
        {
            'hotels_cn_id': {'$exists': 1, '$ne': None}
        },
        no_cursor_timeout=True
    )
    yield cursor.count()
    for matched in cursor:
        if not matched['hotel_id']:
            continue
        if not matched['hotels_cn_id']:
            continue

        yield {
            'hotel_id': matched['hotel_id'],
            'hotels_cn_id': matched['hotels_cn_id']
        }


def upload_by_list(listfile):
    import pandas
    df = pandas.DataFrame.from_csv(listfile)
    yield 1
    for city, row in df.iterrows():
        hotels_id = URL(row['hotels_url']).query.get('hotel-id')
        matched = m.scripture.capture_urls.find_one(
            {'hotels_cn_id': hotels_id}
        )
        if not matched or not matched.get('hotel_id'):
            yield {'hotels_cn_id': hotels_id, 'city': city}
        elif matched and matched.get('hotel_id'):
            yield {
                'hotel_id': matched['hotel_id'],
                'hotels_cn_id': hotels_id,
                'city': city
            }
        else:
            continue


def patch_published():
    mmc = MongoClient(settings.HUB_MONGO)
    rec = []
    query = {
        '__t': 'Hotel',
        'published': True,
        'updatedAt': {'$lt': datetime(2017, 7, 26, 11, 40)}
    }
    for onlined in mmc.hub.poi_items.find(query, no_cursor_timeout=True):
        matched = mc.scripture.capture_urls.find_one({
            'hotel_id': onlined['hotel_id']
        })
        if not matched:
            # logger.warning('Not matched hotel_id %s', onlined['hotel_id'])
            hub = HubHotel(hotel_id=onlined['hotel_id'])

            rec.append((onlined['hotel_id'], hub._doc['address']))
            continue
        hotels_cn_id = matched.get('hotels_cn_id')
        if not hotels_cn_id:
            # logger.debug('Not found on hotels.cn %s', onlined['hotel_id'])
            hub = HubHotel(hotel_id=onlined['hotel_id'])
            rec.append((onlined['hotel_id'], hub._doc['name'], hub._doc['address']))
            continue
        capture_url = onlined.get('capture_url')
        if not capture_url:
            pass
            # logger.warning(
            #     'Not capture_url %s, %s',
            #     matched['hotel_id'],
            #     hotels_cn_id
            # )
        yield {
            'hotel_id': matched['hotel_id'],
            'hotels_cn_id': hotels_cn_id,
            'capture_url': capture_url
        }
    with open('/tmp/txt', 'w') as txt:
        for r in rec:
            txt.write(', '.join(r))
            txt.write('\n')


def t():
    yield 10
    yield {'hotel_id': '86919', 'hotels_cn_id': '115634'}


def start(sequence, columns=[]):
    seq = sequence()
    if next(seq) == 0:
        return
    try:
        for item in seq:
            try:
                hotel = HubHotel(**item)
                logger.info(hotel.to_dict()['capture_url'])
                logger.info(hotel.to_dict()['name'])
                # resp = hotel.to_hub()
                # logger.info(item)
                # logger.info(resp.json())
                resp = hotel.to_hub_hotel(
                    columns=[
                        'policy', 'attractions', 'facilities'
                    ]
                )
                if resp.json()['status'] != 200:
                    logger.error(
                        'Failed to update add info, %s, %s, %s',
                        resp.json(),
                        item,
                        hotel.to_dict()['capture_id']
                    )
                else:
                    logger.info('Success %s', resp.json())
                resp = hotel.to_hub_hotelroom()
                if resp.json()['status'] != 200:
                    logger.error(
                        'Failed to update rooms, %s, %s, %s',
                        resp.json(),
                        item,
                        hotel.to_dict()['capture_id']
                    )
                else:
                    logger.info('Success to update rooms %s', resp.json())
            except HotelNotFound as exc:
                with open('hotel_not_found.txt', 'a') as f:
                    f.write(str(item['hotels_cn_id']) + '\n')
            except Exception as exc:
                logger.error(item)
                logger.exception(exc)
    except CursorNotFound:
        logger.warn('Script is restarting.')
        return start(sequence)


if __name__ == '__main__':
    try:
        # start(byNameSimilarities2)
        # start(updateCoverImage)
        # start(onlyInRoomsXML)
        # start(fillGallery)
        # start(similarity_by_hotels_and_diff_jsets)
        # start(service_and_checkin_checkout)
        # start(lambda: upload_by_list('/home/songww/新增酒店列表2.csv'))
        # start(lambda: upload_by_list('/home/songww/新酒店列表1.csv'))
        start(lambda: upload_by_list('/home/songww/酒店列表3.csv'))
        # start(patch_published)
        # start(t)
    except KeyboardInterrupt:
        pass
