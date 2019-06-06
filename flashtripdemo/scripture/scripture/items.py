# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import json
import scrapy

import logging

log = logging.getLogger(__name__)


class TravelzooItem:
    MALE = 0
    FEMALE = 1
    UNKNOWN = -1

    def __init__(self, item):
        self.origin = item
        self._edition = {}

    @property
    def group(self):
        return self.origin.get('grp')

    @property
    def product_id(self):
        return self.origin.get('pid')

    @property
    def deal_category(self):
        return self.origin.get('dc')

    @property
    def deal_category_type(self):
        return self.origin.get('dct')

    @property
    def platform(self):
        return self.origin.get('plt')

    @property
    def is_expansion_result(self):
        return self.origin.get('exp')

    @property
    def tags(self):
        _tags = []
        tags = self.origin.get('tag')
        dtg = self.origin.pop('dtg')
        if not tags:
            return _tags
        for tag in tags:
            _tags.append(list(filter(lambda d: d['id'] == tag['id'], dtg)))
        return _tags

    @property
    def tzoo_id(self):
        return self.origin['id']

    @property
    def start_time(self):
        return self.origin['psd']

    @property
    def end_time(self):
        return self.origin['ped']

    @property
    def sort(self):
        return self.origin.pop('srt', {})

    @property
    def sort_by_price(self):
        return self.sort.get('spr')

    @property
    def sort_by_recommended(self):
        return self.sort.get('sre')

    @property
    def sort_by_rating(self):
        return self.sort.get('sra')

    @property
    def sort_by_image(self):
        return self.sort.get('sim')

    @property
    def sort_by_group(self):
        return self.sort.get('grp')

    @property
    def sort_by_index(self):
        return self.sort.get('six')

    @property
    def has_external_link(self):
        return self.origin.get('xdl')

    @property
    def edition_country_code(self):
        return self.edition.get('cc')

    @property
    def edition_heading(self):
        return self.edition.get('hdg')

    @property
    def edition_tip_text(self):
        return self.edition.get('tip')

    @property
    def edition_deal_expert(self):
        return self.edition.get('dex')

    @property
    def edition_deal_dxpert_gender(self):
        if self.edition_deal_expert.get('gen') == 'F':
            return self.FEMALE
        elif self.edition_deal_expert.get('gen') in ('M', ''):
            return self.MALE
        else:
            return self.UNKNOWN

    @property
    def edition_disclaimer(self):
        return self.edition.get('dsc')

    @property
    def edition(self):
        if not self._edition:
            for e in self.origin.pop('editions'):
                if e['tzl'] == self.origin['tzl']:
                    self._edition = e
                    break
        return self._edition

    @property
    def is_hotel(self):
        plt = self.origin.get('plt')
        if plt:
            return plt == 2 or plt == 3
        htr_type = self.origin.get('htr', {}).get('typ')
        return htr_type == 0 or htr_type == 1

    @property
    def is_hotel_injected_deal(self):
        return self.origin.get('htr', {}).get('typ') == 1

    @property
    def ima(self):
        return self.origin.get('ima', {})

    @property
    def title(self):
        return self.ima.get('cap') or \
            self.origin.get('hdl') or \
            self.origin.get('fhd')

    @property
    def show_star_rating(self):
        return len(self.origin.get('stl', [])) > 0 and \
            self.star_rating > 0

    @property
    def star_rating(self):
        return self.origin.get('str', 0)

    @property
    def star_rating_value_in_percentage(self):
        if self.star_rating > 0:
            return '{}%'.format(round(100 * self.star_rating / 5))
        return '0'

    @property
    def image(self):
        name = self.ima.get('nam')
        if name is not None:
            return 'https://ssl.tzoo-img.com/images/' + name
        else:
            return None

    @property
    def price(self):
        return self.origin.get('prc')

    @property
    def url(self):
        origin_url = self.origin['url']
        if origin_url.startswith('https://www.travelzoo.com'):
            return origin_url
        else:
            return 'https://www.travelzoo.com' + self.origin['url']

    @property
    def product_variant(self):
        return self.origin.get('hdl')

    @property
    def headline(self):
        return '{price} -- {hdl}'.format(
            price=self.price,
            hdl=self.product_variant
        )

    @property
    def source(self):
        return self.origin.get('src')

    @property
    def src_image(self):
        if self.ima.get('ir') is True:
            directory = 'remote/'
        else:
            directory = 'images/'

        name = self.ima.get('nam')
        if not name:
            log.warn('Name of image is empty: {}'.format(self.ima))
            return None
        return 'https://ssl.tzoo-img.com/' + directory + name

    @property
    def src_image_ver(self):
        if self.ima.get('v') is not None and self.ima.get('v') > 1:
            return self.ima['v']
        else:
            return None

    @property
    def credits(self):
        return self.ima.get('cre')

    @property
    def distance_formatted(self):
        return ':.1f'.format(float(self.distance)) if self.distance else None

    @property
    def distance(self):
        return self.origin.get('dis')

    @property
    def summary_keywords(self):
        return self.origin.get('kw')

    @property
    def when(self):
        return self.origin.get('whn')

    @property
    def where(self):
        return self.origin.get('whe')

    @property
    def badges(self):
        return self.origin.get('srb')

    @property
    def location(self):
        return {'lat': self.origin.get('lat'), 'lng': self.origin.get('lng')}

    def is_top_20(self, idx):
        if self.badges[idx].get('type') == 9 or self.origin['typ'] == 3:
            return True
        else:
            return False

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        item = {}
        for method in dir(self):
            if method.startswith('__'):
                continue

            if method in ('is_top_20', 'to_json', 'to_dict'):
                continue

            item[method] = getattr(self, method)

        return item


class TravelzooCity(scrapy.Item):
    pass
