#! python3.6
# -*- coding: utf-8 -*-

# import os
import random
import logging

from datetime import datetime, timedelta

import json
import js2py

from yarl import URL
from w3lib.html import remove_tags, replace_tags

from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.spiders import SitemapSpider

from scripture import settings
from scripture.models import Hotels
from scripture.xpath import hotels as hotels_xp
from scripture.utils.processors import dupefilter
from scripture.utils.html import take_first, take_all, service_to_dict

from pymongo import MongoClient

log = logging.getLogger(__name__)


class HcomSpider(SitemapSpider):
    name = 'hcom'
    sitemap_urls = ['https://www.hotels.cn/robots.txt']
    allowed_domains = ['www.hotels.cn', 'www.hotels.com']

    handle_httpstatus_list = [302]

    sitemap_rules = [
        ('www.hotels.cn/ho', '_hotel_parse'),
        ('www.hotels.com/ho', '_hotel_parse')
    ]

    site_prefix = {
        'cn': 'CN',
        'com': 'EN'
    }

    details_query: dict = {}

    mongo_client = MongoClient(settings.MONGO)
    db_zh = mongo_client.scripture.hcom.zh.rooms
    def make_requests(self):
        """Make reqeust by id of hcom
        """
        for hcom_id in ['120145']:
            yield Request(
                "https://www.hotels.cn/ho{}".format(hcom_id),
                self._hotel_parse,
            )

    def _hotel_parse(self, response):

        url = URL(response.url)
        if response.xpath('//h2[@class="narrow-results-header"]/text()'):
            self.logger.debug('Drop response(%s)', response.url)
            return
        if url.path == '/search.do' and response.status == 302:
            location = URL(response.headers.get('Location').decode())
            yield Request(
                str(url.with_path(location.path).with_query(location.query)),
                self._hotel_parse,
                meta=response.meta
            )
            return
        hotels_id = url.path.strip('/').split('/')[0][2:]
        hotels_id = url.query.get('hotel-id') or hotels_id

        loader = ItemLoader(item=Hotels(), response=response)

        en_url = response.xpath(hotels_xp.EN_US_URL).extract_first()

        PREFIX = self.site_prefix.get(url.host.split('.')[-1])

        if PREFIX == 'CN':
            en_url = url.with_host('www.hotels.com') \
                .with_query({'pos': 'HCOM_US', 'locale': 'en_US'})
            en_url = str(en_url)
            # yield Request(
            #     en_url,
            #     self._hotel_parse,
            #     meta={
            #         # 'proxy': '172.17.1.198:1118'
            #     }
            # )

            if response.meta.get('crawl_reviews', True):

                review_url = url.with_scheme(url.scheme) \
                    .with_host(url.host) \
                    .join(
                        URL(
                            '/'.join([
                                '',
                                'hotel',
                                hotels_id,
                                'reviews',
                                ''
                            ])
                        )
                    )
                yield Request(
                    str(review_url),
                    self._review_parse,
                    meta={
                        'hotels_id': hotels_id,
                        # 'proxy': '172.17.1.198:1118'
                    }
                )

            loader.add_value('url', response.url)
            loader.add_value('us_url', en_url)

            if response.meta.get('crawl_rooms', True):

                now = datetime.now()
                checkin = now + timedelta(days=1)
                checkout = now + timedelta(days=3)
                details_query = {
                    'q-check-in': checkin.strftime('%Y-%m-%d'),
                    'q-check-out': checkout.strftime('%Y-%m-%d'),
                    # 'hotel-id': hotels_id,
                    'q-room-0-adults': 2,
                    'q-room-0-children': 0,
                    'tab': 'description',
                }
                u = url.with_scheme('https') \
                    .with_query(details_query)

                yield Request(
                    str(u),
                    self._rooms_parse,
                    meta={
                        'hotels_id': hotels_id,
                        'locale': PREFIX.lower(),
                        'dont_redirect': True,
                    }
                )

                yield Request(
                    str(u.with_host('www.hotels.cn')),
                    self._rooms_parse,
                    meta={
                        'hotels_id': hotels_id,
                        'locale': 'en',
                        'dont_redirect': True,
                        # 'proxy': '172.17.1.198:1118'
                    }
                )

        supplier_obj_id = response.meta.get('statics.hotels.id')
        supplier_name = response.meta.get('statics.hotels.supplier')
        if supplier_obj_id:
            loader.add_value('statics_hotels_id', supplier_obj_id)
            loader.add_value('statics_hotels_supplier', supplier_name)

        loader.add_value('hotels_id', hotels_id)
        loader.add_xpath('title', hotels_xp.TITLE)
        loader.add_xpath('name', hotels_xp.NAME)
        position = take_first(response, hotels_xp.POSITION)
        # loader.add_xpath('latitude', hotels_xp.LATITUDE)
        # loader.add_xpath('longitude', hotels_xp.LONGITUDE)
        latitude, longitude = position.split(',')
        loader.add_value('latitude', latitude)
        loader.add_xpath('longitude', longitude)
        loader.add_xpath('star', hotels_xp.STAR, re='(\d+)')
        loader.add_value('address', self._address(response))
        loader.add_xpath('address_text', hotels_xp.ADDRESS)
        loader.add_xpath('price', hotels_xp.PRICE)
        loader.add_xpath('city', hotels_xp.ADDRESS_LOCALITY)
        loader.add_xpath('country', hotels_xp.ADDRESS_COUNTRY)
        loader.add_xpath('telephone', hotels_xp.TELEPHONE)
        # loader.add_xpath('rating', '')
        # loader.add_xpath('tripadvisor', '')
        loader.add_xpath('landmarks', hotels_xp.LANDMARKS)
        loader.add_xpath('traffic_tips', hotels_xp.TRAFFIC_TIPS)
        loader.add_value('notice', self._notice(response, PREFIX))
        IN_STORE_SERVICES = getattr(
            hotels_xp,
            PREFIX + '_IN_STORE_SERVICE_FACT'
        )
        loader.add_value(
            'in_store_service_facilities',
            service_to_dict(response.xpath(IN_STORE_SERVICES), hotels_xp)
        )
        ROOM_SERVICES = getattr(hotels_xp, PREFIX + '_ROOM_SERVICE_FACT')
        loader.add_value(
            'room_service_facilities',
            service_to_dict(response.xpath(ROOM_SERVICES), hotels_xp)
        )
        loader.add_xpath('around', hotels_xp.AROUND)
        pictures = self._pictures(response.xpath(hotels_xp.PICTURES))
        loader.add_value('pictures', pictures)
        loader.add_xpath('short_introduction', hotels_xp.SHORT_INTRODUCTION)
        loader.add_xpath('amenities', hotels_xp.AMENITIES)
        loader.add_xpath('for_families', hotels_xp.FOR_FAMILIES)

        loader.add_value('locale', PREFIX.lower())

        loader.add_value('summary', self._summary(response))

        yield loader.load_item()

    def _review_parse(self, response):
        item = {}
        rev = {"hotels": {}, "TripAdvisor": {}}
        hotels_id = response.meta['hotels_id']
        try:
            resp = json.loads(response.body_as_unicode())
        except Exception as e:
            self.logger.error(response)
            self.logger.exception(e)
            return None
        reviews = resp.get('data', {}) \
            .get('body', {}) \
            .get('reviewContent', {}) \
            .get('reviews')
        if not reviews:
            self.logger.warn('Empty reviews, hotels_id: %s', hotels_id)
            yield None
        if 'hermes' in reviews:
            hermes = reviews['hermes']
            for grp in hermes['groups']:
                key = grp.get('separatorText', '中文评论')
                rev['hotels'][key] = grp['items']

        if 'tripAdvisor' in reviews:
            ta = reviews['tripAdvisor']
            rev['TripAdvisor'] = ta.get('items', [])
            item['tripadvisor'] = ta['allReviewsUrl']
            item['rating'] = ta['rating']
            item['ta_name'] = ta['propertyName']

        item['reviews'] = rev
        item['hotels_id'] = hotels_id

        self.logger.debug('Reviews(%s) of Hotel(%s)', len(rev), hotels_id)
        yield item

    def _rooms_parse(self, response):
        locale = response.meta['locale']
        hotels_id = response.meta['hotels_id']
        query = URL(response.url).query
        if ('location'in response.headers
                or b'location'in response.headers
                or b'Location' in response.headers
                or 'Location' in response.headers):
            for req in self._make_request_for_rooms_info(
                hotels_id, response.url, query
            ):
                yield req
                return
        js_script = response.xpath(hotels_xp.HCOM_CLIENT_DATA).extract_first()
        hcom_data = js2py.eval_js(js_script + 'hcomClientData;').to_dict()
        rooms_in_script = hcom_data.get('pda.roomsAndRates.rooms') or \
            hcom_data.get('pda', {}).get('roomsAndRates', {}).get('rooms')
        rooms_in_html = response.xpath(hotels_xp.ROOMS_LIST)
        key = (locale == 'cn' and 'rooms') or 'en.rooms'
        data = {key: [], 'hotels_id': hotels_id}
        if rooms_in_script:
            data[key] = self._parse_rooms_by_js(rooms_in_script)

        elif len(rooms_in_html) >= 1:
            data[key] = self._parse_rooms_by_html(rooms_in_html)

        else:
            self.logger.debug("Not found rooms, %s", response.url)
            return

        # 假设中文页面的房型和英文页面的房型相同
        db_room_type_num = self.db_zh.find({'hcom_id': hotels_id}).count()

        if not data[key]:
            yield Request(
                'https://www.hotels.cn/ho{}'.format(hotels_id),
                self._hotel_parse
            )
            return
        # FIXME(LensHo): 去重
        if db_room_type_num < 3:
            for req in self._make_request_for_rooms_info(
                hotels_id, response.url, query
            ):
                yield req

        self.logger.debug(
            'Start %s to %s',
            query.get('q-check-in'),
            query.get('q-check-out')
        )
        self.logger.debug(
            'Found %d rooms from %s',
            len(data[key]),
            response.url
        )
        self.logger.debug('Rooms %s name: %s', key, data[key])

        yield data

    def _parse_rooms_by_js(self, rooms_in_script):
        rooms = []
        for room_item in rooms_in_script:
            additional_info = room_item.get('additionalInfo', {})
            # amenities = additional_info.get('details', {}) \
            #     .get('amenities', [])
            # size = [
            #     remove_tags(amenity['description'])
            #     for amenity in amenities
            #     if amenity['type'] == 'room-size'
            # ]
            size = ''
            if additional_info['description'].startswith('<strong>'):
                size = additional_info['description'].split('</strong>', 1)[0]
                size = size[8:]
            bed_type_and_occupancy = room_item.get('bedTypeAndOccupancy', {})  # noqa
            bed_types = bed_type_and_occupancy.get('bedTypes', [])
            bed_extra_types = bed_type_and_occupancy.get('extraBeds', [])
            images = [
                {'type': image.get('caption'), 'url': image.get('fullSizeUrl')}
                for image in room_item.get('images', [])
            ]
            description = list(
                filter(
                    lambda item: item != '' and item != '&nbsp;',
                    replace_tags(
                        remove_tags(
                            additional_info.get('description', ''),
                            keep=('br',)
                        ),
                        '\n'
                    ).split('\n')
                )
            )
            occupancy = room_item.get('maxOccupancy')
            room = {
                'name': remove_tags(room_item['name']),
                'size': len(size) > 0 and size[0] or None,
                'occupancy': ''.join([occupancy.get('messageTotal'), occupancy.get('messageChildren')]),   # noqa
                'bed_types': bed_types,
                'bed_metrics': bed_type_and_occupancy.get('bedTypesTooltipMessage'),   # noqa
                'bed_types_str': bed_type_and_occupancy.get('localisedName'),
                'bed_extra_types': bed_extra_types,
                'description': description,
                'amenities': list(map(remove_tags, additional_info.get('details', {}).get('amenities', []))),  # noqa
                'images': images,
                'room_type_code': room_item['ratePlans'][0]['payment']['book']['bookingParamsMixedRatePlan']['roomTypeCode']  # noqa
            }

            rooms.append(room)
        return rooms

    def _parse_rooms_by_html(self, rooms_in_html):
        rooms = []
        for room_item in rooms_in_html:
            room = {
                'name': remove_tags(room_item.xpath('.' + hotels_xp.ROOM_NAME).extract_first()),  # noqa
                'size': remove_tags(room_item.xpath('.' + hotels_xp.ROOM_SIZE).extract_first()),  # noqa
                'occupancy': remove_tags(room_item.xpath('.' + hotels_xp.ROOM_OCCUPANCY).extract_first()),  # noqa
                'bed_types': remove_tags(room_item.xpath('.' + hotels_xp.ROOM_BEDS).extract_first()),  # noqa
                'bed_metrics': remove_tags(room_item.xpath('.' + hotels_xp.ROOM_BEDS_SIZE).extract_first()),  # noqa
                'bed_extra_types': [
                    {
                        'type': extra.xpath('./text()').extract_first(),
                        'metric': extra.xpath('./span/text()').extract_first()  # noqa
                    }
                    for extra in room_item.xpath('.' + hotels_xp.ROOM_EXTRA_BEDS)  # noqa
                ],
                'images': [],
                'description': room_item.xpath('.' + hotels_xp.ROOM_DESCRIPTION).extract_first(),  # noqa
                'amenities': room_item.xpath('.' + hotels_xp.ROOM_AMENITIES).extract(),  # noqa
                'room_type_code': room_item.xpath('.' + hotels_xp.ROOM_TYPE_CODE).extract_first(),   # noqa
            }
            rooms.append(room)
        return rooms

    def _make_request_for_rooms_info(self, hotels_id, url, query):
        checkin = datetime.strptime(query.get('q-check-in'), '%Y-%m-%d')
        if (checkin - datetime.now()).days > 50:
            return []
        if (checkin - datetime.now()).days > 7:
            day = random.choice([2, 3, 4])
        else:
            day = 2
        details_query = {
            'q-room-0-adults': 2,
            'q-room-0-children': 0,
            'tab': 'description',
            # 'hotel-id': hotels_id,
            'q-check-in': (checkin + timedelta(days=1)).strftime('%Y-%m-%d'),
            'q-check-out': (checkin + timedelta(days=day)).strftime('%Y-%m-%d')
            # q-check-out=2018-03-16&tab=description&q-room-0-adults=2&q-check-in=2018-03-15&
        }
        return [
            Request(
                str(
                    URL(url)
                    .with_host('www.hotels.cn')
                    .with_query(details_query)
                ),
                self._rooms_parse,
                meta={
                    'hotels_id': hotels_id,
                    'locale': 'cn',
                    'dont_redirect': True
                }
            ),
            Request(
                str(
                    URL(url)
                    .with_host('www.hotels.com')
                    .with_query(details_query)
                ),
                self._rooms_parse,
                meta={
                    'hotels_id': hotels_id,
                    'locale': 'en',
                    'dont_redirect': True,
                    # 'proxy': '172.17.1.198:1118'
                }
            )
        ]

    def _pictures(self, selectors):
        _pics = []
        for select in selectors:
            url = take_first(select, './@data-desktop')
            if not url:
                url = take_first(select, './@data-src')
            sizes = take_first(select, './@data-sizes')
            sizes = sizes and list(sizes) or list('zwybndeglst')
            name = take_first(select, './p/span[@class="room-name"]/text()')
            tag = take_first(select, './p/span[@class="second-level"]/text()')
            if not name:
                name = take_first(select, './p/text()')

            u = URL(url)
            if u.host != 'exp.cdn-hotels.com':
                *_, uri = u.path.split('/', 6)
                url = str(
                    URL.build(
                        scheme='https',
                        host='exp.cdn-hotels.com',
                        path=uri
                    )
                )
            else:
                url = url.format(size=sizes[0])
            _pics.append({
                'url': url,
                'name': name,
                'classification': tag,
                'sizes': sizes
            })

        return _pics

    def _address(self, resp):
        return {
            'street': take_first(resp, hotels_xp.ADDRESS_STREET),
            'locality': take_first(resp, hotels_xp.ADDRESS_LOCALITY),
            'region': take_first(resp, hotels_xp.ADDRESS_REGION),
            'postal_code': take_first(resp, hotels_xp.ADDRESS_POSTAL_CODE),
            'country': take_first(resp, hotels_xp.ADDRESS_COUNTRY)
        }

    def _notice(self, resp, prefix):
        keys = {
            'CN': {
                'term': '政策',
                'alias': '其它名称',
                'mandatory': '强制消费',
                'optional': '其它费用'
            },
            'EN': {
                'term': 'term',
                'alias': 'alias',
                'mandatory': 'mandatory fees',
                'optional': 'optional fees'
            }
        }
        key = keys[prefix]
        term_xp = getattr(hotels_xp, prefix + '_TERM')
        alias_xp = getattr(hotels_xp, prefix + '_ALIAS')
        mandatory_xp = getattr(hotels_xp, prefix + '_MANDATORY_FEES')
        optional_xp = getattr(hotels_xp, prefix + '_OPTIONAL_FEES')
        mandatory = dupefilter(self._clean(take_all(resp, mandatory_xp)))
        optional = dupefilter(self._clean(take_all(resp, optional_xp)))
        return {
            key['term']: dupefilter(self._clean(take_all(resp, term_xp))),
            key['alias']: dupefilter(self._clean(take_all(resp, alias_xp))),
            key['mandatory']: mandatory,
            key['optional']: optional
        }

    def _clean(self, _list):
        if not _list:
            return None
        return list(map(lambda v: remove_tags(v), _list))

    def _summary(self, resp):
        xp = (hotels_xp)
        return {
            'key_facts': self._clean(take_all(resp, xp.SUMMARY_KEY_FACTS)),
            'travellings': self._clean(take_all(resp, xp.SUMMARY_TRAVELLING)),
            'transport': self._clean(take_all(resp, xp.SUMMARY_TRANSPORT))

        }
