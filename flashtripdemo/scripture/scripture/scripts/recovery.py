#! python3
# coding: utf8


from datetime import datetime
from pymongo import MongoClient

backup_poiup_mongo = MongoClient()

online_mongo = MongoClient('mongodb://root:PGJ0ssznC8S2BKBuY@dds-2zefca1b050149b42.mongodb.rds.aliyuncs.com:3717,dds-2zefca1b050149b41.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-3027583')  # noqa

recovery_date = datetime.strptime('2017-07-12 00:00:00', '%Y-%m-%d %H:%M:%S')


def main():
    c = online_mongo.hub.poi_items.find(
        {
            'updatedAt': {'$gte': recovery_date},
            'published': False
        },
        no_cursor_timeout=True
    )

    for poi in c:
        backup_poi = backup_poiup_mongo.hub.poi_items.find_one({
            '_id': poi['_id']
        })
        if not backup_poi:
            continue

        set_item = {}

        b_introduction = backup_poi.get('introduction')
        p_introduction = poi.get('introduction')
        if b_introduction != p_introduction:
            set_item['introduction'] = b_introduction

        b_short_introduction = backup_poi.get('short_introduction')
        p_short_introduction = poi.get('short_introduction')
        if b_short_introduction != p_short_introduction:
            set_item['short_introduction'] = b_short_introduction

        b_tips = backup_poi.get('tips')
        p_tips = poi.get('tips')
        if b_tips != p_tips:
            set_item['tips'] = b_tips

        b_traffic_tips = backup_poi.get('traffic_tips')
        p_traffic_tips = poi.get('traffic_tips')
        if b_traffic_tips != p_traffic_tips:
            set_item['traffic_tips'] = b_traffic_tips

        b_cover_image_url = backup_poi.get('cover_image_url')
        p_cover_image_url = poi.get('cover_image_url')
        if b_cover_image_url != p_cover_image_url:
            set_item['cover_image_url'] = b_cover_image_url

        b_city_name = backup_poi.get('city_name')
        p_city_name = poi.get('city_name')
        if b_city_name != p_city_name:
            set_item['city_name'] = b_city_name

        b_recommend_reason = backup_poi.get('recommend_reason')
        p_recommend_reason = poi.get('recommend_reason')
        if b_recommend_reason != p_recommend_reason:
            set_item['recommend_reason'] = b_recommend_reason

        b_comments_from = backup_poi.get('comments_from')
        p_comments_from = poi.get('comments_from')
        if b_comments_from != p_comments_from:
            set_item['comments_from'] = b_comments_from

        b_comments_url = backup_poi.get('comments_url')
        p_comments_url = poi.get('comments_url')
        if b_comments_url != p_comments_url:
            set_item['comments_url'] = b_comments_url

        if not set_item:
            continue

        update = online_mongo.hub.poi_items.update_one(
            {'_id': poi['_id']},
            {'$set': set_item}
        )
        print(poi['_id'], update.modified_count)
        print(set_item)


if __name__ == '__main__':
    main()
