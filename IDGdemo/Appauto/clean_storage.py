# encoding=utf8
import pandas as pd
import re
import time
import pymysql
from config_logs import Config

conf = Config()
logger = conf.getLog()


def get_city_level():
    path = r'city_level.xlsx'
    results = pd.read_excel(path)
    city_list = results['城市']
    level_list = results['城市等级']
    city_level_dict = dict(zip(city_list, level_list))
    # print(city_level_dict)
    return (city_level_dict)


def cleaning(page_source, city):
    """
    :param page_source: appnium获取到的源码
    :return: 门店列表大列表嵌套小列表
    """
    results = re.findall('<android.widget.TextView index=(.*?) class=', page_source)
    # logger.info(results)
    results = [result.replace('"0" ', '') for result in results]
    results = [result.replace('"1" ', '') for result in results]
    results = [result.replace('"2" ', '') for result in results]
    # logger.info(results)
    shop_data = []
    results = results[3:]
    logger.info(results)
    for i, text in enumerate(results):
        if 'km' in text or text == 'text="查看详情"' or text == 'text=""':
            pass
        else:
            # logger.info(text)
            shop_data.append(text)
    # 删除掉最后一个店铺名称,下一个会有,而且没有地址
    logger.info('预清洗的数据%s' % shop_data)
    # 如果有数据
    if shop_data:
        del shop_data[-1]
        shop_data = [shop.replace('text=', '') for shop in shop_data]  # 把列表里元素text=去掉
        shop_data = [shop.replace('"', '') for shop in shop_data]  # 把列表里元素"去掉
        shop_list = [shop_data[i:i + 3] for i in range(0, len(shop_data), 3)]  # 按照三个切分小列表
        # logger.info(shop_list)
        storage(shop_list, city)
    # return shop_list


def storage(shop_list, city):
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "shops")
    cursor = db.cursor()
    local_time = time.localtime(time.time())
    crawlTime = time.strftime('%Y-%m-%d', local_time)
    logger.info(shop_list)
    city_level_dict = get_city_level()
    for shop in shop_list:
        if len(shop) == 3:
            logger.info('要入库的信息%s' % shop)
            # 三种情况解析
            if 'No' in shop[0]:
                """"['总部基地东篱美食城店 (No.0921)','07:30-18:00', '丰台区总部基地十八区负一层W1814号' ]"""
                shopName = shop[0]
                shopId = re.findall('No.(.*\))', shopName).pop().replace(')', '')
                shopAddress = shop[2]
                shopTime = shop[1]
            if 'No' in shop[1]:
                """['丰台区大成路7号天利大厦一层东侧1-108室', '总部基地尚可味美食城店 (No.0020)', '07:30-18:00']"""
                shopName = shop[1]
                shopId = re.findall('No.(.*\))', shopName).pop().replace(')', '')
                shopAddress = shop[0]
                shopTime = shop[2]
            if 'No' in shop[2]:
                """"['07:30-18:00', '丰台区总部基地十八区负一层W1814号', '总部基地东篱美食城店 (No.0921)']"""
                # 这是第二种情况,
                shopName = shop[2]
                shopId = re.findall('No.(.*\))', shopName).pop().replace(')', '')
                shopAddress = shop[1]
                shopTime = shop[0]
                # logger.info('解析不出来的数据', shopName)
            if '敬请期待' in shop:
                open = 0
            else:
                open = 1

            city_level = city_level_dict.get(city)
            # ON DUPLICATE KEY UPDATE 这里用的是主键如果重复就是更新
            # insert_sql = """insert ignore Luckin_shop_detail (shopId,  shopName, shopAddress,shopTime,crawlTime,CityName) VALUES ("%s","%s","%s","%s","%s","%s") ON DUPLICATE KEY UPDATE shopAddress ='%s'""" % (
            #     shopId, shopName, shopAddress, shopTime, crawlTime, city, shopAddress)
            insert_sql = """insert ignore Luckin_shop_detail (shopId,  shopName, shopAddress,shopTime,crawlTime,CityName,city_level) VALUES ("%s","%s","%s","%s","%s","%s","%s") """ % (
                shopId, shopName, shopAddress, shopTime, crawlTime, city, city_level)
            # 这里存的是每天的流水表
            insert_sql2 = """insert ignore Luckin (shopId, crawlTime,open,city_level) VALUES ("%s","%s","%d","%s") """ % (
                shopId, crawlTime, open, city_level)
            logger.info(insert_sql)
            logger.info(insert_sql2)
            cursor.execute(insert_sql)
            cursor.execute(insert_sql2)
