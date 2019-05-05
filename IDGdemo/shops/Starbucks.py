# 获取代理
import json
import time
import pandas as pd
import pymysql
import requests

lost_city_list = ['Jinhua', 'Guangzhou', 'Hangzhou', 'Lishui', 'Nanjing', 'Ningbo', 'SHANGHAI', 'Wuxi', ]
lost_city_dict = {
    'Jinhua': '金华',
    'Guangzhou': '广州',
    'Hangzhou': '杭州',
    'Lishui': '丽水',
    'Nanjing': '南京',
    'Ningbo': '宁波',
    'SHANGHAI': '上海',
    'Wuxi': '无锡',
}


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


def get_city_level():
    path = r'city_level.xlsx'
    results = pd.read_excel(path)
    city_list = results['城市']
    level_list = results['城市等级']
    city_level_dict = dict(zip(city_list, level_list))
    print(city_level_dict)
    return (city_level_dict)


def start_scrawl():
    url = "https://www.starbucks.com.cn/api/stores"
    querystring = {"locale": "CN"}
    payload = ""
    headers = {
        'cache-control': "no-cache",
    }
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    print(response.text)
    response_text = json.loads(response.text)
    storage(response_text)


def storage(response_text):
    # 获取本地文件的城市等级列表
    city_level_dict = get_city_level()
    data_list = response_text.get('data')
    db = pymysql.connect('192.168.103.31', 'root', 'adminadmin', 'shops')
    cursor = db.cursor()
    for data in data_list:
        id = data.get('id')
        shop_name = data.get('name')
        address_dict = data.get('address')
        coordinates = data.get('coordinates')
        # 后续加的一个经纬度
        latitude = coordinates.get('latitude')
        longitude = coordinates.get('longitude')

        city = address_dict.get('city')
        city = city.split('市')[0]
        # 因为有些城市可能是英文,所以转译了一下
        if city in lost_city_list:
            city = lost_city_dict.get(city)
        city_level = city_level_dict.get(city)
        if city == '襄樊':
            city_level = '三线城市'
        if city == '西昌':
            city_level = '四/五线城市'
        if city_level:
            city_level = city_level
        else:
            city_level = '中国大陆外'

        address_values = address_dict.values()
        address_values = list(filter(None, address_values))
        address_values = [address.strip() for address in address_values]  # 把空值,None,"去掉
        address_values = [address.replace('"', '') for address in address_values]  #
        address = ''.join(address_values)
        # print(address)
        # local_time = time.localtime(time.time())
        # crawl_hour_time = time.strftime("%Y-%m-%d ", local_time)
        insert_sql = """insert ignore Starbucks (id,  city, shop_name,address,crawlTime,city_level,latitude,longitude) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s") """ % (
            id, city, shop_name, address, crawl_hour_time, city_level, latitude, longitude)
        cursor.execute(insert_sql)
    db.close()


if __name__ == '__main__':
    local_time = time.localtime(time.time())
    crawl_hour_time = time.strftime("%Y-%m-%d ", local_time)
    print('当前抓取日期%s' % crawl_hour_time)
    start_scrawl()
    # get_city_level()
