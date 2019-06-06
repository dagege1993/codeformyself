# coding: utf-8
"""
原hcom表内的房型数据导出到新表hcom_rooms_zh和hcom_rooms_en
复用原表房型_id字段值
2017-8-22 by liuhao
"""

from pymongo import MongoClient
from scripture.settings import MONGO


mc = MongoClient(MONGO)
all_data = mc.scripture.hotels.find({}, no_cursor_timeout=True)

db_zh = mc.scripture.hcom_rooms_zh
db_en = mc.scripture.hcom_rooms_en


def insert_to_db(rooms, hotels_id, db):
    if rooms is not None:
        for room in rooms:
            room.update({'hcom_id': hotels_id})
            obj_id = room.get('_id')
            room_type_code = room.get('room_type_code')
            if room_type_code:
                _id = db.insert(room)
                if obj_id:
                    assert obj_id == _id
            elif room_type_code is None:
                pass
            else:
                raise TypeError(room_type_code)


def main():
    for data in all_data:
        has_rooms_cn = data.get('rooms')
        has_rooms_en = data.get('en', {}).get('rooms')
        hotels_id = data.get('hotels_id')
        insert_to_db(has_rooms_cn, hotels_id, db_zh)
        insert_to_db(has_rooms_en, hotels_id, db_en)


if __name__ == '__main__':
    main()
