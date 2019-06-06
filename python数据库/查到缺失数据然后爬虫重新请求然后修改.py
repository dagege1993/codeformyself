import json
import re

import requests
from pymongo import MongoClient
from bson import ObjectId
import time


def get_lost_result(url):
    url = url
    payload = ""
    headers = {
        'User-Agent': "PostmanRuntime/7.11.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "www.tripadvisor.cn",
        'accept-encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }
    response = requests.request("GET", url, data=payload, headers=headers, verify=False)  # proxies=proxies,

    longitude = re.findall('longitude":(\S\d+.\d+|\d+.\d+)', response.text)
    print(longitude)
    return longitude


client = MongoClient(host='172.16.4.110', port=27017)
db_auth = client.admin

db = client['scripture']['tripadvisor_lostdesc']

queryArgs = {"longitude": '未获取到当前经度'}  # 城市名字并且不缺失的统计数据
search_res = db.find(queryArgs)
for search in search_res:
    time.sleep(5)
    url = search.get('hotel_tripadvisor_url')
    _id = search.get('_id')
    try:
        longitude = get_lost_result(url)
        longitude = longitude[0]
        print(_id)
        db.update({'_id': ObjectId(_id)}, {"$set": {'longitude': longitude}})  # 根据ID进行查找和修改
    except Exception as e:
        print(url, )
