# coding: utf8

import re

import time
import logging

from concurrent.futures import ThreadPoolExecutor

import pandas
from yarl import URL
from pymongo import MongoClient
from scripture import settings
from scripture.models.hub_hotel import HubHotel

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

HCOM_ID_RE = re.compile(r'/ho([0-9]+)')

__all__ = ['hotels']


def not_nan_and_return(obj):
    return (obj, None)[pandas.isna(obj)]


def __seq_from_csvfile(csvfile):
    sequence = []

    scripture = MongoClient(settings.MONGO).scripture

    df = pandas.DataFrame.from_csv(csvfile)
    for country, item in df.iterrows():
        u = URL(item.get('hotels_url', ''))
        try:
            hcom_id = u.query.get('hotel-id', None) or \
                HCOM_ID_RE.match(u.path).group(1)
        except AttributeError:
            logger.error('Can not parsed url of hotels.cn, %s', item)
            continue
        # match = db_similars.find({'hotels_id': hcom_id}) \
        #     .sort('similarity.0.1', -1)
        comments_url = item.get('ta') or item.get('TA_url')
        item = {
            'city': item.get('城市'),
            'comments_url': comments_url,
            'hotels_cn_id': hcom_id,
            'db': scripture,
            'hotelspro': not_nan_and_return(item.get('hotelspro')),
            'hotelbeds': not_nan_and_return(item.get('hotelbeds')),
            'jactravel': not_nan_and_return(item.get('jactravel')),
            'bonotel': not_nan_and_return(item.get('bonotel'))
        }
        # if match.count() > 0:
        #     _s = match[0]['similarity']
        #     if _s:
        #         item['hotel_id'] = _s[0][0]
        sequence.append(item)
    return sequence


def hotels(sequence=None, csvfile=None, steps=None, similars=None,
           to_excel=False,
           to_hub=False):

    cnt = 0

    if steps is None:
        steps = ['create', 'rooms']

    if not sequence:
        if csvfile:
            sequence = __seq_from_csvfile(csvfile)
        else:
            raise ValueError('请提供 sequence 或 csvfile')

    hub_step_action = {
        'create': 'to_hub',
        'update': 'to_hub_hotel',
        'rooms': 'to_hub_hotelroom'
    }

    def hub_step_do(hub_model, step):
        return getattr(hub_model, hub_step_action[step])()

    data = []

    if to_excel:
        with ThreadPoolExecutor(max_workers=10) as excutor:
            futures = []
            for item in sequence[:2]:
                futures.append(
                    excutor.submit(
                        lambda item: HubHotel(**item).to_dict(), item
                    )
                )
            for f in futures:
                if f.exception():
                    print(f, dir(f))
                    continue
                data.append(f.result())
        return pandas.DataFrame.from_dict(data).to_excel('dumps.xlsx')

    for item in sequence[10:]:
        try:
            hub = HubHotel(**item)
            for step in steps:
                logger.debug('Start %s, %s', step, item)
                resp = hub_step_do(hub, step)
                if resp.status_code != 200 or resp.json()['status'] != 200:
                    logger.error(
                        'In step %s, status %s, response %s',
                        step,
                        resp.status_code,
                        resp.text
                    )
                    continue
                logger.info(
                    'In step %s, status %s, response %s',
                    step,
                    resp.status_code,
                    resp.text
                )
            cnt += 1
        except Exception as e:
            logger.exception(e)
    while 1:
        logger.info('waiting for exit.')
        time.sleep(1)
    logger.info('Success %d', cnt)
    print('Success', cnt)
