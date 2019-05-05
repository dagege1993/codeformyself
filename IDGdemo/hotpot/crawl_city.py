import json
import time
import pymysql
import requests

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "hotpot")
cursor = db.cursor()


def city_list():
    url = "https://superapp.kiwa-tech.com/app/cityPosition/getCityList"
    payload = "{\"_HAIDILAO_APP_TOKEN\":\"\",\"customerId\":\"\"}"
    headers = {
        'user-agent': "MI 5(Android/6.0.1) Haidilao(Haidilao/6.1.0) Weex/0.18.17.71 1080x1920",
        'Content-Type': "application/json; charset=UTF-8",
        'Host': "superapp.kiwa-tech.com",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'cache-control': "no-cache",
    }
    proxies = get_ip()
    response = requests.request("POST", url, data=payload, headers=headers, verify=False, proxies=proxies)
    # print(response.text)
    response_text = json.loads(response.text)
    data = response_text.get('data')
    hotCityList = data.get('hotCityList')
    cityList = data.get('cityList')
    storage(hotCityList)
    storage(cityList)


def storage(city_list):
    for city in city_list:
        print(city)
        city_name = city.get('cityName')
        py = city.get('py')
        city_id = city.get('cityId')
        localtime = time.localtime(time.time())
        crawl_time = time.strftime("%Y-%m-%d", localtime)
        insert_sql = """insert ignore CITY_ID (cityId, city, py, crawlTime) VALUES ("%s","%s","%s","%s") """ % (
            city_id, city_name, py, crawl_time)
        cursor.execute(insert_sql)
        # 提交到数据库执行
        db.commit()


def get_ip():
    try:
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
        else:
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
    except Exception as e:
        print('当前代理挂掉了')
        pass


SECOND_DAY = 7 * 24 * 60 * 60


def delta_seconds():
    from datetime import datetime
    cur_time = datetime.now()
    des_time = cur_time.replace(hour=0, minute=1, second=0, microsecond=0)
    # 这里添加时间 replace()= Return a new datetime with new values for the specified fields.返回一个替换指定日期字段的新date对象
    delta = des_time - cur_time
    skip_seconds = delta.total_seconds() % SECOND_DAY  # total_seconds()是获取两个时间之间的总差
    print("Must sleep %d seconds" % skip_seconds)
    return skip_seconds


if __name__ == '__main__':
    # s = delta_seconds()
    # time.sleep(s)
    print("work it!")  # 这里可以替换成作业
    city_list()
