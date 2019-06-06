# coding: utf8

import pandas
import logging

from yarl import URL
from pymongo import MongoClient
from scripture import settings

hub = MongoClient(settings.HUB_MONGO).hub
scripture = MongoClient(settings.MONGO).scripture

logger = logging.getLogger(__name__)


def get_capture_id(hotel_id):
    f = hub.poi_items.find_one({'hotel_id': hotel_id}, {'capture_id': 1})
    return f.get('capture_id')


def get_capture_history(hotel_id=None, hotels_id=None):
    by_hcom = scripture.capture_urls.find({
        # '$or': [{'hotel_id': hotel_id}, {'hotels_cn_id': hotels_id}]
        'hotels_cn_id': hotels_id
    })
    by_rxml = scripture.capture_urls.find({
        'hotel_id': hotel_id
    })
    if by_rxml.count() == 1:
        if by_hcom.count() == 0:
            scripture.capture_urls.update_one(
                {'hotel_id': hotel_id},
                {'$set': {'hotels_cn_id': hotels_id}}
            )
            return True
        else:
            logger.error(
                '%s %s hcom.count: %d',
                hotel_id,
                hotels_id,
                by_hcom.count()
            )
            return False
    else:
        logger.error(
            '%s %s rxml.count: %d, hcom.count %d',
            hotel_id,
            hotels_id,
            by_rxml.count(),
            by_hcom.count()
        )
        return False


def start(checklist):
    with open(checklist) as cl:
        for line in cl.readlines():
            hotel_id, *_, hotels_id = line.strip().split(',')
            if hotels_id.strip().isnumeric():
                yield (
                    hotel_id,
                    hotels_id,
                    get_capture_history(hotel_id, hotels_id)
                )
            else:
                logger.error(line)


def bad_capture_id():
    c = hub.poi_items.find({
        '__t': 'Hotel',
        'published': True,
        'capture_id': {'$exists': False}
    })
    empty = multi_m = multi_p = 0
    for poi in c:
        _p = hub.poi_items.find({'hotel_id': poi['hotel_id']})
        cnt = _p.count()
        if cnt == 1:
            ma = scripture.capture_url.find({'hotel_id': poi['hotel_id']})
            if ma.count() == 0:
                print(poi['hotel_id'], poi.get('capture_url'))
                empty += 1
                # pass
            else:
                print('Multi matched', poi['hotel_id'], *ma)
                multi_m += 1
        else:
            multi_p += 1
            for p in _p:
                print('Multi poi', poi['hotel_id'], p.get('capture_url'))
    print('Multi matched', multi_m)
    print('Multi poi', multi_p)
    print('Empty', empty)


def not_uploaded(csvfile):
    with open(csvfile) as csv:
        df = pandas.DataFrame.from_csv(csv)
    for city, item in df.iterrows():
        hcom_id = URL(item['hotels_url']).query.get('hotel-id')
        cap = scripture.capture_urls.find({'hotels_cn_id': hcom_id})
        if cap.count() == 0:
            logger.error('Empty %s', hcom_id)
        elif cap.count() > 1:
            logger.error('Multi match %s', hcom_id)
        else:
            poi = hub.poi_items.find({'capture_id': str(cap[0]['_id'])})
            if poi.count() == 0:
                logger.error('Miss upload %s, %s', hcom_id, str(cap[0]['_id']))
            elif poi.count() > 1:
                logger.error(
                    'Duplicated capture_id %s, %s',
                    hcom_id,
                    str(cap[0]['_id'])
                )
            else:
                pass
