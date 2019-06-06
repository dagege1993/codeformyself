import json
from bson import ObjectId
from pymongo import MongoClient

mc = MongoClient()

filename = 'ten_after.json'

mapping = []

with open(filename) as f:
    for line in f.readlines():
        mapping.append(json.loads(line.strip()))

oids = [ObjectId(_map['name']) for _map in mapping]


def find(oid):
    for _map in mapping:
        if _map['name'] == str(oid):
            return _map
    return {}


for item in mc.hub.poi_items.find({'_id': {'$in': oids}}):
    must_be_dropped = find(item['_id']).get('urls')
    if not must_be_dropped:
        print('Bad oid:', item['_id'])
        continue
    cleaned = []
    o_cnt = len(item['gallery'])
    for gallery in item['gallery']:
        if gallery['image_url'] not in must_be_dropped:
            cleaned.append(gallery)
        else:
            must_be_dropped.remove(gallery['image_url'])
    n_cnt = len(cleaned)
    mc.hub.poi_items.update_one(
        {'_id': item['_id']},
        {'$set': {'gallery': cleaned}}
    )
    print('Updated successful', o_cnt, n_cnt, item['_id'])
