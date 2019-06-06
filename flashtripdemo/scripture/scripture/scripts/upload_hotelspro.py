# coding: utf8

import json
import logging
import random
import re
import time

import oss2
#
import requests
from lxml import etree
from pymongo import MongoClient
from yarl import URL

from scripture.xpath import bookings as bk
from scripture.xpath import tripadvisor as ta
from tasks.upload_image import _upload_image

comm_at_re = re.compile(r"([0-9 \-]+)")

errors = {}
exists = {}

logger = logging.getLogger(__name__)


class TxOss(object):
    def __init__(self, ak, sk, bucket):
        endpoint = 'http://oss-cn-beijing-internal.aliyuncs.com'
        auth = oss2.Auth('LTAIwHXVgRkPRxcw', 'PCm6kdpeyjAG2gJz4B4C2js3TIifrc')
        self.bucket = oss2.Bucket(auth, endpoint, 'weegotr-statics')

    def head_object(self, path):
        return self.bucket.head_object(path)

    def put_object(self, path, content):
        return self.bucket.put_object(path, content)

    def object_exists(self, path):
        return self.bucket.object_exists(path)

    def get_object(self, key):
        return self.bucket.get_object(key)


class TxGallery(dict):
    domains = [
        'img3.weegotr.com',
        'img4.weegotr.com'
    ]

    def __init__(self):
        endpoint = 'http://oss-cn-beijing.aliyuncs.com'
        self.bucket = TxOss(
            'LTAIwHXVgRkPRxcw',
            'PCm6kdpeyjAG2gJz4B4C2js3TIifrc',
            endpoint
        )

    def get_image_url(self, url, to_try):
        state = self.handle(url, to_try)
        if state:
            host = random.choice(self.domains)
            url = str(URL(url).with_scheme('http').with_host(host))
            return url
        else:
            return url

    def _image_is_exists(self, uri):
        if uri.startswith('/'):
            uri = uri[1:]
        state = self.bucket.object_exists(uri)
        return state

    def handle(self, url, to_try=None, ori=None):
        if to_try is None:
            to_try = ['z', 'y', 'b', 'n', 'l', 't', 'd', 's', 'e', 'g']
        try:
            fr = URL(url).path[1:]
            if ori:
                _ori = URL(ori)
                if _ori.path.startswith('/'):
                    to = _ori.path[1:]
                else:
                    to = _ori.path
            else:
                to = fr
            state = self._image_is_exists(to)
            if state:
                return True
            logger.info(f'upload pic : {url} to {to}')
            _upload_image.delay(url, to)
            return True
        except Exception as e:
            print(e)
            return False

    def get_object(self, key):
        return self.bucket.get_object(key)

    def replace_webp_to_jpeg(self, url, f):
        return self.bucket.put_object(url, f)


tx = TxGallery()


def telephone(string):
    statement = []
    expr_re = re.compile(r"[a-z]+\+?='[0-9 \-]+'|document.write\(([a-z\+]+)\)")
    for line in string.split("\n"):
        match = expr_re.match(line)
        if not match:
            continue
        if match[1]:
            statement.append("tel = " + match[1])
            # statement.append(match[1])
        else:
            statement.append(match[0])
    expr = "\n".join(statement)
    if expr:
        g = {}
        exec(expr, g)
        try:
            return g["tel"].strip()
        except (KeyError, TypeError):
            print("Bad telephone: %s", expr)
    else:
        return ""


def safe_xpath(tree, xp, name):
    try:
        fnd = tree.xpath("." + xp)
        return fnd[0]
    except IndexError:
        html = etree.tostring(tree, encoding="unicode")


def published(tree):
    comment_at = safe_xpath(tree, "." + ta.comment_at, "published_at")
    if comment_at is not None:
        _at = comment_at.xpath("./@title")
        if _at:
            return _at[0]
        _at = comment_at.xpath("./text()")[0]
        try:
            match = comm_at_re.search(_at)
            return match[1]
        except (IndexError, TypeError):
            print("")
    return ""


HCOM_ID_RE = re.compile(r"/ho([0-9]+)")

db = MongoClient("mongodb://172.16.4.110:27017/scripture").get_database()
hub = MongoClient("mongodb://172.16.4.110:27017/hub").get_database()

session = requests.Session()

cookie = {'cookie': 'this.sid=s%3At-zhuMN_RbW3-Irhy02rQEl9BBlVPnmk.ureaEka%2Fx2EihnSii%2B60QACXlRRDfciTHF3ILSFfgXI; XSRF-TOKEN=RZ5QUuWNRH41c3d5e3e72550af3e8dd244c43d138061d51d89'}


class HotelsproBaseData:
    allXpath = [x for x in dir(bk) if x[0] != "_"]

    def __init__(self, hid, hname, branch, ta_url, bk_url):
        ta_url = ta_url.replace("tripadvisor.com/", "tripadvisor.cn/")
        self.hid = hid
        self.ori_ta_url = URL(ta_url)
        self.ta_url = f"{self.ori_ta_url.scheme}://{self.ori_ta_url.host}{self.ori_ta_url.path}"
        self.branch = branch
        self.ori_booking_url = URL(bk_url)
        self.bk_url = f"{self.ori_booking_url.scheme}://{self.ori_booking_url.host}{self.ori_booking_url.path}"
        self._doc = {
            "capture_id": hid,
            "hotel_id": hid,
            "quote_ids": [
                {"hotel_id": hid, "quoter": "59b0b048a389295de92f4815"}
            ],
            "name_en": hname,
            "website": "",
            "telephone": "",
            "comments_url": ta_url,
            "gallery": [],
        }
        self.ta_headers = {
            "Host": "www.tripadvisor.cn",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        }
        self.bk_headers = {
            "Host": "www.booking.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        }
        self.host = URL("http://172.16.4.110:8289/").with_path("api/internal")
        # self.host = URL("https://api.weegotr.com/").with_path("api/internal")

    def ta(self):
        if self.ta_url == '://None':
            return
        req = requests.get(self.ta_url, headers=self.ta_headers)
        try:
            req = req.content.decode("utf-8")

            parser = etree.HTML(req)
            self._doc["rating"] = parser.xpath('*//span[@class="overallRating"]')[
                0
            ].xpath("string(.)")
        except:
            print(req)
            print(f"error url : {self.ta_url}")
            return

    def bk(self):
        print(f"bk_url : {self.bk_url}")
        if self.bk_url == '://None':
            return
        req = requests.get(self.bk_url)
        req = req.content.decode("utf-8")
        response = etree.HTML(req)
        pic = []
        for e in self.allXpath:
            Xpath = eval("bk." + e)
            fielName, lable = "_".join(e.split("_")[:-1]), e.split("_")[-1]
            tempResult = ""
            if lable == "non":
                if response.xpath(Xpath):
                    tempResult = response.xpath(Xpath)[0].strip()
            elif lable == "ren":
                if re.findall(Xpath, req):
                    tempResult = re.findall(Xpath, req)[0].strip()
            elif lable == "rea":
                if re.findall(Xpath, req):
                    for each in re.findall(Xpath, req):
                        tempResult += each.strip()
            elif lable == "sub":
                if response.xpath(Xpath):
                    tempResult = re.sub(
                        "\\n+",
                        "\\n",
                        response.xpath(Xpath)[0].xpath("string(.)"),
                    ).strip()
            elif lable == "sua":
                selects, subSelcets, y = (
                    Xpath.split("weego")[0],
                    Xpath.split("weego")[1],
                    Xpath.split("weego")[2:],
                )
                for each in response.xpath(selects):
                    temp = each.xpath(subSelcets)
                    if isinstance(temp, list):
                        tempResult += temp[0]
                    elif isinstance(temp, str):
                        tempResult += temp
                tempResult = re.sub("\\n+", "\\n", tempResult).strip()
            elif lable == "pic":
                selects, subSelcets, y = (
                    Xpath.split("weego")[0],
                    Xpath.split("weego")[1],
                    Xpath.split("weego")[2:],
                )
                for each in response.xpath(selects):
                    temp = each.xpath(subSelcets)
                    pic.append(temp[0])
                tempResult = pic
            elif lable == "pir":
                for each in re.findall(Xpath, req):
                    pic.append(each)
                tempResult = pic
            elif lable == "xpl":
                selects, subSelcets, y = (
                    Xpath.split("weego")[0],
                    Xpath.split("weego")[1],
                    Xpath.split("weego")[2:],
                )
                tl = []
                for each in response.xpath(selects):
                    temp = re.sub(
                        "\\n+", " - ", each.xpath(subSelcets).strip()
                    )
                    tl.append(temp)
                self._doc[fielName.lower()] = tl
            if lable != "xpl":
                if self._doc.get(fielName.lower()):
                    if self._doc.get(fielName.lower())[0] == "":
                        self._doc[fielName.lower()] = tempResult
                else:
                    self._doc[fielName.lower()] = tempResult

    def upload_to_sanbox(self):
        self.bk()
        # self.ta()
        # self.fix_data()
        # self.website(self._doc['address_en'])
        deling = []
        for k,v in self._doc.items():
            if not v:
                deling.append(k)
        for e in deling:
            del self._doc[e]
        print(f"{'*'*30}\n")
        for k, v in self._doc.items():
            print(f"{k} : {v}\n")
        print(f"{'*'*30}\n")
        resp = db["stratics.hotelspro.temp_save"].update_one(
            {"hotel_id": self.hid},
            {"$set": self._doc},
            upsert=True
        )
        print(f"resp : {resp}")
        # print(f'host : {host}')

    def from_db(self, id, exists_data):
        # exist = hub['poi_items'].find_one({'$or': [{"quote_ids.hotel_id": e}, {'name_en': {'$regex': self._doc['name_en'], '$options': 'i'}}]})
        # if exist:
        #     exists[id] = str(exist['_id'])
        #     json.dump(exists, open('exists.json', 'w'))
        #     return
        payload = {}
        res = db["stratics.hotelspro.temp_save"].find_one({"hotel_id": id})
        resp = None
        if not (res.get('landmarks') or res.get('facilities') or res.get('checkin_time') or res.get('checkout_time')):
            return
        res.pop("_id")
        payload["capture_id"] = id
        payload['policy'] = []
        payload['attractions'] = []
        payload['facilities'] = []
        host = self.host / "hotels"
        # if 'address_en' in res and not res.get('website'):
        #     addr = res.pop('address_en')
            # self.website(addr)
            # res['website'] = self._doc['website']
        # if res.get('traffic_info'):
        #     ori_traffic_info = res['traffic_info']
        #     traffic_info = [f"{s.strip()}km" for s in ori_traffic_info.split('km') if s != '']
        #     res['traffic_info'] = traffic_info

        attractions = None
        facilities = None
        up_policy = True


        polices = {}
        if exists_data.get('policy'):
            for _policy in exists_data['policy']:
                polices[_policy['type']] = _policy


        if exists_data.get('attractions'):
            payload['attractions'] = exists_data['attractions']
            attractions = True
        elif res.get('landmarks'):
            payload['attractions'] = [{'name': n_d.split(' - ')[0], 'distance': n_d.split(' - ')[1]} for n_d in res['landmarks']]

        if exists_data.get('facilities'):
            payload['facilities'] = exists_data['facilities']
            facilities = True
        elif res.get('facilities'):
            payload['facilities'] = [{'facility': name} for name in set(res['facilities'][0].split(' - 使用的语言')[0].split(' - ')) if name not in ['（额外付费）', '宠物', '不允许携带宠物入住。', '住宿外', '活动设施', '户外', '免费！']]

        if '入住政策' not in polices and res.get('checkin_time') and res.get('checkout_time'):
            payload['policy'].append({'type': '入住政策',
                                      'content': f"入住时间: {res['checkin_time']} \n退房时间: {res['checkout_time']}"})
            up_policy = False

        if res.get('children_policy') and '儿童政策' not in polices:
            payload['policy'].append({'type': '儿童政策',
                                      'content': res['children_policy']})
            up_policy = False

        if res.get('pet_policy') and '宠物政策' not in polices:
            payload['policy'].append({'type': '宠物政策',
                                      'content': res['pet_policy']})
            up_policy = False

        if all([attractions, facilities, up_policy]):
            print(f'{id} all msg already exists!')
            return

        for _type, _polices in polices.items():
            payload['policy'].append(_polices)

        filted = ['landmarks', 'pet_policy', 'children_policy', 'checkin_time', 'checkout_time', 'cancellation_policy']

        for k,v in res.items():
            if k in filted:
                continue
            if k not in payload:
                if isinstance(v, str):
                    payload[k] = ''
                elif isinstance(v, list):
                    payload[k] = []
                elif isinstance(v, dict):
                    payload[k] = {}
        payload['traffic_info'] = []

        # res = self.update_filter(res)

        for i in range(3):
            try:
                resp = requests.put(
                    f'{host}/{id}', json=payload, headers={"accept-version": "6.0.0"}
                )
                if resp:
                    print(f"payload : {payload}")
                    break
            except Exception as exc:
                print(exc)
                time.sleep(3)
        if resp and resp.json()['status'] == 500:
            errors[id] = res
            json.dump(errors, open('error_req.json', 'w'))
        print(f"resp : {resp.json()}")

    def fix_data(self):
        statics_data = db["statics.hotels.hotelspro"].find_one(
            {"code": self.hid}
        )
        if not statics_data:
            print(f"hid : {self.hid} not in db!")
            return
        if not self._doc.get('name'):
            return
        name_cn = re.findall('（(.*?)）', self._doc.get('name', ""))

        if name_cn:
            self._doc['name'] = name_cn[0]
        self._doc['telephone'] = statics_data['phone']
        self._doc['address_en'] = statics_data['address']
        self._doc['introduction'] = self._doc['introduction'].replace("位置超赞 - 查看地图","")
        if 'pictures_1280' in self._doc:
            self._doc['gallery'].extend([
                {
                    'image_url': tx.get_image_url(url,None)
                } for url in self._doc['pictures_1280'] if url.startswith("http")
            ]
            )
            self._doc.pop('pictures_1280')
        if 'highlights' in self._doc and 'gallery' in self._doc:
            highlights = []
            ori_hi = self._doc['highlights']
            for i in range(min(len(self._doc['highlights']), len(self._doc['gallery']))):
                highlights.append(
                    {
                        'image_url': self._doc['gallery'][i]['image_url'],
                        'title': ori_hi[i],
                        'description': ori_hi[i]
                    }
                )
            self._doc['highlights'] = highlights

    def update_filter(self, res):
        for k,v in res.items():
            if k == 'highlights':
                n_hl = []
                for _ in range(min(8, int(len(res.get('gallery', []))/2))):
                    n_hl.append(
                        {
                            'image_url': res['gallery'].pop(-1)['image_url'],
                            'description': "",
                            "title": "",
                        }
                    )
                res['highlights'] = n_hl
                continue
        return res

    def upload_room(self, hid, online_data):
        if online_data['hotel_rooms']:
            print(f"{hid} already exists!")
            return
        host = f'{self.host}/hotels/hotelrooms/{hid}'
        print(f'rooms_url : {host}')
        res = db["stratics.hotelspro.temp_save"].find_one({"hotel_id": hid}, {'rooms':'1'})
        if not res.get('rooms'):
            print(f'rooms is empty! {hid}')
            return
        _payload = res['rooms']
        for room in _payload:
            room['room_desc'] = room['room_desc'].replace('\n更多', '').replace('\n平方米', '平方米')
            if isinstance(room['room_type'], list):
                room['room_type'] = room['room_type'][0]
            if isinstance(room['room_size'], list):
                if room['room_size']:
                    room['room_size'] = room['room_size'][0]
                else:
                    room['room_size'] = ""
            for pic in room['gallery']:
                pic['image_url'] = tx.get_image_url(pic['image_url'], None)
        db["stratics.hotelspro.temp_save"].update_one({"hotel_id": hid},
                                                    {'$set': {'rooms': _payload}})
        for _ in _payload:
            _['capture_id'] = hid
        payload = {'rooms': _payload, 'capture_id': hid}
        print(f'rooms_update_payload : {payload}')
        resp = requests.post(host, json=payload, headers={"accept-version": "6.0.0"})
        if resp:
            print(resp.json())
            return
        else:
            print(f'uplo')
