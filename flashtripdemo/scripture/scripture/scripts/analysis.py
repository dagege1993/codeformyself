#!python
# coding: utf8

import re
import pandas as pd

from pymongo import MongoClient

mongo = MongoClient('mongodb://127.0.0.1:27017')

analysis = {'outsite': {}, 'insite': {}}


class Stop:
    def stop(self):
        pass


def loader():
    for doc in mongo.travelzoo.spider.find():

        dct = doc['deal_category_type']
        cc = doc['edition_country_code']
        price = doc['price']
        if not price:
            continue
        price_re = re.compile('([0-9\.]+)')
        res = price_re.search(price)
        if res:
            price = float(res.group(1))
        else:
            continue
        if price < 50:
            deg = '<50'
        elif 50 <= price and price < 100:
            deg = '50~100'
        elif 100 <= price and price < 150:
            deg = '100~150'
        elif 150 <= price:
            deg = '>150'

        if doc.get('has_external_link') or doc.get('external_link', '') != '':
            if cc not in analysis['outsite']:
                analysis['outsite'][cc] = {}
            if dct not in analysis['outsite'][cc]:
                # analysis['outsite'][cc][dct] = 0
                analysis['outsite'][cc][dct] = {}
            if deg not in analysis['outsite'][cc][dct]:
                analysis['outsite'][cc][dct][deg] = 0
            analysis['outsite'][cc][dct][deg] += 1
            # analysis['outsite'][cc][dct] += 1
        else:
            if cc not in analysis['insite']:
                analysis['insite'][cc] = {}
            if dct not in analysis['insite'][cc]:
            #     analysis['insite'][cc][dct] = 0
                analysis['insite'][cc][dct] = {}
            if deg not in analysis['insite'][cc][dct]:
                analysis['insite'][cc][dct][deg] = 0
            analysis['insite'][cc][dct][deg] += 1
            # analysis['insite'][cc][dct] += 1

    return


def dumps():
    pd.Panel(analysis['outsite']).to_excel('/home/songww/outsite_price.xlsx')
    pd.Panel(analysis['insite']).to_excel('/home/songww/insite_price.xlsx')


if __name__ == '__main__':
    loader()
    dumps()
