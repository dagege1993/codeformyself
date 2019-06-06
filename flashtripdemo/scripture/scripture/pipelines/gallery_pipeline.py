# coding: utf8

import logging

from twisted.internet import defer

from scripture.models.txgallery import TxGallery


class GalleryPipeline():
    def __init__(self, settings):
        self.settings = settings
        self._process = lambda x, y: y
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        try:
            item = yield self._process(item)
        except Exception as e:
            print(e)
            self.logger.error('Exception', exc_info=e)
        return item

    def open_spider(self, spider):
        if spider.name == 'hcom':
            self._process = self._hcom_dispatcher
        elif spider.name == 'distributed_spider':
            self._process = self._distributed_spider

    @defer.inlineCallbacks
    def _hcom_rooms(self, item, key):
        for room in item[key]:
            room['images'] = yield self._hcom_images(room['images'])
        return item

    @defer.inlineCallbacks
    def _hcom_dispatcher(self, item):
        if item.get('locale'):
            pictures = item.get('pictures', [])
            item['pictures'] = yield self._hcom_images(pictures)
        elif 'rooms' in item:
            item = yield self._hcom_rooms(item, 'rooms')
        elif 'en.rooms' in item:
            item = yield self._hcom_rooms(item, 'en.rooms')
        return item

    @defer.inlineCallbacks
    def _hcom_images(self, pictures):
        for img in pictures:
            img['image_url'] = (yield TxGallery()
                                .get_image_url(img['url'], img.get('sizes')))
        self.logger.debug('Handled hcom pictures, %s', pictures)
        return pictures

    @defer.inlineCallbacks
    def _booking_dispatcher(self, item):
        bk_gallery = item.get('gallery', [])
        if bk_gallery:
            item['gallery'] = yield self._booking_images(bk_gallery)
        if 'rooms' in item:
            item = yield self._booking_rooms(item, 'rooms')
        return item

    @defer.inlineCallbacks
    def _booking_images(self, pictures):
        for img in pictures:
            img['wg_image_url'] = (yield TxGallery()
                                   .get_image_url(img['image_url']))
        self.logger.debug('Handled booking pictures, %s', pictures)
        return pictures

    @defer.inlineCallbacks
    def _booking_rooms(self, item, key):
        for room in item[key]:
            room['gallery'] = yield self._booking_images(room['gallery'])
        return item

    @defer.inlineCallbacks
    def _distributed_spider(self, item):
        spider_name = item.get('spider_name')[0]
        if spider_name == 'hcom_page':
            yield self._hcom_dispatcher(item)
        elif spider_name == 'booking_page':
            yield self._booking_dispatcher(item)
        return item