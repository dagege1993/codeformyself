# coding: utf-8

import json
import os.path
import logging
from urllib.parse import urlencode

import scrapy
from pymongo import MongoClient

from scripture import settings
from scripture.xpath import travelzoo
from scripture.items import TravelzooItem

log = logging.getLogger(__name__)


class USTravelzooSpider(scrapy.Spider):
    _cities = None
    _mongo = MongoClient(settings.MONGO)

    name = "ustravelzoo"
    allowed_domains = ["www.travelzoo.com"]
    domain = 'https://www.travelzoo.com'

    __locations_autocomplete = (
        '/api/v1/location/getlocationsautocomplete/',
        {
            'query': '',
            'querytype': 'exapt',
            'tzlocale': 1,
            'locale': 'en-US',
            'SuppressDefaultLocations': False,
            'IncludeFuzzyLocations': True,
            'CategoryTagFilterId': 0
        }
    )

    CTFIDS = (
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
        20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37,
        39, 40, 41, 42, 43, 44, 46, 96, 97, 98
    )

    def start_requests(self):
        '''Override
        Default entrypoint
        '''
        for ctf_id in self.CTFIDS:
            yield scrapy.Request(
                '{}{}?{}'.format(
                    self.domain,
                    '/search/GetSearchResult/',
                    urlencode({'locationId': 0, 'ctfId': ctf_id})
                ),
                headers={
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
            )

        for request in self._make_request_by_cities():
            yield request

    def parse(self, response):
        '''Override
        parse dataSource
        '''
        result = json.loads(response.body_as_unicode())
        search_response = result.get('searchResponse')
        if not search_response:
            log.warn('Bad response: {}'.format(response.body_as_unicode()))
            return
        dls = search_response.get('dls')
        if not dls:
            log.warn('Result is empty!')
            return
        if 'err' in search_response:
            log.warn(search_response['err']['dtp'])
            return

        editions = result['editions']
        dtg = search_response['dtg']

        log.error('Count: {}'.format(len(dls)))

        for dl in dls:
            dl['editions'] = editions
            dl['dtg'] = dtg

            item = TravelzooItem(dl).to_dict()
            yield item

            if not item['has_external_link']:
                yield scrapy.Request(
                    item['url'],
                    self._parse_detail,
                    meta={'item': item}
                )

    def _parse_detail(self, response):
        item = response.meta['item']
        if response.url != item['url']:
            item['external_link'] = response.url
            yield item
            return

        main = response.xpath('//section[@role="main"]')
        item['origin_body'] = main.extract_first().strip()
        item['deal_title'] = main.xpath('.//h1[@id="deal-headline"]/text()') \
            .extract_first().strip()
        item['deal_company'] = main.xpath('//div[@id="deal-company"]/text()') \
            .extract_first().strip()

        where = main.xpath('.//div[@id="deal-where"]/text()').extract_first()
        if not where:
            where = ''
        item['deal_where'] = where.strip()

        # images
        imgs = main.xpath('.//a[@class="js-gallery-image"]//img/@data-src')
        for img in imgs.extract():
            yield scrapy.Request(
                img.split('?')[0],
                self._dispose_image,
                meta={'tzoo_id': item['tzoo_id']}
            )

        external_link = main.xpath(travelzoo.external_link).extract_first()
        if external_link:
            item['external_link'] = external_link.strip()

        item['prices'] = self._price(main)

        when_u_can_go = main.xpath(travelzoo.avalible).extract_first()
        if when_u_can_go:
            item['when_u_can_go'] = when_u_can_go.strip()

        item['company'] = self._contact(main)

        the_deal = main.xpath(travelzoo.the_deal).extract_first()
        if not the_deal:
            the_deal = main.xpath(travelzoo.the_deal2).extract_first()
        if not the_deal:
            the_deal = ''

        why_we_love_it = main.xpath(travelzoo.why_love).extract()

        item['highlights'] = {
            'the_deal': the_deal.strip(),
            'why_we_love_it': list(map(lambda i: i.strip(), why_we_love_it))
        }

        item['highlights_contain'] = main.xpath(travelzoo.highlight_container)\
            .extract()

        item['whats_included'] = main.xpath(travelzoo.included).extract()

        term = main.xpath(travelzoo.term).extract_first()
        if term:
            item['term'] = term.strip()
        item['policies'] = self._policies(main.xpath(travelzoo.policies))

        item['overview'] = '\n'.join(main.xpath(travelzoo.overview).extract())
        item['reviews'] = []

        item['rating'] = []
        rate_summary = response.xpath(travelzoo.rate_summary).extract()
        if rate_summary:
            item['rating'] = self._rates(main, rate_summary)

        item['currency'] = travelzoo.currency \
            .search(item['edition_disclaimer']).group(1)

        name = response.xpath('//head/title/text()').extract_first()
        item['name'] = name.split('|')[0].strip()

        yield item

        reviews = main.xpath(travelzoo.review)
        if not reviews.extract():
            return
        self._dispose_reviews(reviews, item['tzoo_id'])

        rev_req = response.xpath(travelzoo.review_req).extract_first().strip()
        u, l, _, k, _ = rev_req.splitlines()[0].split('(')[1].split(',')
        if len(reviews.extract()) >= int(l):
            return
        yield scrapy.Request(
            '{}{}?{}={}'.format(self.domain, u, k, len(reviews) + 1),
            self._parse_reviews,
            meta={
                'uri': u,
                'key': k,
                'length': int(l),
                k: len(reviews) + 1,
                'tzoo_id': item['tzoo_id'],
            }
        )

    def _policies(self, _policies):
        _p = {}
        for _policy in _policies:
            key = _policy.xpath('.//span[class="sub-header"]/text()') \
                .extract_first()
            if not key:
                continue
            val = _policy.xpath('.//span[class="description"]/text()') \
                .extract_first()
            _p[key] = val

        return _p

    def _rates(self, resp, rate_summary):
        a, count = rate_summary
        percent, like_or_not = a.strip().split()
        count = count.strip().strip('(').split()[0]
        rating = {
            'percent': percent,
            'like_or_not': like_or_not,
            'rev_count': count,
            'rates': {}
        }
        rates_xp = '//div[@id="deal-reviews"]/div[contains(@class,'
        rates_xp += '"review-intro")]/div[@class="ratings"]/div[@class='
        rates_xp += '"ratingCategory"]'
        rates = resp.xpath(rates_xp)
        t_xp = './span[contains(@class, "member-rating-meterbar")]/@title'
        c_xp = './text()'
        for rate in rates:
            _rate = rate.xpath(t_xp).extract_first().strip().split()
            r = _rate[0]
            total = _rate[-1]
            column = rate.xpath(c_xp).extract()[-1].strip()
            rating['rates'][column] = (r, total)

        return rating

    def _price(self, response):
        try:
            kicker = response.xpath(travelzoo.kicker).extract_first().strip()
        except:
            kicker = None
        try:
            p_price = response.xpath(travelzoo.p_price).extract_first().strip()
        except:
            p_price = None
        try:
            price = response.xpath(travelzoo.price).extract_first().strip()
        except:
            price = None

        return {
            'kicker': kicker,
            'promo_price': p_price,
            'original_price': price
        }

    def _contact(self, resp):
        addr_xp = './/div[@id="deal-address"]/div/'
        addr_xp += 'div[@class="merchant-address"]/a/div/text()'

        tel_xp = './/div[@id="deal-address"]/div/div[@class="nowrap"]/a/text()'
        telephone = resp.xpath(tel_xp).extract_first()
        if not telephone:
            telephone = ''
        return {
            'address': resp.xpath(addr_xp).extract(),
            'telephone': telephone.strip()
        }

    def _parse_reviews(self, response):
        revs = response.xpath('/div[contains(@class, "row js-review review")]')

        self._dispose_reviews(revs, response.meta['tzoo_id'])
        key = response.meta['key']
        index = response.meta[key] + 50
        length = response.meta['length']
        if index < length:
            uri = response.meta['uri']
            response.meta[key] = index
            yield scrapy.Request(
                '{}{}?{}={}'.format(self.domain, uri, key, index),
                self._parse_reviews,
                meta=response.meta
            )

    def _dispose_reviews(self, reviews, travelzoo_id):
        for rev in reviews:
            # rev.xpath()
            pass

        # self._mongo

    def _dispose_image(self, response):

        pass

    def _make_request_by_cities(self):
        '''Make request by city
        '''
        for city in self.cities:
            c = self._mongo.travelzoo.cities.find({'name': ''})
            if c.count() > 0:
                yield self._make_request_by_shotrip(c[0])
            else:
                yield self._get_locations_autocomplete(city)

    def _get_locations_autocomplete(self, q):
        '''Get compatiblity location of travelzoo
        '''
        uri, query = self.__locations_autocomplete
        query['query'] = q

        destination = '{domain}{uri}?{query}'.format(
            domain=self.domain,
            uri=uri,
            query=urlencode(query)
        )

        return scrapy.Request(
            destination,
            self.__shorttrips_by_city,
            headers={
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            meta={'query': q}
        )

    def __shorttrips_by_city(self, response):
        '''Get nearby deals of city
        '''
        result = json.loads(response.body_as_unicode())
        locs = result.get('loc')
        origin = response.meta['query']

        location = self._parse_location(locs, origin)

        if 'dn' not in location:
            log.warn('Bad structure of loc<{}>'.format(location))
            return

        location['name'] = origin
        self._mongo.travelzoo.cities.insert_one(location)
        yield self._make_request_by_shotrip(location)

    def _make_request_by_shotrip(self, location):
        return scrapy.Request(
            '{}{}?{}'.format(
                self.domain,
                '/search/GetSearchResult/',
                urlencode({'locationId': location['id'], 'ctfId': 0})
            ),
            headers={
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        )

    def _parse_location(self, locs, origin):
        location = None
        for loc in locs:
            city_state = loc['dn'].split(',')
            if len(city_state) == 1:
                city = city_state[0]
                state = None
            else:
                city, state = city_state
                state = state.strip()

            if origin.upper() != city.upper():
                continue

            state_abbr = self.cities[origin]['state_abbr']
            if state is None or state_abbr == state.upper():
                location = loc
                break

        if location is None:
            location = locs[0]
            log.warn(
                'The city of `{}` was not found, using `{}` instead.'.format(
                    origin, location['dn']
                )
            )

        return location

    @property
    def cities(self):
        '''Load all cities of U.S.A
        '''
        if self._cities is not None:
            return self._cities

        city_file = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'resources',
            'us_cities.json'
        )
        with open(city_file, 'r') as _city_file:
            self._cities = json.loads(_city_file.read())

        return self._cities
