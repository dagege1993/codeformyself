import json
import pandas as pd
import time
import pymysql
import requests
from starbar_sign import sign_string


def get_ip():
    try:
        proxy = requests.get('http://192.168.103.23:9898/?qty=1&user=hlz_liulishuo_spider&packid=1')
        proxy_response = json.loads(proxy.text)
        data = proxy_response.get('data')
        if len(data) > 0:  # 如果有代理,就添加代理
            ip_dict = data.pop()
            ip = ip_dict.get('IP')
            proxies = {
                "http": "http://" + ip,
                "https": "https://" + ip
            }
            return proxies
        else:
            proxy = requests.get('http://192.168.103.23:9898/?qty=1&user=hlz_liulishuo_spider&packid=2')
            proxy_response = json.loads(proxy.text)
            data = proxy_response.get('data')
            if len(data) > 0:  # 如果有代理,就添加代理
                ip_dict = data.pop()
                ip = ip_dict.get('IP')
                proxies = {
                    "http": "http://" + ip,
                    "https": "https://" + ip
                }
                return proxies
    except Exception as e:
        print('当前代理挂掉了')
        pass


# 传入ID(转换后的的ID),下载菜单页面
def get_menu(APP_shop_id, shop_name, key, id_city):
    url = "https://appdelivery.starbucks.com.cn/assortment/menu/detail"
    unsigned_string = 'appid=859977c6f22b4f9ce98d4b02d031b4a8&lang=zh-cn&store_id=' + APP_shop_id
    # 参数加密
    sign = sign_string(unsigned_string)
    querystring = {"store_id": "25023", "lang": "zh-cn", "appid": "859977c6f22b4f9ce98d4b02d031b4a8",
                   "sign": ''}
    querystring["sign"] = sign
    querystring["store_id"] = APP_shop_id
    payload = ''
    headers = {
        'Host': "appdelivery.starbucks.com.cn",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Authorization': "Bearer cgYh7tam3VW6AJjd8fnnFNuWbwTw26oC.lDdNN9X8G7%2FGZ%2Fvwscl69Aeqd%2BxwL57CLVF4aavf%2FD8",
        'User-Agent': "com.starbucks.cn/2157",
        'x-bs-device-id': "kpOv8udkAryBA3OfoBOe_XAn46tmIT7EZXIsIFi0KzffmyKGX-YpIZ5b2ULurX_HF0Ra3Ki8gVT_UiXQMcLX_WwAl0e5ZQ6GFAS7je-TGaA3QLNCu7aEgAwY9jfEbsQG9NmcsK-HX6onu_gpcIfEn6nrAjXWY14F",
        'cache-control': "no-cache",
    }
    if key == 1:
        proxies = get_ip()
        response = requests.request("GET", url, data=payload, headers=headers, params=querystring, proxies=proxies,
                                    timeout=6)
    if key == 2:
        response = requests.request("GET", url, data=payload, headers=headers, params=querystring, timeout=6)
    # response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    print(response.text)
    response_text = json.loads(response.text)
    code = response_text.get('code')
    if code == 100:
        storage(response_text, shop_name, id_city)


def PC_shop_id(shop_name):
    db = pymysql.connect('192.168.103.31', 'root', 'adminadmin', 'shops')
    cursor = db.cursor()
    sql = """select DISTINCT id from Starbucks WHERE shop_name ='%s'; """ % (shop_name)
    cursor.execute(sql)
    result = cursor.fetchone()
    if result:
        result = result[0]
    return result


def storage(response_text, shop_name, id_city):
    # print(response_text)
    db = pymysql.connect('192.168.103.31', 'root', 'adminadmin', 'shops')
    cursor = db.cursor()
    data_dict = response_text.get('data')
    categories = data_dict.get('categories')
    city = id_city[-1]
    # 获取本地文件的城市等级列表
    city_level_dict = get_city_level()
    city_level = city_level_dict.get(city)

    for category in categories:
        subCategories = category.get('subCategories')
        for subCategory in subCategories:
            subCategory_name = subCategory.get('name')
            products = subCategory.get('products')
            for product in products:
                defaultPrice = product.get('defaultPrice')
                defaultPrice = str(int(defaultPrice) / 100)
                name = product.get('name')
                id = product.get('id')
                shop_id = PC_shop_id(shop_name)
                print(subCategory_name, name, defaultPrice, id, shop_id)
                insert_sql = """insert ignore Starbucks_menu (food_id,subCategory_name,shop_name,name,defaultPrice,crawlTime,shop_id,city,city_level) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s") """ % (
                    id, subCategory_name, shop_name, name, defaultPrice, crawlTime, shop_id, city, city_level)
                cursor.execute(insert_sql)


# 传入库里ID(库里ID是来自PC端),和APP端的ID是对不上,所以需要转换,返回的是城市列表
def transformation(id_city):
    latitude = id_city[1]
    longitude = id_city[2]
    url = "https://appdelivery.starbucks.com.cn/assortment/store/list"
    payload = {"in_business": 1, "latitude": "39.907098", "longitude": "116.429323"}
    payload["latitude"] = latitude
    payload["longitude"] = longitude
    payload = json.dumps(payload)
    to_encode = "appid=859977c6f22b4f9ce98d4b02d031b4a8&lang=zh_CN" + payload
    sign = sign_string(to_encode)
    querystring = {"lang": "zh_CN", "appid": "859977c6f22b4f9ce98d4b02d031b4a8", "sign": sign}
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer erJCQ3JZMbAAcTinU5JMjcRHdl68e5Om.4oDCinNVwzRNp2x6VF%2FIOd0Qydp9sQk4MWHZQjc5Yxo",
        'cache-control': "no-cache"
    }
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    print(response.text)
    if response.status_code == 200:
        response_text = json.loads(response.text)
        return response_text
    else:
        print(response.text)
        pass


# 传入城市,获取城市级别
def get_city_level():
    path = r'city_level.xlsx'
    results = pd.read_excel(path)
    city_list = results['城市']
    level_list = results['城市等级']
    city_level_dict = dict(zip(city_list, level_list))
    print(city_level_dict)
    return (city_level_dict)


# 去数据库拿到去重后的带有经纬度的PC端店铺ID
def start_scrawl():
    db = pymysql.connect('192.168.103.31', 'root', 'adminadmin', 'shops')
    cursor = db.cursor()
    inquery_sql = """select id,latitude,longitude,city from Starbucks WHERE latitude !='' and longitude !='' and city_level !='中国大陆外' GROUP BY id;"""
    cursor.execute(inquery_sql)
    results = cursor.fetchall()
    df_data = pd.DataFrame(list(results))  # 转换成DataFrame格式
    print(df_data)
    # dataframe便利行,loc做数据切分用的
    id_city_list = []
    for indexs in df_data.index:
        id_city = df_data.loc[indexs].values[0:]
        id_city_list.append(id_city)
    return id_city_list


if __name__ == '__main__':
    local_time = time.localtime(time.time())
    crawlTime = time.strftime("%Y-%m-%d ", local_time)
    print('当前抓取日期%s' % crawlTime)
    # get_menu()

    id_city_list = start_scrawl()
    for id_city in id_city_list:
        """id_city =['1017245' '18.308424' '109.411488' '三亚'] PC端店铺ID,经纬度,城市 """
        print(id_city)
        # id_city = ['1023894', '29.332596', '104.771515', '自贡']
        response_text = transformation(id_city)
        if response_text:
            code = response_text.get('code')
            # 如果解析成功
            if code == 100:
                data_list = response_text.get('data')
                print(data_list)
                # data_list = data_list[:3] 改为全部抓取,
                for data in data_list:
                    print(data)
                    APP_shop_id = data.get('id')
                    shop_name = data.get('name')
                    key = 1  # key=1使用代理,=2不适用代理
                    try:
                        get_menu(APP_shop_id, shop_name, key, id_city)
                    except Exception as e:
                        print(e)
