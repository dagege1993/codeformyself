# coding: utf8

import requests
import logging
from lxml import objectify
import re
from aiohttp import BasicAuth
from tasks import settings

# Current Project
from . import Providers, BaseSupplier

language_map = {
    "eng": 'en',
    "chi": 'cn',
    "jpn": 'jp'
}

logger = logging.getLogger(__name__)

update_data_endpoint = f'{settings.QUOTES}/api/v6/relux/static'

class ReluxHotel(BaseSupplier):

    supplier = Providers.relux

    hotels_endpoint = "https://partner-cdn.rlx.jp/static-file/sales-hotel/hotels"
    
    def hotels(self, language):
        resp = requests.get(
                f"{self.hotels_endpoint}_{language}.json"
            ).json()
        for _hotel in resp["hotels"]:
            hotel = {}
            hotel['code'] = str(_hotel['id'])
            if _hotel.get('postcode'):
                province = self.get_province_by_postal_code(
                        _hotel['postcode'], "JP"
                )
                if province:
                    hotel['province'] = province
            all_facility = []
            facility_with_detail = _hotel.get('facility', '').split('\n\n')
            facility_only_tag = _hotel.get('tags', [])
            facility_bath = _hotel.get('bath', '').split('\n')
            for faci in facility_with_detail:
                _faci = faci.split('\n')[0].replace('・', '')
                if not _faci:
                    continue
                all_facility.append({'facility': _faci})
            for faci in facility_only_tag:
                _faci = faci.get('name', '').replace('■', '').replace('・', '').replace('※', '')
                if not _faci or faci.get('status', 0) == 0:
                    continue
                all_facility.append({'facility': _faci})
            for faci in facility_bath:
                if not faci:
                    continue
                all_facility.append({'facility': faci})
            _hotel['facility'] = all_facility
            _hotel['facility_with_detail'] = facility_with_detail
            _traffic_info = {}
            for key, value in _hotel.get('access', {}).items():
                if 'For' not in key:
                    logger.debug(f"unknown access key : {key}")
                    continue
                tag, title = key.split('For')
                if title not in _traffic_info:
                    _traffic_info[title] = {'traffic': "", 'destination': ''}
                if tag == "description":
                    _traffic_info[title]['destination'] = re.sub('\n{2,}', '\n', value).replace('※', '')
                elif tag == "title":
                    _traffic_info[title]['traffic'] = value
                else:
                    logger.debug(f"unknown tag : {tag}")
            _hotel['traffic_info'] = list(_traffic_info.values())
            policy = []
            policy.append({'type': '注意事项', 'content': _hotel.get('notice', '').replace('・', '')})
            policy.append({'type': "服务须知", 'content': _hotel.get('service', '').replace('※', '')})
            policy.append({'type': '接受的信用卡', 'content': '、'.join([name['name'] for name in _hotel.get('cards', {})])})
            _hotel['policy'] = policy
            hotel['wgstar'] = _hotel.get('grade', 0)
            gallery = [{'image_url': url['url']} for url in _hotel.get('pictures')]
            hotel['gallery'] = gallery
            if language == "eng":
                for key, value in _hotel.items():
                    hotel[key] = value
            else:
                for key, value in _hotel.items():
                    if key in [
                        'id', 'postcode',
                        'ruby', 'wgstar', 'province',
                        'grade', 'url', 'popularity',
                        'mail', 'tel', 'latitude',
                        'longitude', 'cards', 'pictures',
                    ]:
                        hotel[key] = value
                    else:
                        hotel[f"{key}_{language_map[language]}"] = value
            self.save(hotel, "hotels")
            

class ReluxRooms(BaseSupplier):

    supplier = Providers.relux_rooms
    rooms_endpoint = "https://partner-cdn.rlx.jp/static-file/sales-room/rooms"

    def rooms(self, language):
        resp = requests.get(
            f"{self.rooms_endpoint}_{language}.json"
        ).json()
        for _hotel in resp["hotels"]:
            hotel = {}
            hotel['code'] = str(_hotel['id'])
            hotel['id'] = _hotel['id']
            _hotel['rooms'] = fix_character(_hotel['rooms'])
            if language == "eng":
                hotel['rooms'] = _hotel['rooms']
            else:
                hotel[f"rooms_{language_map[language]}"] = _hotel['rooms']
            self.save(hotel, "hotels")


def fix_character(rooms):
    for room in rooms:
        room['name'] = replace_character(room['name'])
        room['description'] = replace_character(room['description'])
        for plan in room['plans']:
            plan['name'] = replace_character(plan['name'])
            plan['feature'] = replace_character(plan['feature'])
            plan['meal']['content'] = replace_character(plan['meal']['content'])
    return rooms


def replace_character(seq):
    if not seq:
        return ""
    seq = (
            seq.replace('【', '[').replace('】', ']')
            .replace('〜', '').replace('，', ',')
            .replace('！', '!').replace('「', ' ')
            .replace('」', ' ').replace('·', '')
            .replace('～', '').replace('：', ':')
            .replace('※', '').replace('&lt;', '')
            .replace('&gt;', '').replace('\n=', ' ')
            .replace('■', '').replace('□', '')
            .replace('◇', '').replace('◆', '')
            .replace('？', '?').replace('', '')
            .replace('（', '(').replace('）', ')')
            .replace('。', '.').replace('⇒', '')
            .replace('＋', '').replace('+', '')
            .replace('《', '').replace('》', '')
            .replace('★', '').replace('为Relux会员们', '')
            .replace('＜', ' ').replace('＞', '')
            .replace('『', '').replace('』', '')
            .replace('-', '').replace('如有需要请向Relux礼宾部咨询', '')
            .replace('如有需要请向Relux咨询台咨询', '').replace('', '')
            .replace('・', '').replace('－', '')
            .replace('〉', '>').replace('〈', '<')
            .replace('①', '1').replace('②', '2')
            .replace('③', '3').replace('④', '4')
            .replace('⑤', '5').replace('⑥', '6')
        )
    return seq

def update_quotes(code):
    payload = {
        'quoter_id': '5bc41308bca48f00449c431d',
        'hotel_id': int(code)
    }
    resp = requests.post(update_data_endpoint, json=payload)
    if resp.status_code != 200:
        logger.error(f"update quotes relux statics data fail {resp.json()['error_message']}")
    return resp.json().get('message', '') or resp.json().get('error_message', '')
