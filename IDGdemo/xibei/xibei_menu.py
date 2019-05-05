import json
import pandas as pd
import time
import pymysql
import requests


# city_list = ["上海市", "北京市", "深圳市", "杭州市", "西安市", "苏州市", "广州市", "成都市", "武汉市", "南京市", "天津市", "重庆市", "青岛市", "宁波市", "无锡市",
#              "厦门市", "长沙市", "呼和浩特市", "常州市", "福州市", ]


def get_city_list():
    get_city_sql = """select DISTINCT(city) from XIBEI_WAITE"""
    cursor.execute(get_city_sql)
    results = cursor.fetchall()
    city_list = [result[0] for result in results]
    return city_list


def get_ip():
    try:
        proxy = requests.get('http://192.168.103.23:9898/?qty=1&user=hlz_liulishuo_spider&packid=1')
        proxy_response = json.loads(proxy.text)
        data = proxy_response.get('data')
        if len(data) > 0:  # 如果有代理,就添加代理
            ip_dict = data.pop()
            ip = ip_dict.get('IP')
            proxies = {"http": "http://" + ip, "https": "https://" + ip}
            return proxies
        else:
            proxy = requests.get('http://192.168.103.23:9898/?qty=1&user=hlz_liulishuo_spider&packid=2')
            proxy_response = json.loads(proxy.text)
            data = proxy_response.get('data')
            if len(data) > 0:  # 如果有代理,就添加代理
                ip_dict = data.pop()
                ip = ip_dict.get('IP')
                proxies = {"http": "http://" + ip, "https": "https://" + ip}
                return proxies
    except Exception as e:
        print('当前代理挂掉了')
        pass


# 获取待抓取店铺ID
def deter_shops():
    storeid_list = []
    # 这里做了一下限制
    city_list = get_city_list()
    for city in city_list:
        sql = """select distinct storeId from XIBEI_WAITE where crawlTime = '2019-02-13 19:00:00' and city = '%s' limit 3""" % city
        cursor.execute(sql)
        results = cursor.fetchall()
        for result in results:
            storeid = str(result[0])
            # 生成一个字典关于id和城市
            storeid_city_dict = {}
            storeid_city_dict[storeid] = city
            storeid_list.append(storeid_city_dict)
    return storeid_list


def get_city_level():
    path = r'city_level.xlsx'
    results = pd.read_excel(path)
    city_list = results['城市']
    level_list = results['城市等级']
    city_level_dict = dict(zip(city_list, level_list))
    print(city_level_dict)
    return (city_level_dict)


# 输入店铺ID获取菜单
def get_menu(city_dict, key):
    url = "https://online.xibei.com.cn/api/classes/getFoodList"
    querystring = {"token": "D9FB28AEBC38CD73CB2DDEBF3D9C88D5"}
    storeId = list(city_dict.keys())[0]
    # storeId = '93'
    city = list(city_dict.values())[0]
    city_in = city.split("市")[0]
    city_level = city_level_dict.get(city_in)
    payload = "store_code=" + storeId + "&environment=reserve"
    headers = {
        'Host': "online.xibei.com.cn",
        'Connection': "keep-alive",
        'Content-Length': "32",
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'Origin': "https://online.xibei.com.cn",
        'X-Requested-With': "XMLHttpRequest",
        'User-Agent': "Mozilla/5.0 (Linux; Android 6.0.1; MI 5 Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/51.0.2704.81 Mobile Safari/537.36 MMWEBID/759 MicroMessenger/7.0.3.1400(0x27000334) Process/tools NetType/WIFI Language/zh_CN",
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
        'Referer': "https://online.xibei.com.cn/online/reserve?store_id=4&from=reserve",
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "zh-CN,en-US;q=0.8",
        'Cookie': "remember=09445ab9a779dafc7b642dfa3565848a; PHPSESSID=laj9dv47kpji11dmj57oo5esi0; token=310F20D5630EF54117E79951A1074025",
        'cache-control': "no-cache",
        'Postman-Token': "56b9a6af-7bc0-45f7-b35d-82c9bfbd16cc"
    }

    if key == 1:
        proxies = get_ip()
        response = requests.request("POST", url, data=payload, headers=headers, params=querystring, proxies=proxies)
    if key == 2:
        response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

    # print(response.text)
    if response.status_code == 200:
        response_detail = json.loads(response.text)
        data = response_detail.get('data')
        # 结果返回的数据可能是列表可能是字典
        if isinstance(data, list):
            for result in data:
                # result获取的是一个字典,然后获取他的值
                classes_name = result.get('classes_name')
                food_list = result.get('food_list')
                print(classes_name)
                print(food_list)
                for food in food_list:
                    food_code = food.get('food_code')
                    food_name = food.get('food_name')
                    food_unit = food.get('food_unit')
                    food_price = food.get('food_price')
                    food_member_price = food.get('food_member_price')
                    insert_sql = """insert ignore XIBEI_MENU (storeId,city,food_name,food_code ,food_unit,classes_name,food_price,food_member_price,crawlTime,city_level) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s") """ % (
                        storeId, city, food_name, food_code, food_unit, classes_name, food_price, food_member_price,
                        start_time, city_level)
                    print(insert_sql)
                    cursor.execute(insert_sql)
                    db.commit()
        if isinstance(data, dict):
            data_list = list(data.values())
            for result in data_list:
                # result获取的是一个字典,然后获取他的值
                classes_name = result.get('classes_name')
                food_list = result.get('food_list')
                # print(classes_name)
                # print(food_list)
                for food in food_list:
                    food_code = food.get('food_code')
                    food_name = food.get('food_name')
                    food_unit = food.get('food_unit')
                    food_price = food.get('food_price')
                    food_member_price = food.get('food_member_price')
                    insert_sql = """insert ignore XIBEI_MENU (storeId,city,food_name,food_code ,food_unit,classes_name,food_price,food_member_price,crawlTime,city_level) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s") """ % (
                        storeId, city, food_name, food_code, food_unit, classes_name, food_price, food_member_price,
                        start_time, city_level)
                    # print(insert_sql)
                    cursor.execute(insert_sql)
                    db.commit()


if __name__ == '__main__':
    print('开始工作')
    localtime = time.localtime(time.time())
    start_time = time.strftime("%Y-%m-%d ", localtime)
    start_times = time.strftime("%Y-%m-%d %H:%M", localtime)
    # start_time = '2019-01-20 16:39:00'
    print('开始抓取时间', start_times)
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "xibei")
    cursor = db.cursor()
    # get_menu()
    storeid_list = deter_shops()
    print(storeid_list)
    print(len(storeid_list))
    # for storeId_city in storeid_list:
    #     try:
    #         get_menu(storeId_city, 1)
    #     except Exception as e:
    #         pass
    # 获取城市对应的城市等级
    city_level_dict = get_city_level()
    # 因为不好判断何为缺失,所以干脆不用代理再跑一遍

    for storeId_city in storeid_list:
        try:
            time.sleep(1)
            get_menu(storeId_city, 2)
        except Exception as e:
            pass
