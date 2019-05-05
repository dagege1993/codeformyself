import json
import time
import pymysql
import requests


def get_city():
    url = "https://www.bianlifeng.com/product/free/city/openShop/v1"
    querystring = {"_": "1550483086862"}
    payload = ""
    headers = {
        'cache-control': "no-cache",
        # 'Postman-Token': "997e57e4-0c09-4762-a3c4-72d961b8660e"
    }
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    print(response.text)
    response_text = json.loads(response.text)
    data = response_text.get('data')
    for city_dict in data:
        print(city_dict)
        cityCode = city_dict.get('cityCode')
        cityName = city_dict.get('cityName')
        get_city_shop(cityCode)


def get_city_shop(citycode):
    url = "https://www.bianlifeng.com/product/free/list/city/v1"
    payload = {"cityCode": "100"}
    payload['cityCode'] = citycode
    payload = json.dumps(payload)
    headers = {
        'Host': "www.bianlifeng.com",
        'Connection': "keep-alive",
        'Content-Length': "18",
        'Accept': "*/*",
        'Origin': "https://www.bianlifeng.com",
        'X-Requested-With': "XMLHttpRequest",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        'Content-Type': "application/json;charset=UTF-8",
        'Referer': "https://www.bianlifeng.com/",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
        'cache-control': "no-cache",
        # 'Postman-Token': "4d99f4a2-a3dd-452a-81bd-c4faccc37990"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)
    response_text = json.loads(response.text)
    storage(response_text)


def storage(response_text):
    db = pymysql.connect('192.168.103.31', 'root', 'adminadmin', 'shops')
    cursor = db.cursor()
    data_list = response_text.get('data')
    for data in data_list:
        shopCode = data.get('shopCode')
        name = data.get('name')
        address = data.get('address')
        city = data.get('city')
        district = data.get('district')
        insert_sql = """insert ignore BianLiFeng (id,  city, shop_name,address,crawlTime,district) VALUES ("%s","%s","%s","%s","%s","%s") """ % (
            shopCode, city, name, address, crawl_hour_time, district)
        cursor.execute(insert_sql)
    db.close()


if __name__ == '__main__':
    local_time = time.localtime(time.time())
    crawl_hour_time = time.strftime("%Y-%m-%d ", local_time)
    print('当前抓取日期%s' % crawl_hour_time)
    get_city()
