import json
import time
import pandas as pd
import pymysql
import requests

requests.packages.urllib3.disable_warnings()  # 忽略警告


# 获取城市等级
def get_city_level():
    path = r'city_level.xlsx'
    results = pd.read_excel(path)
    city_list = results['城市']
    level_list = results['城市等级']
    city_level_dict = dict(zip(city_list, level_list))
    print(city_level_dict)
    return (city_level_dict)


# 获取全国门店列表
def start_crawl():
    # 获取本地文件的城市等级列表
    city_level_dict = get_city_level()
    url = "https://superapp.kiwa-tech.com/app/getNearbyStore"
    payload = "{\"_HAIDILAO_APP_TOKEN\":\"\",\"customerId\":\"\",\"latitude\":\"39.907857\",\"longitude\":\"116.42946\",\"pageSize\":10,\"pageNum\":1,\"country\":\"CN\"}"
    headers = {
        'Content-Type': "application/json; charset=UTF-8",
        'Host': "superapp.kiwa-tech.com",
        # 'Connection': "Keep-Alive",
        'Connection': "close",
        'Accept-Encoding': "gzip",
        'cache-control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers, verify=False, timeout=15)
    response_test = json.loads(response.text)
    shop_list = response_test.get('data')
    localtime = time.localtime(time.time())
    crawl_time = time.strftime("%Y-%m-%d", localtime)
    print('抓取时间', crawl_time)
    print('店铺长度', len(shop_list))
    for shop in shop_list:
        storeId = shop.get('storeId')
        storeName = shop.get('storeName')
        cityId = shop.get('city')
        address = shop.get('address')
        cursor = db.cursor()
        # 拿到城市id
        inquery_sql = """select city from CITY_ID where  cityId = '%s'""" % cityId
        cursor.execute(inquery_sql)
        city_names = cursor.fetchone()
        print('获取城市名字结果', city_names)
        print('获取城市查询语句', inquery_sql)
        city_name = city_names[0]
        city = city_name.split('市')[0]
        city_level = city_level_dict.get(city)
        web_queue = str(shop.get('webQueue'))
        if city_level:
            city_level = city_level
        else:
            city_level = '中国大陆外'
        # 插入到店铺详情页
        insert_sql = """INSERT ignore SHOP_DETAIL(storeId,
                         cityId, storeName,city, address,crawlTime,city_level,web_queue)
                       VALUES  ("%s","%s","%s","%s","%s","%s","%s","%s")""" % (
            storeId, cityId, storeName, city_name, address, crawl_time, city_level, web_queue)
        cursor.execute(insert_sql)
        # 提交到数据库执行
        db.commit()


if __name__ == '__main__':
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "hotpot")
    cursor = db.cursor()
    print('开始抓取')
    start_crawl()
    # 抓取完毕关闭数据库连接
    db.close()
    # get_city_level()
