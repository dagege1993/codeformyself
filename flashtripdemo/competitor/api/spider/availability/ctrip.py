# coding: utf-8
import re
import json
import logging
import aiohttp
from bson import ObjectId
from datetime import datetime, timedelta
from lxml import etree
from yarl import URL
from bson import ObjectId


from api.spider.base_spider import BaseSpider
from api.utils.database import databases, redis_db
from api.utils import generate
from api.settings import configs
from api.types.consts import const

class CtripSpider(BaseSpider):

    def __init__(self, hotel_id = None, name=None, ctrip_id=None, ctrip_city_id=None, **kwargs):
        self.name = name
        self.ctrip_id = ctrip_id
        self.is_oversea = None
        self.city_id = ctrip_city_id
        self.hotel_id = hotel_id
        self.ctrip_name = 'id来源为cms，非从携程上抓取'
    
    async def refresh_hotel_msg(self):
        if not self.ctrip_id:
            if not self.name:
                await self.get_hotel_name()
            self.ctrip_id = await self.get_hid(self.name)
        return True
    

    def __str__(self):
        return f"spider_name:{{ctrip}}, hotel_name: {{{self.name}}}, ctrip_name: {{{self.ctrip_id}}}, " \
               f"is_over_sea: {{{self.is_oversea}}}, ctrip_city_id: {{{self.city_id}}}, " \
               f"cms_id: {{{self.hotel_id}}}"
            

    async def before_crawl(self, msg):
        '''
        msg: {'hotel_id': , 'checkin': '%Y-%m-%d', 'checkout': '%Y-%m-%d', 'roomfilters': }
        '''
        if not self.ctrip_id:
            if not self.name:
                await self.get_hotel_name()
            if not self.ctrip_id:
                self.ctrip_id, self.ctrip_name = await self.find_ctrip_msg(self.name)
        if not self.ctrip_id or self.ctrip_id == 'not match':
            return ""
        inday = msg['checkin'].replace('-', '/')
        outday = msg['checkout'].replace('-', '/')
        query = {
                'inday': inday,
                'outday': outday,
                'subchannel': '',
                'hotelchannel': '1',
                'isoversea': '1' if self.is_oversea else '0',
                'ismorning': '0',
                'adult': msg['roomfilters'][0]['adults'],
                'child': child_formatter(msg['roomfilters'][0].get('children', [])),
            }
        if query['child'] == '-1,-1,-1':
            query.pop('child')
        return URL(f"http://m.ctrip.com/webapp/hotel/j/hoteldetail/dianping/rooms/{self.ctrip_id}").with_query(query)

    
    async def handler(self, response, **kwargs):
        logger = logging.getLogger(__name__)
        text = await response.text()
        et = etree.HTML(text)
        ori_json = et.xpath('*//input[@class="model_data"]/@data-roomlistinfo')
        if not ori_json:
            return {}

        data = json.loads(ori_json[0])
        rooms = data['rooms']

        min_no_meal_room = min_breakfast_room = None
        min_room = {}
        min_no_meal_price = min_breakfast_price = None
        for room in rooms:
            room_type = room['bname']
            current_price = room.get('priceInfo', {}).get('cnyTotalPrice', '')
            if not current_price:
                continue
            meal = room.get('bookChangeCheck', {}).get('breakfastCount') != '0'
            if room_type not in min_room:
                min_room[room_type] = {'meal': None, 'no_meal': None, 'no_meal_price': 9999999999, 'price': 99999999}
            current_room = min_room[room_type]
            current_price = float(current_price) * 0.95
            if not current_room['no_meal'] and not meal:
                current_room['no_meal'] = room
                current_room['no_meal_price'] = current_price
            elif not meal and current_room['no_meal_price'] > current_price:
                current_room['no_meal'] = room
                current_room['no_meal_price'] = current_price
            elif not current_room['meal'] and meal:
                current_room['meal'] = room
                current_room['price'] = current_price
            elif meal and current_room['price'] > current_price:
                current_room['meal'] = room
                current_room['price'] = current_price
            min_room[room_type] = current_room
        if not min_room:
            return {}
        min_room_types = sorted(min_room, key=lambda x: min_room[x]['no_meal_price'])
        rooms = []
        for mrt in min_room_types[:2]:
            if min_room[mrt]['meal']:
                rooms.append(min_room[mrt]['meal'])
            if min_room[mrt]['no_meal']:
                rooms.append(min_room[mrt]['no_meal'])
        if not self.city_id:
            self.city_id = await self.get_ctrip_city_id()
        days = (
            datetime.strptime(kwargs['checkout'], '%Y-%m-%d') 
            - datetime.strptime(kwargs['checkin'], '%Y-%m-%d')
        ).days
        room_num = int(len(kwargs['roomfilters']))
        avai_rooms = [
            {
                'room_type': re.sub('(携.*?程)', '', room['bname']), 
                'meal_type': 'Breakfast' if room.get('bookChangeCheck', {}).get('breakfastCount') else '' , 
                'use_tips': '', 
                'price': (float(room.get('priceInfo', {}).get('cnyTotalPrice', '')) *.95) / days / room_num, 
                'total_price': float(room.get('priceInfo', {}).get('cnyTotalPrice', '')) *.95,
                'cancel_rules': cancel_rule_formatter(room.get('bookChangeCheck', {})),
                'key': await self.make_prep_key(kwargs, room),
                'unique_info': {},
            }
            for room in rooms
        ]
        logger.info(f"avai_rooms: {avai_rooms}")
        _prep_room = [
            await self.prep(room['key'][0], room['key'][1], room['key'][0])
            for room in avai_rooms
        ]
        logger.info(f"_prep_room: {_prep_room}")
        prep_room = []
        for room in _prep_room:
            if not room['room_type']:
                continue
            room.pop('currency')
            room.pop('timezone')
            room.pop('hotel_name')
            prep_room.append(room)

        return prep_room
    
    async def crawl(self, sess, **kwargs):
        hotel_url = await self.before_crawl(kwargs)
        if not hotel_url:
            return {}
        async with sess.get(hotel_url) as resp:
            return await self.handler(resp, **kwargs)


    async def find_ctrip_msg(self, name=None):
        logger = logging.getLogger(__name__)
        async with aiohttp.ClientSession() as sess:
            async with sess.get(f"http://m.ctrip.com/restapi/h5api/searchapp/search?action=autocomplete&source=globalonline&keyword={name or self.name}") as resp:
                if resp.status != 200:
                    return False
                data = await resp.text()
                data = json.loads(data)
                if not data['data']:
                    return 'not find!', 'not find!'
                ctrip_id = data['data'][0]['url'].split('/')[-1].replace('.html', '')
                try:
                    int(ctrip_id)
                except Exception as exc:
                    logger.warning(f"{name} find ctrip id failed!")
                    ctrip_id = 'not find!'
                ctrip_name = data['data'][0]['word']
                return ctrip_id, ctrip_name
    
    async def get_ctrip_city_id(self):
        logger = logging.getLogger(__name__)
        if not self.ctrip_id:
            if not self.name:
                await self.get_hotel_name()
            self.ctrip_id, self.ctrip_name = await self.find_ctrip_msg()
        data = {}

        async with aiohttp.ClientSession() as sess:
            async with sess.get(f"http://m.ctrip.com/webapp/hotel/oversea/hoteldetail/{self.ctrip_id}.html") as resp:
                text = await resp.text()
                cityid = re.findall('"cityid":(\d+),', text)
                if cityid:
                    self.city_id = int(cityid[0])
                    return
                # 如果正则未找到则用xpath解析json
                et = etree.HTML(text)
                data_script = et.xpath('*//script[@id="pageData"]')
                if not data_script:
                    logger.error(f'{self.ctrip_id} find city id failded!')
                    return ''
                try:
                    data = json.loads(
                        re.findall(
                            'var __HOTEL_PAGE_DATA__ = (.*?)\n',
                            data_script[0].xpath('.//text()')[0]
                        )[0][:-2]
                    )
                except json.decoder.JSONDecodeError as exc:
                    logger.warning(f"{self.ctrip_id} find city id failed with json loads")
                if not data or not data.get('cityid'):
                    logger.warning(f"cityid_text : {text}")
                self.city_id = data.get('cityid', '')


    async def get_hotel_name(self):
        hub = databases('hub')
        hotel_name = await hub['poi_items'].find_one({"_id": ObjectId(self.hotel_id)}, {'name_en', 'city', 'crawl_info'})
        if hotel_name.get('crawl_info'):
            for web in hotel_name.get('crawl_info', []):
                if web.get('crawl_website', '') == 'ctrip_id':
                    self.ctrip_id = web.get('crawl_url', '')
        self.is_oversea = await over_sea_check(hotel_name['city'])
        self.name = hotel_name['name_en']
    

    async def make_prep_key(self, msg, room):
        if not self.city_id:
            await self.get_ctrip_city_id()

        rds = await redis_db('redis')
        query_dict = dict(
            rcount = len(msg.get('roomfilters', [{}])),
            indate = msg['checkin'].replace('-', ''),
            outdate = msg['checkout'].replace('-', ''),
            shadowid = room['shadowId'],
            rateid = room['rateid'],
            ceckid = room['ceckid'],
            roomid = room['id'],
            cityid = self.city_id,
            paytype = find_paytype(room['roomfeatures']),
        )
        query_dict.update(room['bookChangeCheck'])
        query = dict(
            query = query_dict,
            hotel_id = self.hotel_id,
            website = 'ctrip',
        )
        rds_key = generate(24)
        await rds.psetex(f"competitor::prep::{rds_key}", configs[const.REDIS_EXPIRE_TIME], json.dumps(query))
        
        return rds_key, query_dict

    async def prep(self, key, query, old_key = None):
        logger = logging.getLogger(__name__)
        rds = await redis_db('redis')
        data = await rds.get(f"competitor::result::{key}")
        if data:
            return json.loads(data)
        url = URL('http://m.ctrip.com/webapp/hotel/booking')
        query_params = {
            'frflag': 'detail',
            'sct':"H5overseas",
            # "paytype": '0', 
            "hotelid": self.ctrip_id,
        }
        days = (
            datetime.strptime(query['outdate'], '%Y%m%d') 
            - datetime.strptime(query['indate'], '%Y%m%d')
        ).days
        rooms = int(query['rcount'])
        query_params.update(query)
        logger.info(f"query_params: {query_params}")
        url = url.with_query(query_params)
        async with aiohttp.ClientSession() as sess:
            async with sess.get(url) as resp:
                text = await resp.text()
                et = etree.HTML(text)
                data = self.prep_handler(et, days, rooms, str(url), old_key)
                await rds.psetex(f"competitor::result::{key}", configs[const.REDIS_EXPIRE_TIME], json.dumps(data))
                return data
    
    def prep_handler(self, et, days, rooms, url, old_key):
        logger = logging.getLogger(__name__)
        price = ''.join([e.strip() for e in et.xpath('*//div[@class="pay-total"]//text()') if e.strip()])
        price = re.findall('\d+\.?\d*', price)
        if price:
            price = float(price[0]) - 10
            avg_price = price/days/rooms
        else:
            price = ''
            avg_price = ''
        room_type = et.xpath('*//div[@class="bk-cell-num"]/h2/text()')
        if not room_type:
            room_type = ''
            logger.error(f"{url} xpath for room_type failded!")
        else:
            room_type = room_type[0]
        meal_type = None if '不含早餐' in ''.join(et.xpath('.//text()')) else "Breakfast"
        cancel_policy = "".join([e.strip() for e in et.xpath('*//p[@class="ellips"]//text()') if e.strip()]).replace('•', '').replace('&nbsp', '')
        msg = {
            'room_type': re.sub('(携.*?程)', '', room_type),
            'meal_type': meal_type,
            'use_tips': '',
            'price': avg_price,
            'total_price': price,
            'cancel_policy': cancel_policy,
            'timezone': '+08:00:00',
            'unique_info': {'book_url': url},
            'key': old_key or generate(24),
            'currency': "CNY",
            'hotel_name': self.name,
        }
        return msg


async def over_sea_check(city_id):
    hub = databases('hub')
    if isinstance(city_id, str):
        city_id = ObjectId(city_id)
    city = await hub['meta_cities'].find_one({"_id": city_id}, {'country'})
    country = await hub['meta_countries'].find_one({"_id": city['country']}, {'name'})
    if country and country['name'] != '中国':
        return True
    else:
        return False


def cancel_rule_formatter(rules):
    if rules.get('cancelTagType') != 'TIME_LIMIT_CANCEL':
        return []
    elif rules.get('cancelLimitTime'):
        return [
            {
                'policy_from': datetime.now().strftime("%Y-%m-%d %H:%M:00"), 
                'policy_to': datetime.strptime(rules['cancelLimitTime'], '%Y%m%d%H%M').strftime("%Y-%m-%d %H:%M:00"),
                'policy_fee': '0',
            }
        ]


def child_formatter(child):
    if not child:
        return '-1,-1,-1'
    res = ['-1', '-1', '-1']
    for i, e in enumerate(child):
        res[i] = str(e)
    return ','.join(res)


def find_paytype(roomfeatures):
    for rf in roomfeatures:
        if rf['ftype'] != 'paytype':
            continue
        if str(rf['option']) == '2':
            return '1'
        else:
            return '0'