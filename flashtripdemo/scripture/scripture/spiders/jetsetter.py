# -*- coding: utf-8 -*-

import logging

import scrapy

from scripture.xpath import jetsetter

log = logging.getLogger(__name__)


class JetsetterSpider(scrapy.spiders.SitemapSpider):
    name = "jetsetter"
    sitemap_urls = ['https://www.jetsetter.com/robots.txt']
    allowed_domains = ["www.jetsetter.com", "cdnx.jetcdn.com"]

    enable_proxy = True

    sitemap_rules = [
        ('www.jetsetter.com/hotels/', '_parse_hotel_detail'),
        # ('www.jetsetter.com/search/q', '_parse_search_list')
    ]

    custom_settings = {
        'CONCURRENT_REQUESTS': 4
    }

    def _parse_hotel_detail(self, response):
        whatoknow = response.xpath(jetsetter.whatoknow).extract()
        whatwelove = response.xpath(jetsetter.whatwelove).extract()
        amenities = response.xpath(jetsetter.amenities).extract()
        overview = response.xpath(jetsetter.overview).extract()
        howtogethere_t = response.xpath(jetsetter.howtogethere)
        if not howtogethere_t.extract_first():
            howtogethere_t = response.xpath(jetsetter.howtogethere1)
        howtogethere = howtogethere_t.xpath('div/text() | text()').extract()
        travel_tips = response.xpath(jetsetter.travel_tips).extract_first()

        latitude = response.xpath(jetsetter.latitude).extract_first()
        longitude = response.xpath(jetsetter.longitude).extract_first()

        name = response.xpath('//head/title/text()').extract_first()

        images = []
        for image in response.xpath(jetsetter.images):
            img_src = image.xpath('./@src').extract_first().strip()
            images.append({
                'desc': image.xpath('./@alt').extract_first().strip(),
                'origin_url': img_src,
            })
            yield scrapy.Request(img_src)

        origin_body = response.xpath(jetsetter.body).extract_first()

        yield {
            'name': name.split('|')[0].strip(),
            'url': response.url,
            'what_to_know': whatoknow,
            'what_we_love': whatwelove,
            'amenities': list(filter(lambda x: x != '\xa0', amenities)),
            'overview': overview,
            'how_to_get_there': howtogethere or [],
            'travel_tips': travel_tips,
            'latitude': latitude,
            'longitude': longitude,
            'origin_body': origin_body,
            'images': images,
        }

    def _parse_search_list(self, response):
        log.debug(response.url)

    def start_requests(self):
        with open('/home/songww/workspace/git.feifanweige.com/scripture/jset_low_gallery.txt') as f:  # noqa
            for line in f.readlines():
                url = line.split()[0]
                yield scrapy.Request(url, self._parse_hotel_detail)
