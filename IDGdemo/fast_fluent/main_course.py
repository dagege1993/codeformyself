# encoding=utf8
import json
import time

from scrapy.cmdline import execute

import sys
import os

from fast_fluent.starturl_list import get_token
from mysql_couse import get_course_id

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

SECOND_DAY = 24 * 60 * 60


def delta_seconds():
    from datetime import datetime
    cur_time = datetime.now()
    des_time = cur_time.replace(hour=0, minute=1, second=0, microsecond=0)
    # 这里添加时间 replace()= Return a new datetime with new values for the specified fields.返回一个替换指定日期字段的新date对象
    delta = des_time - cur_time
    skip_seconds = delta.total_seconds() % SECOND_DAY  # total_seconds()是获取两个时间之间的总差
    print("Must sleep %d seconds" % skip_seconds)
    return skip_seconds


def get_fluent_id_count():
    import requests
    url = "https://apineo.llsapp.com/api/v1/curriculums/filtered"
    querystring = {"type": "1", "pageSize": "20", "level": "", "sort": "diamond_consume_desc", "page": "1",
                   "appVer": "6", "deviceId": "354730011088642", "sDeviceId": "354730010301566", "appId": "lls",
                   "token": "4cc82410cb810136b78c0a5864605084"}
    querystring['token'] = get_token()
    headers = {
        'Accept-Language': "zh-cn",
        'User-Agent': "Lingome/5.0 (SM-G955N;Android 4.4.2;)",
        'Host': "apineo.llsapp.com",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'cache-control': "no-cache",
        'Postman-Token': "b4d8e656-09c2-4c88-a280-d0405f2f78d2"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)
    response_text = json.loads(response.text)
    return response_text.get('total')


if __name__ == '__main__':
    localtime = time.localtime(time.time())
    strtime = time.strftime("%Y-%m-%d %H:%M", localtime)
    print('当前抓取时间是', strtime)
    execute(["scrapy", "crawl", "Course", ])
