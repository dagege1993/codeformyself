#! python
# coding: utf8

from pymongo import MongoClient
# from scripture import settings

m = MongoClient()
mc = MongoClient('mongodb://root:PGJ0ssznC8S2BKBuY@dds-2zefca1b050149b42.mongodb.rds.aliyuncs.com:3717,dds-2zefca1b050149b41.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-3027583')

where = {
    'similarity': {'$gt': []},
    'similarity.0.1': {'$gte': 80}
}

will_update = 0

for sims in m.scripture.jset_name_similarities2.find(where):
    hotel_id = sims['similarity'][0][0]
    in_hub = mc.hub.poi_items.find_one({'hotel_id': str(hotel_id)})
    if not in_hub:
        will_update += 1

print(f'Found {will_update} new hotels')
