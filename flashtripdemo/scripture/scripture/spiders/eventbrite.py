# -*- coding: utf-8 -*-
import datetime
import json
import logging
from scrapy import Request
from scrapy.spiders import SitemapSpider
from scripture.xpath import eventbrite
from yarl import URL


class EventbriteSpider(SitemapSpider):
    name = 'eventbrite'
    allowed_domains = ['eventbrite.com']
    sitemap_urls = ['https://www.eventbrite.com/sitemap_xml/directory00.xml.gz']
    sitemap_rules = [('www.eventbrite.com/d/', 'parse')]

    custom_settings = {
        'DOWNLOAD_DELAY': 2
    }

    logger = logging.getLogger(__name__)

    def parse(self, response):
        url = URL(response.url)
        page_num = url.query.get('page', 1)
        if page_num == 1:
            max_page = response.xpath('//span[contains(@class, "js-pagination-description")]/text()')\
                .extract_first()
            try:
                # +2  because range() [)
                max_page = int(max_page.strip().split('of ')[1].split(' ')[0]) // 15 + 2
                for i in range(2, max_page):
                    q = dict(url.query)
                    q['page'] = i
                    yield Request(str(url.with_query(q)))
            except AttributeError as e:
                self.logger.error(e)
        divs = response.xpath('//div[contains(@class, "js-event-list-container")]/div')
        source = response.xpath('//script[@type="application/ld+json"]/text()')\
            .extract_first().strip()
        result_list = []
        for div in divs:
            result = self.parse_info(div)
            result_list.append(result)
        source = json.loads(source)
        for i, j in zip(result_list, source):
            if i.get('url') == j.get('url'):
                j['end_date'] = j.pop('endDate')
                j['start_date'] = j.pop('startDate')
                offers = j.pop('offers')
                offers['low_price'] = offers.pop('lowPrice')
                offers['price_currency'] = offers.pop('priceCurrency')
                offers['high_price'] = offers.pop('highPrice')
                offers['type'] = offers.pop('@type')
                j.update({'offers': offers})
                organizer = j.pop('organizer')
                organizer['type'] = organizer.pop('@type')
                j.update({'organizer': organizer})
                location = j.pop('location')
                location['type'] = location.pop('@type')
                address = location.pop('address')
                address['type'] = address.pop('@type')
                address['address_locality'] = address.pop('addressLocality')
                address['address_country'] = address.pop('addressCountry')
                address['street_address'] = address.pop('streetAddress')
                address['address_region'] = address.pop('addressRegion')
                location.update({'address': address})
                geo = location.pop('geo')
                geo['type'] = geo.pop('@type')
                location.update({'geo': geo})
                j.update({'location': location})
                j.pop('@context')
                j['type'] = j.pop('@type')
                i.update(j)
        for i in result_list:
            yield i

    def parse_info(self, div):
        name = div.xpath(eventbrite.TITLE_SHARE).extract_first() \
               or div.xpath(eventbrite.TITLE).extract_first()
        name = name.strip() if name else ''
        url = div.xpath(eventbrite.LINK).extract_first() \
              or div.xpath(eventbrite.LINK_SHARE).extract_first()
        tags = div.xpath(eventbrite.TAGS).extract() \
               or div.xpath(eventbrite.TAGS_SPAN).extract()
        tags = [i[1:] for i in tags if i.startswith('#')]
        price = div.xpath(eventbrite.PRICE).extract_first()
        image = div.xpath(eventbrite.IMG_URL).extract_first()
        date = div.xpath(eventbrite.DATE).extract_first()
        if date:
            value = date.split(',')[1].split('&')[0].strip()
            value = datetime.datetime.strptime(value, '%b %d %I:%M %p')
            date = value.strftime(str((datetime.datetime.now()).year) + '-%m-%d %H:%M')
        location = div.xpath(eventbrite.VENUE).extract_first()
        location = location.strip() if location else ''
        return {'title': name,
                'url': url,
                'tags': tags,
                'price': price,
                'image': image,
                'date': date,
                'address': location}