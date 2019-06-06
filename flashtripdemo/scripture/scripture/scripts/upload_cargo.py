# coding: utf8

import re
import os

import requests

from urllib.parse import urlencode, parse_qsl, urlsplit, urlunsplit
from scripture import settings
from scripture.utils import strip_tags

from pymongo import MongoClient
from googletrans import Translator

os.environ['https_proxy'] = 'socks5://127.0.0.1:1080'
os.environ['http_proxy'] = 'socks5://127.0.0.1:1080'
os.environ['no_proxy'] = '47.94.77.75'

trans = Translator()


def url_cleaner(url):
    splited = urlsplit(url)
    q = dict(parse_qsl(splited.query))
    q.pop('searchGuid')
    splited = list(splited)
    splited[3] = urlencode(q)
    return urlunsplit(splited)


def payload(dl):
    # bt.trans = lambda x: [{'dst': x}]

    digit = re.compile('[0-9\.]+')
    currency = re.compile('[^A-Z]([A-Z]{3})[^A-Z]')

    addr = dl.get('company', {}).get('address', [])
    addr = ','.join(addr)
    if not addr:
        return None

    name_x = dl.get('title') \
        or dl['origin'].get('hdl') \
        or dl['origin'].get('fhd')
    name_en = name_x
    name = trans.translate(name_en, dest='zh-CN').text
    city = dl['where']
    price = dl.get('prices', {}).get('promo_price')
    if not price:
        price = dl['price']
    try:
        price = float(digit.findall(price)[0])
    except:
        print('Bad price: {}'.format(dl['price']))
        print('Title: {}'.format(name_x))
        print('Url is: {}'.format(dl['url']))
        price = 0
    price_type = currency.search(dl['edition_disclaimer']).group(1)
    cover_images = dl['src_image']
    _merchant = dl['source']
    # merchant = trans.translate(_merchant, dest='zh-CN').text
    _highlights = dl.get('highlights', {})
    highlights_zh = []
    highlights_en = []
    the_deal = strip_tags(_highlights.get('the_deal', ''))
    if the_deal:
        highlights_en.append({
            'title': 'The Deal',
            'description': the_deal
        })
        highlights_zh.append({
            'title': 'The Deal',
            'description': trans.translate(the_deal, dest='zh-CN').text
        })
    why_love = map(strip_tags, _highlights.get('why_we_love_it', []))
    for why in why_love:
        why_t = trans.translate(why, dest='zh-CN').text
        if not why_t:
            continue
        highlights_en.append({
            'title': 'Why We Love It',
            'description': why
        })
        highlights_zh.append({
            'title': 'Why We Love It',
            'description': why_t
        })
    _info = '\n'.join(map(strip_tags, dl.get('whats_included', [])))
    info = trans.translate(_info.replace('\n', '|'), dest='zh-CN') \
        .text.replace('|', '\n')
    _tips = strip_tags(dl.get('term', '').replace('\n', '|'))
    if _tips:
        tips = trans.translate(_tips, dest='zh-CN').text.replace('|', '\n')
    else:
        tips = ''
    phone = dl.get('company', {}).get('telephone')
    available_start = dl['start_time']
    available_end = dl['end_time']
    capture_url = url_cleaner(dl['url'])
    short_introduction = dl['summary_keywords']
    introduction = dl.get('overview')
    en = {
        'merchant': _merchant,
        'highlights': highlights_en,
        'info': _info,
        'tips': _tips,
        'address': addr,
    }

    d = {
        'name': name,
        'name_en': name_en,
        'city_ref': city,
        'info_ref': _info,
        'tips_ref': _tips,
        'tags_ref': '',
        'price': float(price),
        'price_type': price_type,
        'merchant': _merchant,
        'highlights': highlights_zh,
        'cover_images': [{'image_url': cover_images}],
        'info': info,
        'tips': tips,
        'address': addr,
        'available_start': available_start,
        'available_end': available_end,
        'capture_url': capture_url,
        'en': en,
        'introduction': strip_tags(introduction),
        'short_introduction': strip_tags(short_introduction)
    }
    if phone:
        d['phone'] = phone

    return d

if __name__ == '__main__':

    m = MongoClient(settings.MONGO)

    for tz in m.scripture.tzoos.find({
        # 'company.address': {'$exists': True},
        'has_external_link': False,
        'edition_country_code': 'us',
        'is_hotel': False
    }):
        try:
            pld = payload(tz)
        except:
            continue
        if not pld:
            continue

        r = requests.post(
            'http://47.94.77.75/api/v3/products',
            json=pld
        )
        try:
            print(r.json())
        except:
            print(r.text)
