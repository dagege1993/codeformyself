# encoding=utf8
import json
import time
import pymysql
import requests
import multiprocessing

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


def get_today_shop_id_list(start_time):
    sql = """select storeId from SHOP_DETAIL WHERE crawlTime = '%s' and  storeStar is  Null""" % start_time
    cursor.execute(sql)
    results = cursor.fetchall()
    storeId_list = []
    for result in results:
        storeId = result[0]
        storeId_list.append(storeId)
    return storeId_list


# 获取分数
def get_store_stare(storeId, key):
    url = "https://superapp.kiwa-tech.com/app/getStoreById"
    payload = {'_HAIDILAO_APP_TOKEN': '', 'customerId': '', 'storeId': '020136'}
    # 更新店铺id
    payload['storeId'] = storeId
    payload = json.dumps(payload)
    headers = {
        'Content-Type': "application/json; charset=UTF-8",
        'Host': "superapp.kiwa-tech.com",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'cache-control': "no-cache",
        # 'Postman-Token': "8217bb42-f5d9-432f-a7cc-1b82865facda"
    }
    proxies = get_ip()
    # 参数等一1,使用代理,参数为2不使用代理
    if key == 1:
        response = requests.request("POST", url, data=payload, headers=headers, verify=False, proxies=proxies,
                                    timeout=12)
    if key == 2:
        response = requests.request("POST", url, data=payload, headers=headers, verify=False, timeout=12)
    # print(response.text)
    response_detail = json.loads(response.text)
    data = response_detail.get('data')
    storeStar = data.get('storeStar')
    update_sql = """UPDATE SHOP_DETAIL SET storeStar = %s WHERE storeId = '%s' and crawlTime = '%s'""" % (
        storeStar, storeId, start_time)
    print(update_sql)
    cursor.execute(update_sql)


if __name__ == '__main__':
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "hotpot")
    cursor = db.cursor()
    localtime = time.localtime(time.time())
    start_time = time.strftime("%Y-%m-%d", localtime)
    # start_time = '2019-01-20 16:39:00'
    print('开始抓取时间', start_time)
    # 获取今日全部门店ID
    storeId_list = get_today_shop_id_list(start_time)
    print('还有剩余店铺缺失', len(storeId_list))
    # 单进程版本
    for i in range(5):
        if len(storeId_list) > 1:
            for storeId in storeId_list:
                try:
                    get_store_stare(storeId, 1)
                    # 传入1,启用代理,传入2,不启动代理
                except Exception as e:
                    pass
    storeId_list = get_today_shop_id_list(start_time)
    if storeId_list:
        print('不用代理跑剩下的店铺')
        for i in range(5):
            storeId_list = get_today_shop_id_list(start_time)
            if len(storeId_list) > 1:
                for storeId in storeId_list:
                    try:
                        get_store_stare(storeId, 1)
                        # 传入1,启用代理,传入2,不启动代理
                    except Exception as e:
                        pass

    # # 多进程版本
    # pool = multiprocessing.Pool(processes=4)
    # for storeId in storeId_list:
    #     try:
    #         pool.apply_async(get_store_stare, (storeId, 1))  # 维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
    #     except Exception as e:
    #         print(e)
    # # 等待所有子进程运行完毕后在运行剩余部分
    # pool.close()
    # pool.join()
    # storeId_list = get_today_shop_id_list(start_time)
    # if storeId_list:
    #     print('还有剩余店铺缺失', len(storeId_list))
    #     for storeId in storeId_list:
    #         try:
    #             pool.apply_async(get_store_stare, (storeId, 2))  # 维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
    #         except Exception as e:
    #             pass
    #     # 等待所有子进程运行完毕后在运行剩余部分
    #     pool.close()
    #     pool.join()
