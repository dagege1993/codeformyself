# coding: utf8

import json
import pathlib
import logging

import oss2
import pandas as pd
from pymongo import MongoClient
from tasks import settings


scripture = MongoClient('mongodb://172.16.4.110/scripture').scripture

c = scripture.statics.hotels.hotelbeds.find()

o = oss2.Bucket(
    oss2.Auth(
        settings.ALIYUN_ACCESS_KEY_ID,
        settings.ALIYUN_ACCESS_KEY_SECRET
    ),
    'http://oss-cn-beijing.aliyuncs.com',
    'weegotr-statics'
)
#     [
#         {
#             '$group': {'_id': '$city', 'hotels': {'$push': '$$ROOT'}}
#         }
#     ]
# )

# {'_id': ObjectId('59e74dd46fdf1e7a80a78da3'),
#  'address': 'AVENIDA JUST MARLES,21-23  ',
#  'category': '4 STARS',
#  'city': 'LLORET DE MAR',
#  'country_code': 'ES',
#  'destination_code': 'LLM',
#  'email': 'booking@hoteldelamarlloret.com',
#  'hotel_id': 102342.0,
#  'latitude': 41.698847,
#  'longitude': 2.844205,
#  'name': 'Delamar',
#  'postal_code': '17310',
#  'website': 'www.hoteldelamar.com',
#  'zone_code': 99.0}
# for h in c:
#     s = 0
#     star = h.get('category').lower()
#     if 'star' in star:
#         s = int(star[0])
#     if s < 4:
#         continue
#     city = h.get('city', '').title()
#     country = h.get('country_code')
#     hotel = {
#         'id': int(h['hotel_id']),
#         'hotel': h.get('name', '').title(),
#         '星级': s,
#         'city': city,
#         'country': country,
#         'address': h.get('address')
#     }
#     with open(f'hotels/{city.replace("/", "_")}_{country}.txt', 'a') as f:
#         f.write(json.dumps(hotel))
#         f.write(',\n')

path = pathlib.Path('hotels')
files = []
for f in path.glob('*.txt'):
    ll = []
    try:
        for x in f.read_text().splitlines():
            ll.append(json.loads(x[:-1]))
    except Exception as exc:
        logging.error('Bad json file, %s', f, exc_info=exc)
    if len(ll) < 5:
        continue
    df = pd.DataFrame.from_dict(ll)
    excel = ''.join([str(f)[:-3], 'xlsx'])
    df.to_excel(excel)

    excelpath = pathlib.Path(excel)

    resp = o.put_object_from_file(
        f'statics/hotels/hotelbeds/{excelpath.name}',
        excelpath
    )
    assert resp.status == 200
    files.append(
        f'https://img2.weegotr.com/statics/hotels/hotelbeds/{excelpath.name}'
    )

with open('filelist.txt', 'w') as filelist:
    filelist.write('\n'.join(files))
