# coding: utf8

import logging
import requests
from lxml import etree
from pymongo import MongoClient
from scripture.models.tripadvisor import TripAdvisor


class Contact(object):

    def __init__(self, mongo_connect_uri):
        mongodb = MongoClient(mongo_connect_uri)
        self._scripture = mongodb.get_database()
        self._process = lambda x, y: y
        self._logger = logging.getLogger(__name__)
        self._user_agent = ('Mozilla/5.0 (X11; Linux x86_64) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/59.0.3071.86 Safari/537.36')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('MONGO'))

    def open_spider(self, spider):
        """Disabled
        Where to save
        How to identity
        """
        # if spider.name = 'hcom':
        #     self._process = self._fetch_from_thirdparty

        pass

    def process_item(self, item, spider):
        return self._process(item)

    def _fetch_from_thirdparty(self, item):
        hotel = self._scripture.hotels.find_one(
            {
                'hotels_id': item['hotels_id']
            }
        )
        if 'contacts' in hotel:
            item['contacts'] = hotel['contacts']
            return item

        try:
            ta_contact = self._fetch_from_tripadvisor(self)
        except:
            ta_contact = {}
        if ta_contact and 'telephone' in ta_contact and 'website' in ta_contact:
            return ta_contact
        try:
            g_contact = self._fetch_from_google(item)
        except:
            g_contact = {}

        c = {}
        if ta_contact.get('telephone'):
            c['telephone'] = ta_contact.get('telephone')
        elif g_contact.get('telephone'):
            c['telephone'] = g_contact.get('telephone')
        if ta_contact.get('website'):
            c['website'] = ta_contact.get('website')
        elif g_contact.get('website'):
            c['website'] = g_contact.get('website')
        return c

    def _fetch_from_tripadvisor(self, url):

        ta = TripAdvisor(url)
        c = {}
        if ta.telephone:
            c['telephone'] = ta.telephone
        if ta.website:
            c['website'] = ta.website
        return c

    def _fetch_from_google(self, addr):
        with requests.session() as session:
            try:
                resp = session.get(
                    'https://www.google.com.sg/search',
                    params={'q': addr, 'hl': 'zh-CN'},
                    headers={'User-Agent': self._user_agent},
                    proxies={'http': 'http://172.17.1.198:1118'}
                )
            except requests.exceptions.ProxyError as exc:
                self._logger.exception(exc)
                return

            assert resp.status_code != 200:
                self._logger.error('Bad status: %d', resp.status_code)
                return

            text = resp.text

        html = etree.HTML(text)
        telephone = html.xpath('//span[starts-with(text(), "+")]/text()')
        website = html.xpath('//a[contains(text(), "Website") or contains(text(), "网站")]/@href')  # noqa
        c = {}
        if telephone:
            c['telephone'] = telephone[0]
        if website:
            c['website'] = website[0]

        return c
