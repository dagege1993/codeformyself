# coding: utf8

from yarl import URL
from lxml import etree
from scripture.xpath import jetsetter


class JsetAdditional:
    def __init__(self, html):
        self.html = etree.HTML(html)

    def url(self):
        url = self.html.xpath(jetsetter.ta_url)
        if url:
            return url[0]

    def rating(self):
        rating = self.html.xpath(jetsetter.ta_rating)
        if rating:
            return rating[0]

    def images(self):
        def patch_url(url):
            return URL(url).with_host('img3.weegotr.com') \
                    .with_scheme('http')
        gallery = []
        imgs = self.html.xpath(jetsetter.images)
        for img in imgs:
            gallery.append({
                'image': None,
                'image_url': patch_url(img.xpath('.//@src')[0].split('?')[0])
            })
        return gallery

    def price(self):
        price = self.html.xpath(jetsetter.price)
        if price:
            return ''.join(price).strip().replace('\xa0', '').replace('$', '')

    def city(self):
        city = self.html.xpath(jetsetter.city_state)
        if city:
            return city[0]
