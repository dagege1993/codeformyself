import json
import os
import re
import sys
import time
import pymysql
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# sys.path 返回的是一个列表！该路径已经添加到系统的环境变量了，当我们要添加自己的搜索目录时，可以通过列表的append()方法；对于模块和自己写的脚本不在同一个目录下，在脚本开头加sys.path.append(‘xxx’)：
from crowdfuding.url_list import public_recent
from python_redis.get_in_redis import get_authorizationV2_in_redis

total_list = ['中老年抗癌互助计划', '中青年抗癌互助计划', '百万终身抗癌互助计划', '综合意外互助计划', '少儿健康互助计划']


# 获取所有公示详情页的数据
def pulic_list():
    url = "https://api.shuidihuzhu.com/api/hz/noticeV2/userListV2"

    payload = {"groupNo": "62409d911d09c1c55fb4f1",
               "thirdType": "2",
               "AuthorizationV2": "67vQPM0zeQHq2kvgrb5-gYwdzmeX2qV9Bqgk2wN3PGs="}
    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'Host': "api.shuidihuzhu.com",
        'Connection': "keep-alive",
        'Content-Length': "105",
        'Accept': "application/json, text/plain, */*",
        'Origin': "https://www.shuidihuzhu.com",
        'User-Agent': "Mozilla/5.0 (Linux; Android 4.4.2; OPPO R11 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36 android rock/1.8.3",
        'api-version': "2",
        'AuthorizationV2': "67vQPM0zeQHq2kvgrb5-gYwdzmeX2qV9Bqgk2wN3PGs=",
        'Content-Type': "application/x-www-form-urlencoded",
        'Referer': "https://www.shuidihuzhu.com/sd/notice/8c4b029f7f26d47fd9f1ba?channel=app_android_yingyongbao_1.8.3",
        'Accept-Encoding': "gzip,deflate",
        'Accept-Language': "zh-CN,en-US;q=0.8",
        'X-Requested-With': "com.shuidihuzhu.rock",
        'cache-control': "no-cache",
    }

    # detail_list = public_total()  # 自定义函数.获取所有公示的url,初次抓取的时候要用
    detail_list = public_recent()  # 自定义函数.获取近第一页公示的url
    # 获取每一期的公示详情
    for detail in detail_list:
        group_no = detail.get('groupNo')
        payload["groupNo"] = group_no
        payload['AuthorizationV2'] = get_authorizationV2_in_redis()
        year = detail.get('year')
        response = requests.request("POST", url, data=payload, headers=headers)
        response_text = json.loads(response.text)
        data = response_text.get('data')
        noticeUserInfoV2VOList = data.get('noticeUserInfoV2VOList')
        # 对公示详情数据做去重,去重规则是根据只要保留五个保险计划的其中一个用户就行
        user_list = list_contains_dictionary_for_set(noticeUserInfoV2VOList)  # 自定义的函数对列表包含字典的value进行去重
        # 然后在对用户详情页发起请求
        for user in user_list:
            id = user.get('id')
            response = user_detail(id)
            period = data.get('subTitle')
            storage(response, period, year)


# 列表包含字典,按照字典的某一个值进行去重
def list_contains_dictionary_for_set(l3):
    l4 = []
    l4.append(l3[0])
    for dict in l3:
        k = 0
        for item in l4:
            if dict['planType'] != item['planType']:
                k = k + 1
            else:
                break
            if k == len(l4):
                l4.append(dict)
    print('去重后的数据', l4)
    return l4


# 对用户详情页发送请求
def user_detail(id):
    url = "https://api.shuidihuzhu.com/api/hz/noticeV2/userDetailV2"
    payload = {
        "AuthorizationV2": "67vQPM0zeQHq2kvgrb5-gYwdzmeX2qV9Bqgk2wN3PGs=",
        "id": 1739,
        "thirdType": 2}
    payload['id'] = id
    payload['AuthorizationV2'] = get_authorizationV2_in_redis()  # 其中一个参数过期时间是七天
    headers = {'cache-control': "no-cache", }
    response = requests.request("POST", url, data=payload, headers=headers)
    return response


# 存储数据
def storage(response, period, year):
    response_text = json.loads(response.text)
    data = response_text.get('data')
    name = data.get('insuranceTitle')  # 计划名称
    join_person = data.get('joinPerson')  # 本期参与人数
    year = int(year.replace('年', ''))  # 年份
    period = period  # 第几期
    months = ''.join(re.findall('(\d+)月', period))
    schedule = ''.join(re.findall('(\d)期', period))
    localtime = time.localtime(time.time())
    str_time = time.strftime("%Y-%m-%d", localtime)
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "water_safe")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # SQL 插入语句
    sql = """INSERT ignore PLANS2 (insuranceTitle,joinPerson,period,years,times,months,schedule)VALUES  ("%s","%d","%s","%s","%s","%d","%d")""" % (
        name, int(join_person), period, year, str_time, int(months), int(schedule))
    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
    # 关闭数据库连接
    db.close()


if __name__ == '__main__':
    pulic_list()
