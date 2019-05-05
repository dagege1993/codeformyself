import json
import pandas as pd
import re
import time
import pymysql
import requests


def get_city():
    url = "https://store.xibei.com.cn/index/confimcity"
    payload = ""
    headers = {
        'Host': "store.xibei.com.cn",
        'Connection': "keep-alive",
        'User-Agent': "Mozilla/5.0 (Linux; Android 6.0.1; MI 5 Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044408 Mobile Safari/537.36 MMWEBID/759 MicroMessenger/7.0.3.1400(0x27000334) Process/tools NetType/WIFI Language/zh_CN",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,image/wxpic,image/sharpp,image/apng,image/tpg,*/*;q=0.8",
        'Referer': "https://store.xibei.com.cn/",
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "zh-CN,en-US;q=0.8",
        'Cookie': "store=6l0celco58fuhlkccdgg1risp3; remember=dac06b7ca0170a4e5415cd216be72125",
        'cache-control': "no-cache",
    }
    response = requests.request("GET", url, data=payload, headers=headers)
    # print(response.text)
    city_list = re.findall("""controller.init\((.*)\);""", response.text)
    tt = city_list[0]
    tt = tt.replace("'", "")
    city_list = eval(tt)
    return city_list


def get_city_level():
    path = r'city_level.xlsx'
    results = pd.read_excel(path)
    city_list = results['城市']
    level_list = results['城市等级']
    city_level_dict = dict(zip(city_list, level_list))
    print(city_level_dict)
    return (city_level_dict)


def get_city_shops(city_dict):
    url = "https://store.xibei.com.cn/index/getStoreList"
    querystring = {"brand": "1", "city_id": "310100"}
    city_id = city_dict.get('id')
    city = city_dict.get('name')
    city_in = city.split("市")[0]
    city_level = city_level_dict.get(city_in)
    querystring["city_id"] = city_id
    # querystring["city_id"] = "610100"
    payload = ""
    headers = {
        'Host': "store.xibei.com.cn",
        'Connection': "keep-alive",
        'Accept': "*/*",
        'X-Requested-With': "XMLHttpRequest",
        'User-Agent': "Mozilla/5.0 (Linux; Android 6.0.1; MI 5 Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044408 Mobile Safari/537.36 MMWEBID/759 MicroMessenger/7.0.3.1400(0x27000334) Process/tools NetType/WIFI Language/zh_CN",
        'Referer': "https://store.xibei.com.cn/",
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "zh-CN,en-US;q=0.8",
        'Cookie': "store=6l0celco58fuhlkccdgg1risp3; remember=dac06b7ca0170a4e5415cd216be72125",
        'cache-control': "no-cache",
    }
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    # print(response.text)
    if response.status_code == 200:
        response_detail = json.loads(response.text)
        data = response_detail.get('data')
        store_list = data.get('store_list')
        for store in store_list:
            storeId = store.get('store_id')
            storeName = store.get('store_name')
            store_queue = store.get('store_queue')
            queues = store_queue.get('queues')
            # 网络排号开启
            if queues:
                open_or_not = 1
                for queue in queues:
                    wait = queue.get('wait')
                    qname = queue.get('qname')
                    waittime = queue.get('waittime')
                    insert_sql = """insert ignore XIBEI_WAITE (storeId,storeName,wait,qname,waittime,city,crawlTime,open_or_not,city_level) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s") """ % (
                        storeId, storeName, wait, qname, waittime, city, start_time, open_or_not, city_level)
                    cursor.execute(insert_sql)
                    db.commit()
            # 未开启网络排号
            else:
                open_or_not = 0
                insert_sql = """insert ignore XIBEI_WAITE (storeId,storeName,city,crawlTime,open_or_not,city_level) VALUES ("%s","%s","%s","%s","%s","%s") """ % (
                    storeId, storeName, city, start_time, open_or_not, city_level)
                cursor.execute(insert_sql)
                db.commit()


if __name__ == '__main__':
    print('开始工作')
    localtime = time.localtime(time.time())
    start_time = time.strftime("%Y-%m-%d %H", localtime)
    print(start_time)
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "xibei")
    cursor = db.cursor()
    city_list = get_city()
    # 获取城市对应的城市等级
    city_level_dict = get_city_level()
    for city_dict in city_list:
        time.sleep(1)
        print(city_dict)
        get_city_shops(city_dict)
