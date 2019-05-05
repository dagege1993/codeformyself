import json
import random

import pymysql
import redis
import requests
import math
import time


# # from fast_fluent.starturl_list import get_token
# from fast_fluent.starturl_list import get_token
# 从redis 获取一个随机的token,这个token是设置了7天的过期时间
def get_token():
    conn = redis.StrictRedis(host='192.168.103.31')
    token_len = conn.llen('token')
    result = conn.lindex("token", random.randint(0, token_len - 1))
    result = str(result, encoding="utf8")
    return result


def get_provider():
    url = "http://apineo.llsapp.com/api/v1/podcasts"
    querystring = {"page": "1", "appId": "lls", "deviceId": "354730010301566", "sDeviceId": "354730010301566",
                   "appVer": "4", "token": "0465e280c892013659dc0a5864630fa3"}
    payload = ""
    headers = {"cache-control": "no-cache", }
    querystring['token'] = get_token()  # 从 redis随机获取一个token
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    response.encoding = "utf-8"  # 指定编码格式,防止乱码
    response_text = json.loads(response.text)
    get_info(response_text)  # 入库
    total = response_text.get("total")
    if isinstance(total, int) is True:
        total_int = int(total)
        total_page = math.ceil(total_int / 20)  # 向上取整
        total_page += 1
        for i in range(2, int(total_page)):
            time.sleep(1)
            querystring["page"] = str(i)
            print("当前请求的是第%s页", i)
            response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
            if "操作过于频繁，请稍后再试" in response.text:
                response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
            else:
                response.encoding = "utf-8"  # 指定编码格式,防止乱码
                response_text = json.loads(response.text)
                get_info(response_text)  # 入库


def get_info(response_text):
    podcasts = response_text.get("podcasts")
    localTime = time.localtime(time.time())
    strTime = time.strftime("%Y-%m-%d", localTime)
    for podcast in podcasts:
        id = podcast.get("id")
        title = podcast.get("title")
        body = podcast.get("body")
        if "🎵" in body:
            body = body.replace("🎵", "")
        if '\"' in body:
            body = body.replace('\"', "")
            print('替换后的body', body)
        subscribesCount = podcast.get("subscribesCount")  # 订阅数
        episodesCount = podcast.get("episodesCount")  # 节目数
        print("当前入库的数据为:", id, title, body, subscribesCount, episodesCount)
        # 打开数据库连接
        db = pymysql.connect("192.168.103.31", "root", "adminadmin", "fluent")
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        # SQL 插入语句
        sql = """INSERT ignore PROVIDER(ID,
                 TITLE, BODY, subscribesCount, episodesCount,times)
               VALUES  ("%s","%s","%s","%d","%d","%s")""" % (id, title, body, subscribesCount, episodesCount, strTime)
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        # 关闭数据库连接
        db.close()


SECOND_DAY = 24 * 60 * 60


def delta_seconds():
    from datetime import datetime
    cur_time = datetime.now()
    des_time = cur_time.replace(hour=0, minute=0, second=0, microsecond=0)
    delta = des_time - cur_time
    skip_seconds = delta.total_seconds() % SECOND_DAY  # total_seconds()是获取两个时间之间的总差
    print("Must sleep %d seconds" % skip_seconds)
    return skip_seconds


# while True:
#     s = delta_seconds()
#     time.sleep(s)
#     print("work it!")  # 这里可以替换成作业
if __name__ == '__main__':
    get_provider()
