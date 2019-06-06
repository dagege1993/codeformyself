# coding: utf8

import fire
import pandas
import logging
import itertools

from yarl import URL
# from bson import ObjectId
from collections import defaultdict

from pymongo import MongoClient

from scripture import settings

_db_cache = {}

_db_uri_maps = {
    'scripture': settings.MONGO,
    'hub': settings.HUB_MONGO
}

logging.basicConfig(
    format='[%(asctime)s]%(name)s - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)


def database(name):
    if name not in _db_cache:
        _db_cache[name] = MongoClient(_db_uri_maps[name])
    return _db_cache[name][name]


def load(filename):
    df = pandas.DataFrame.from_csv(filename)
    for city, row in df.iterrows():
        _id = URL(row['hotels_URL']).query.get('hotel-id')
        yield _id


def main():
    hub = database('hub')
    logger = logging.getLogger(__name__)
    scripture = database('scripture')
    iders = itertools.chain(
        load('/home/songww/新增酒店列表2.csv'),
        load('/home/songww/新酒店列表1.csv')
    )
    count = defaultdict(list)
    for _id in iders:
        match = scripture.capture_urls.find({'hotels_cn_id': _id})
        if match.count() < 1:
            hcom = scripture.hotels.find_one({'hotels_id': _id})
            name = hcom['name'].split('(')[0]
            name_en = hcom['en']['name']
            poi = hub.poi_items.find(
                {'$or': [{'name': name, 'name_en': name_en}]}
            )

            if poi.count() < 1:
                # logger.warn('Not uploaded %s, %s, %s', _id, name, name_en)
                count['not_upload_and_not_matched'].append(_id)
            # elif poi.count() > 1:
            #     logger.warn('Multi uploaded %s, %s', _id, name, name_en)
            #     count['multi_upload_but_not_matched'].append(_id)
            # else:
            #     count['upload_but_not_matched'].append(_id)
        elif match.count() > 1:
            c_ids = []
            for m in match:
                c_ids.append((m['hotel_id'], str(m['_id'])))
            logger.debug('Found multi capture_id, %s, %s', _id, c_ids)
            count['multi_matched'].append(_id)
            continue
        else:
            # # hotel_id = match[0]['hotel_id']
            # capture_id = match[0]['_id']
            # poi = hub.poi_items.find({'capture_id': str(capture_id)})
            # if poi.count() == 0:
            #     logger.error('Not uploaded, %s, %s', _id, capture_id)
            #     count['not_uploaded'].append(_id)
            # elif poi.count() > 1:
            #     logger.error('Duplicated %s', _id)
            #     count['dup_uploaded'].append(_id)
            # else:
            #     p = poi[0]
            #     at = p['updatedAt']
            #     by = (str(p['updatedBy']) == '592e7406bcc7c81e078f7d8c') and \
            #         'me' or \
            #         hub.sys_users.find_one({'_id': p['updatedBy']})['name']
            #     count['suc_uploaded'].append(_id)
            #     logger.debug('%s %s', at, by)
            pass
    for key, value in count.items():
        print(key, len(value), value)


if __name__ == '__main__':
    fire.Fire(main)
