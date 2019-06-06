#! python3
# coding: utf8

import time
from datetime import datetime
from pymongo import MongoClient

backup_poiup_mongo = MongoClient()

online_mongo = MongoClient('mongodb://root:PGJ0ssznC8S2BKBuY@dds-2zefca1b050149b42.mongodb.rds.aliyuncs.com:3717,dds-2zefca1b050149b41.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-3027583')  # noqa

recovery_date = datetime.strptime('2017-07-12 00:00:00', '%Y-%m-%d %H:%M:%S')

cnt = 0


def main():
    c = online_mongo.hub.poi_items.find(
        {
            # 'updatedAt': {'$gte': recovery_date},
            'published': True,
            '__t': 'Hotel',
            'cover_image_url': ''
        },
        no_cursor_timeout=True
    )

    cnt = 0
    for poi in c:
        backup_poi = backup_poiup_mongo.hub.poi_items.find_one({
            '_id': poi['_id']
        })
        if not backup_poi:
            continue

        set_item = {}

        b_introduction = backup_poi.get('introduction')
        p_introduction = poi.get('introduction')
        if b_introduction != p_introduction \
                and isinstance(b_introduction, (str, bytes)) \
                and b_introduction.strip() != '':

            set_item['introduction'] = b_introduction
            # cnt += 1
            # print(b_introduction, p_introduction, sep=' -|- ')

        b_short_introduction = backup_poi.get('short_introduction')
        p_short_introduction = poi.get('short_introduction')
        if b_short_introduction != p_short_introduction \
                and isinstance(b_short_introduction, (str, bytes)) \
                and b_short_introduction.strip() != '':
            set_item['short_introduction'] = b_short_introduction

        b_tips = backup_poi.get('tips')
        p_tips = poi.get('tips')
        if b_tips != p_tips \
                and isinstance(b_tips, (str, bytes)) \
                and b_tips.strip() != '':
            set_item['tips'] = b_tips

        b_traffic_tips = backup_poi.get('traffic_tips')
        p_traffic_tips = poi.get('traffic_tips')
        if b_traffic_tips != p_traffic_tips \
                and isinstance(b_traffic_tips, (str, bytes)) \
                and b_traffic_tips.strip() != '':

            set_item['traffic_tips'] = b_traffic_tips

        b_cover_image_url = backup_poi.get('cover_image_url')
        p_cover_image_url = poi.get('cover_image_url')
        if b_cover_image_url != p_cover_image_url \
                and isinstance(b_cover_image_url, (str, bytes)) \
                and b_cover_image_url.strip() != '':

            set_item['cover_image_url'] = b_cover_image_url

        b_city_name = backup_poi.get('city_name')
        p_city_name = poi.get('city_name')
        if b_city_name != p_city_name \
                and isinstance(b_city_name, (str, bytes)) \
                and b_city_name.strip() != '':
            set_item['city_name'] = b_city_name

        # b_recommend_reason = backup_poi.get('recommend_reason')
        # p_recommend_reason = poi.get('recommend_reason')
        # if b_recommend_reason != p_recommend_reason:
        #     set_item['recommend_reason'] = b_recommend_reason

        b_comments_from = backup_poi.get('comments_from')
        p_comments_from = poi.get('comments_from')
        if b_comments_from != p_comments_from \
                and isinstance(b_comments_from, (str, bytes)) \
                and b_comments_from.strip() != '':

            set_item['comments_from'] = b_comments_from

        b_comments_url = backup_poi.get('comments_url')
        p_comments_url = poi.get('comments_url')
        if b_comments_url != p_comments_url \
                and isinstance(b_comments_url, (str, bytes)) \
                and b_comments_url.strip() != '':
            set_item['comments_url'] = b_comments_url

        if not set_item:
            continue

        if backup_poi['published'] is False:
            set_item['published'] = False
        #     continue

        # if 'recommend_reason' in set_item\
        #         or 'comments_url' in set_item \
        #         or 'comments_from' in set_item \
        #         or 'city_name' in set_item \
        #         or 'traffic_tips' in set_item \
        #         or 'short_introduction' in set_item \
        #         or 'tips' in set_item \
        #         or 'introduction' in set_item:
        #     continue

        update = online_mongo.hub.poi_items.update_one(
            {'_id': poi['_id']},
            {'$set': set_item}
        )
        print(poi['_id'], update.modified_count)
        print(set_item)
        # time.sleep(0.1)
        cnt += 1
    print(cnt)


if __name__ == '__main__':
    main()
