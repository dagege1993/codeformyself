# coding: utf8

import requests

from pymongo import MongoClient
from scripture import settings
from scripture.xpath import jetsetter

from yarl import URL
from lxml import etree
from pprint import pprint

hub = MongoClient('mongodb://hub_write:hvAnfbwByFMG27tT@dds-2zefca1b050149b42.mongodb.rds.aliyuncs.com:3717,dds-2zefca1b050149b41.mongodb.rds.aliyuncs.com:3717/hub?replicaSet=mgset-3027583')   # noqa
mc = MongoClient(settings.MONGO)
me = hub.hub.poi_items.find_one({'hotel_id': '44815'})['updatedBy']
sandbox = MongoClient('mongodb://172.17.1.201:27017/hub')

# c = hub.hub.poi_items.find({
#     # 'published': True,
#     '__t': 'Hotel',
#     '$where': 'this.gallery.length<5'
# })

# c = hub.hub.poi_items.find({
#     # 'published': True,
#     '__t': 'Hotel',
#     '$where': 'this.gallery.length<=5'
# })

not_jset = []
not_captured = []
bad_captured = []
updated = []
eight = []
urls = [
    "https://www.jetsetter.com/hotels/san-francisco/california/5736/palace-hotel-a-luxury-collection-hotel-san-francisco",
    "https://www.jetsetter.com/hotels/seoul/south-korea/10275/four-seasons-hotel-seoul",
    "https://www.jetsetter.com/hotels/barcelona/spain/10844/hotel-blancafort-spa-termal",
    "https://www.jetsetter.com/hotels/chicago/illinois/5412/radisson-blu-aqua-hotel-chicago",
    "https://www.jetsetter.com/hotels/san-francisco/california/5723/the-donatello-hotel"
]
for url in urls:
    item = hub.hub.poi_items.find_one({'capture_url': url})
    # if 'capture_url' not in item or not item['capture_url']:
    #     not_captured.append(item['name'])
    #     continue
    jset = mc.scripture.jsets.find_one({'url': url})
    # if not jset:
    #     not_jset.append(item['capture_url'])
    #     continue
    images = etree.HTML(jset['origin_body']).xpath(jetsetter.images)
    if len(images) <= 1:
        # bad_captured.append(item['capture_url'])
        continue
    imgs = set()
    for img in images:
        image_url = URL(img.xpath('./@src')[0].split('?')[0]) \
            .with_scheme('http') \
            .with_host('img3.weegotr.com')
        imgs.add(str(image_url))
    gallery = set()
    uploads = []
    for ga in item['gallery']:
        if 'image' in ga:
            del ga['_id']
            uploads.append(ga)
        elif ga['image_url'] != '':
            gallery.add(ga['image_url'])
    gallery.update(imgs)
    uploads.extend(map(lambda img: {'image_url': img}, gallery))
    updated.append((jset['url'], len(item['gallery']), len(uploads)))
    # sandbox.hub.poi_items.update(
    #     {'_id': item['_id']},
    #     {
    #         '$set': {
    #             'gallery': uploads,
    #             'updatedBy': me
    #         },
    #         '$currentDate': {
    #             'updatedAt': True
    #         }
    #     }
    # )
    data = {'capture_url': jset['url'], 'gallery': uploads}
    # host = 'http://192.168.2.101:8289/api/v3/hotels'
    host = 'http://47.94.77.75/api/v3/hotels'
    resp = requests.post(host, json=data)
    print(resp.status_code, resp.json())
    print('From', len(item['gallery']), 'to', len(uploads))
    mc.scripture.gallery_backup.insert(data)
    if len(uploads) == 8:
        eight.append(jset['url'])
print('not_jset', end=' ')
pprint(not_jset)
print('not_captured', end=' ')
pprint(not_captured)
print('bad_captured', end=' ')
pprint(bad_captured)
print('updated', end=' ')
pprint(updated)
