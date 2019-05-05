# 获取代理
import json
import re
import time
import pymysql
import requests

requests.packages.urllib3.disable_warnings()  # 忽略警告
# city_list = ["北京市", "上海市", "深圳市", "郑州市", "西安市", "武汉市", "南京市", "广州市", "杭州市", "苏州市", "青岛市", "天津市", "长沙市", "成都市",
#              "昆明市", "厦门市", "南昌市", "无锡市", "南通市", "常州市", "福州市", "沈阳市", "银川市", "宁波市", "泉州市", "合肥市", "烟台市", "石家庄市", "哈尔滨市",
#              "长春市",]


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


def get_city_list():
    get_city_sql = """select DISTINCT(city) from SHOP_DETAIL WHERE city_level !='中国大陆外'"""
    cursor.execute(get_city_sql)
    results = cursor.fetchall()
    city_list = [result[0] for result in results]
    return city_list


def get_unit(itemName):
    if itemName not in ['单锅', '鸳鸯锅', '四宫格']:
        if "半" in itemName:
            unit = '半份'
        elif "个" in itemName:
            unit = re.findall('(\d+)个', itemName)
            if len(unit) >= 1:
                unit = unit[0] + '个'
            else:
                unit = '一个'
        elif '啤酒' in itemName:
            unit = re.findall('(\d+)瓶', itemName)
            if len(unit) >= 1:
                unit = unit[0] + '瓶'
            else:
                unit = '一瓶'
        elif "两" in itemName:
            unit = '一两'
        elif "条" in itemName:
            unit = '一条'
        elif 'ml' in itemName or 'ML' in itemName:
            unit = re.findall('.*?(\d+)[ML,ml]', itemName)
            if unit:
                unit = unit[0] + "ML"
        elif 'L' in itemName:
            unit = re.findall('(\d+.*?)L', itemName)
            if unit:
                unit = unit[0] + "L"
        else:
            unit = '一份'
    else:
        if itemName == '单锅':
            unit = '一份'
        if itemName == '鸳鸯锅':
            unit = '半份'
        if itemName == '四宫格':
            unit = '四分之一份'

    return unit


def deter_shops2():
    storeid_list = []
    city_list = get_city_list()
    # 这里做了一下限制
    for city in city_list:
        sql = """select distinct storeId from SHOP_DETAIL where crawlTime = '2019-02-12' and city = '%s' limit 3""" % city
        cursor.execute(sql)
        results = cursor.fetchall()
        for result in results:
            storeid = str(result[0])
            # 生成一个字典关于id和城市
            storeid_city_dict = {}
            storeid_city_dict[storeid] = city
            storeid_list.append(storeid_city_dict)
    return storeid_list


def lost_shop():
    sql = """select DISTINCT storeId from SHOP_MENU WHERE crawlTime = '%s'""" % start_time
    cursor.execute(sql)
    results = cursor.fetchall()
    lost_shop_len = results[0]
    # 如果长度等于90,认为没有缺失数据
    if lost_shop_len == 90:
        lost_shop = 1
    else:
        lost_shop = 0
    return lost_shop


def crawl(storeId_city, key):
    import requests
    url = "https://superapp.kiwa-tech.com/app/dish/list"
    payload = {'_HAIDILAO_APP_TOKEN': '', 'customerId': '', 'storeId': '020136'}
    payload['storeId'] = list(storeId_city.keys())[0]  # 返回dict_keys类型，其性质类似集合(set)而不是列表(list)，因此不能使用索引获取其元素
    # payload['storeId'] = "090201"
    payload = json.dumps(payload)
    headers = {
        'Content-Type': "application/json; charset=UTF-8",
        'Host': "superapp.kiwa-tech.com",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'cache-control': "no-cache",
    }

    # 参数等1,使用代理,参数为2不使用代理
    if key == 1:
        proxies = get_ip()
        response = requests.request("POST", url, data=payload, headers=headers, verify=False, proxies=proxies,
                                    timeout=6)
    if key == 2:
        response = requests.request("POST", url, data=payload, headers=headers, verify=False)
    # 存储阶段
    if response.status_code == 200:
        response_detail = json.loads(response.text)
        data = response_detail.get('data')
        for result in data:
            dishTypeName = result.get('dishTypeName')
            bodyList = result.get('bodyList')
            if dishTypeName == '锅底':  # 锅底算二级类
                if bodyList:  # 如果不为空
                    for body in bodyList:
                        bodyList2 = body.get('bodyList')
                        dishTypeName = body.get('dishTypeName')
                        if bodyList2:
                            for body2 in bodyList2:
                                if body2:
                                    itemId = body2.get('itemId')
                                    if itemId:
                                        itemId = itemId.split("_")[0]
                                        itemName = body2.get('itemName')
                                        # 获取份数
                                        unit = get_unit(dishTypeName)
                                        price = body2.get('price')
                                        insert_sql = """insert ignore SHOP_MENU (storeId,city,itemName,dishTypeName,itemId,price,crawlTime,unit) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s") """ % (
                                            list(storeId_city.keys())[0], list(storeId_city.values())[0], itemName,
                                            dishTypeName, itemId, price, start_time, unit)
                                        cursor.execute(insert_sql)
                                        db.commit()
            else:
                if bodyList:  # 如果不为空
                    for body3 in bodyList:
                        if body3:
                            itemList = body3.get('itemList')
                            if itemList:  # 有半份的
                                # pass
                                for item in itemList:
                                    itemId = item.get('itemId')
                                    if itemId:
                                        itemId = itemId.split('_')[0]
                                        itemName = item.get('itemName')
                                        # 获取份数
                                        unit = get_unit(itemName)
                                        price = item.get('price')
                                        insert_sql = """insert ignore SHOP_MENU (storeId,city,itemName,dishTypeName,itemId,price,crawlTime,unit) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s") """ % (
                                            list(storeId_city.keys())[0], list(storeId_city.values())[0], itemName,
                                            dishTypeName,
                                            itemId, price, start_time, unit)
                                        cursor.execute(insert_sql)
                                        db.commit()
                            else:  # 没有半份的
                                itemId = body3.get('itemId')
                                if itemId:
                                    itemId = itemId.split('_')[0]
                                    itemName = body3.get('itemName')
                                    unit = get_unit(itemName)
                                    price = body3.get('price')
                                    insert_sql = """insert ignore SHOP_MENU (storeId,city,itemName,dishTypeName,itemId,price,crawlTime,unit) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s") """ % (
                                        list(storeId_city.keys())[0], list(storeId_city.values())[0], itemName,
                                        dishTypeName,
                                        itemId, price, start_time, unit)
                                    cursor.execute(insert_sql)
                                    db.commit()


if __name__ == '__main__':
    print('开始工作')
    localtime = time.localtime(time.time())
    start_time = time.strftime("%Y-%m-%d ", localtime)
    start_times = time.strftime("%Y-%m-%d %H:%M", localtime)
    # start_time = '2019-01-20 16:39:00'
    print('开始抓取时间', start_times)
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "hotpot")
    cursor = db.cursor()
    # 获取表中的总数
    menu_storeid_list = deter_shops2()
    print('抓取门店长度', len(menu_storeid_list))
    print('抓取门店长度', menu_storeid_list)
    # 单机版太慢
    for storeId_city in menu_storeid_list:
        try:
            time.sleep(1)
            crawl(storeId_city, 1)
        except Exception as e:
            pass
    # 因为不好判断何为缺失,所以干脆不用代理再跑一遍
    for storeId_city in menu_storeid_list:
        try:
            time.sleep(1)
            crawl(storeId_city, 2)
        except Exception as e:
            pass

    # 多进程版本
    # import multiprocessing
    #
    # pool = multiprocessing.Pool(processes=4)
    #
    #
    # if len(menu_storeid_list) > 1:
    #     for storeId_city in menu_storeid_list:
    #         try:
    #             pool.apply_async(crawl, (storeId_city, 1))
    #             # 传入1,启用代理,传入2,不启动代理
    #         except Exception as e:
    #             pass
    #
    # # 等待所有子进程运行完毕后在运行剩余部分
    # pool.close()
    # pool.join()
    # # 上面是循环5次,携带代理,后面是不使用代理
    # print('第一次抓取完成,查看有没有遗失,用本机IP再抓一遍')
    # for i in range(5):
    #     menu_storeid_list = deter_shops2()
    #     # 因为有7个还没开启网络排队,这个数可能会变
    #     if len(menu_storeid_list) > 1:
    #         print('开始不用代理抓取')
    #         for storeId_city in menu_storeid_list:
    #             try:
    #                 # 非阻塞,主函数会自己执行自个的，不搭理进程的执行
    #                 pool.apply_async(crawl, (storeId_city, 2))
    #             except Exception as e:
    #                 pass
    #     else:
    #         break
    # # 等待所有子进程运行完毕后在运行剩余部分
    # pool.close()
    # pool.join()
    # db.close()

    localtime = time.localtime(time.time())
    end_time = time.strftime("%Y-%m-%d %H:%M", localtime)
    print('抓取完毕时间', end_time)
