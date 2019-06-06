# coding: utf8

import logging

import numpy
import pandas

from yarl import URL
from pymongo import MongoClient

from scripture import settings

from scripture.models.similarity import Similarity

mc = MongoClient(settings.MONGO)
# mc = MongoClient()
local_mc = MongoClient()

logging.basicConfig(
    format='%(asctime)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO
)


def hcom(csvfile):
    logger = logging.getLogger(__name__)
    # query = {'en.city': {'$exists': 1}, 'notice.其它名称': {'$exists': 1}}
    city_map = {
        '巴厘岛': 'Bali',
        '普吉岛': 'Phuket',
        '马尔代夫': 'Maldives',
        '沙巴': 'Sabah',
        '北海道': 'Hokkaido',
        '京都': 'Kyoto',
        '箱根': 'Hakone',
        '大阪': 'Osaka',
        '东京': 'Tokyo',
        '苏梅岛': 'Koh Samui',
        '冲绳': 'Okinawa',
        '大溪地': 'Tahiti',
        '斐济': 'Fiji'
    }
    city_id_map = {
        'Bali': '16956',
        'Phuket': '18778',
        'Maldives': '17412',
        'Sabah': {'Sandakan': '17401', 'Kota Kinabalu': '17381'},
        'Kyoto': '17246',
        'Hakone': {'Hakone': '17204', 'Numazu': '17280'},
        'Osaka': '17286',
        'Tokyo': '17303',
        'Hokkaido': {
            'Sapporo': '17290',
            'Niseko': '183146',
            'Otaru': '7657460',
            'Hakodate': '17203',
        },
        'Koh Samui': '18749',
        'Okinawa': '17285',
        'Tahiti': '16512',
        'Fiji': {
            'Malololailai': '16313',
            'Denarau Island': '16310',
            'Natadola Beach': '64711',
            'Savusavu': '16324',
            'Suva': '16325',
            'Castaway Island': '16308',
            'Naigani Island': '16319',
            'Toberua Island': '64885',
            'Labasa': '183156',
            'Pacific Harbour': '16321',
            'Vuda Point': '16329',
            'Momi Bay': '16317',
            'Beqa Island': '16307',
            'Yaqeta Island': '16330',
            'Matangi Island': '16316',
            'Nadi': '16318',
            'Lautoka': '16312',
            'Nanuya Lailai Island': '16320',
            'Taveuni': '16326',
            'Vomo Island': '16328',
            'Matamanoa Island': '16315',
            'Coral Coast': '16309',
            'Nananu Island': '91482',
            'Kadavulailai Island': '16311',
            'Mana Island': '16314',
            'Malolo Island': '64812',
            'Plantation Island': '16322',
            'Beachcomber Island': '64687',
            'Rakiraki': '16323',
            'Bekana Island': '64827',
            'Treasure Island': '16327',
            'Tokoriki Island': '91506',
        }
    }
    mapping = {}
    df = pandas.DataFrame.from_csv(csvfile)
    for city, row in df.iterrows():
        url = row.get('hotels_URL') != numpy.NAN and \
            row.get('hotels_URL') or \
            row.get('hotels_url')
        hotels_id = URL(url).query.get('hotel-id')
        mapping[hotels_id] = city_map[city]
    query = {'hotels_id': {'$in': list(mapping.keys())}}
    only = {
        'notice.其它名称': 1,
        'en.city': 1,
        'en.name': 1,
        'en.notice': 1,
        'hotels_id': 1,
        'address': 1
    }
    cursor = mc.scripture.hotels.find(query, only, no_cursor_timeout=True)
    for h in cursor:
        if 'en' not in h:
            logger.warn('Bad info of hotels %s', h['hotels_id'])
            continue
        # city = h['en']['city']
        city = mapping[h['hotels_id']]
        names = h['notice']['其它名称']
        if not names:
            names = []
            try:
                names.append(h['en'].get('name'))
            except Exception:
                logger.error('Hotel %s name is empty!', h['hotels_id'])
            names.extend(h['en']['notice']['alias'] or [])
        _city_id = city_id_map[city]
        _city_id = isinstance(_city_id, (str, int)) and _city_id \
            or list(_city_id.values())
        similarity = Similarity.load(
            city,
            mongoclient=mc,
            city_id=_city_id
        )
        logger.debug('%s -|- %s', city, names)
        mapped = map(
            lambda name: list(similarity.top_10(name, gte=30)),
            filter(None, names)
        )
        for m in mapped:
            doc = {
                'city': city,
                'hotels_id': h['hotels_id'],
                'address': h['address'],
                'similarity': list(m)
            }
            local_mc.scripture.hcom_similarities.insert_one(doc)

    cursor.close()


if __name__ == '__main__':
    try:
        hcom()
    except KeyboardInterrupt:
        mc.close()
