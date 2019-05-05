# encoding=utf-8
import json
import time
import pymysql
import requests

requests.packages.urllib3.disable_warnings()  # 忽略警告


# 获取代理
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


# 获取全国门店列表
def start_crawl():
    shop_list_sql = """select DISTINCT storeId from SHOP_DETAIL"""
    cursor.execute(shop_list_sql)
    results = cursor.fetchall()
    shop_list = [shop[0] for shop in results]
    return shop_list


# 门店等待人数
def get_shop_waite(shopId):
    # 拿到Id后拼接成参数然后发送请求
    url = "https://superapp.kiwa-tech.com/app/getStoreById"
    payload = {'_HAIDILAO_APP_TOKEN': '', 'customerId': '', 'storeId': '020136'}
    # 更新店铺id
    payload['storeId'] = shopId
    payload = json.dumps(payload)
    headers = {
        'Content-Type': "application/json; charset=UTF-8",
        'Host': "superapp.kiwa-tech.com",
        # 'Connection': "Keep-Alive",
        'Connection': "close",
        'Accept-Encoding': "gzip",
        'cache-control': "no-cache",
    }
    proxies = get_ip()
    response = requests.request("POST", url, data=payload, headers=headers, verify=False, proxies=proxies, timeout=12)
    response_detail = json.loads(response.text)
    data = response_detail.get('data')
    storeId = data.get('storeId')
    rowNumber = data.get('rowNumber')
    webQueue = data.get('webQueue')
    for row in rowNumber:
        typeName = row.get('typeName')
        waitNum = row.get('waitNum')
        insert_sql = """insert ignore SHOP_WAITE2 (storeId,  waitNum,typeName,crawlTime,webque) VALUES ("%s","%s","%s","%s","%s") """ % (
        storeId, waitNum, typeName, start_time, webQueue)
        cursor.execute(insert_sql)
        db.commit()


# 第一次抓取完成后,去查还有多少没抓取完成的
def get_lost_shop():
    inqury_sql = """SELECT a.* FROM(
    SELECT storeId FROM SHOP_WAITE2 WHERE crawlTime = '%s' GROUP by storeId
    UNION ALL
    SELECT DISTINCT(storeId) FROM SHOP_DETAIL 
)a GROUP BY a.storeId HAVING COUNT(a.storeId)=1;""" % start_time
    print('查询缺失的sql', inqury_sql)
    cursor.execute(inqury_sql)
    lost_storid_list = cursor.fetchall()
    # 读出来结果是bytes类型,然后转为字符串
    lost_storid_list = [storid[0] for storid in lost_storid_list]
    # print(lost_storid_list)
    print('缺失抓取数量', len(lost_storid_list))
    return lost_storid_list


# 传id补剩下的店铺
def get_lost_wait(storeId, key):
    # 拿到Id后拼接成参数然后发送请求
    url = "https://superapp.kiwa-tech.com/app/getStoreById"
    payload = {'_HAIDILAO_APP_TOKEN': '', 'customerId': '', 'storeId': '020136'}
    # 更新店铺id
    payload['storeId'] = storeId
    payload = json.dumps(payload)
    headers = {
        'Content-Type': "application/json; charset=UTF-8",
        'Host': "superapp.kiwa-tech.com",
        # 'Connection': "Keep-Alive",
        'Connection': "close",
        'Accept-Encoding': "gzip",
        'cache-control': "no-cache",
    }
    # time.sleep(0.1)
    proxies = get_ip()
    if key == 1:
        response = requests.request("POST", url, data=payload, headers=headers, verify=False, proxies=proxies,
                                    timeout=12)
    if key == 2:
        response = requests.request("POST", url, data=payload, headers=headers, verify=False, timeout=12)

    response_detail = json.loads(response.text)
    data = response_detail.get('data')
    storeId = data.get('storeId')
    rowNumber = data.get('rowNumber')
    webque = data.get('webQueue')
    for row in rowNumber:
        typeName = row.get('typeName')
        waitNum = row.get('waitNum')
        insert_sql = """insert ignore SHOP_WAITE2 (storeId,  waitNum, typeName,crawlTime,webque) VALUES ("%s","%s","%s","%s","%s") """ % (
        storeId, waitNum, typeName, start_time, webque)

        cursor.execute(insert_sql)
        db.commit()


if __name__ == '__main__':
    print('开始工作')
    localtime = time.localtime(time.time())
    start_time = time.strftime("%Y-%m-%d %H:%M", localtime)
    # start_time = '2019-01-21 16:39:00'
    print('开始抓取时间', start_time)
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "hotpot")
    cursor = db.cursor()
    # 获取表中的总数
    shop_list = start_crawl()
    print('抓取门店长度', len(shop_list))
    # 获取每个门店的等待时间
    for shopId in shop_list:
        try:
            result = get_shop_waite(shopId)
        except Exception as e:
            pass
            # print(e)
    # 防止遗漏,拿到没有抓取下来的,用代理抓取
    print('第一次抓取完成,查看有没有遗失,用代理再抓一遍')
    for i in range(5):
        lost_storeId_list = get_lost_shop()
        # 因为有7个还没开启网络排队,这个数可能会变
        if len(lost_storeId_list) > 7:
            for storeId in lost_storeId_list:
                try:
                    # 传入1,启用代理,传入2,不启动代理
                    get_lost_wait(storeId, key=1)
                except Exception as e:
                    # print(e)
                    pass
        else:
            break
    # 上面是循环5次,携带代理,后面是不使用代理
    print('第一次抓取完成,查看有没有遗失,用本机IP再抓一遍')
    for i in range(5):
        lost_storeId_list = get_lost_shop()
        # 因为有7个还没开启网络排队,这个数可能会变
        if len(lost_storeId_list) > 7:
            print('开始不用代理抓取')
            for storeId in lost_storeId_list:
                try:
                    # 传入1,启用代理,传入2,不启动代理
                    get_lost_wait(storeId, key=2)
                except Exception as e:
                    # print(e)
                    pass
        else:
            break
    db.close()
    localtime = time.localtime(time.time())
    end_time = time.strftime("%Y-%m-%d %H:%M", localtime)
    print('抓取完毕时间', end_time)
