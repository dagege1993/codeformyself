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


# 判断是否包含中文
def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


# 传入店铺名字.返回店铺ID
def get_shop_id(shop_name):
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "shops")
    shop_name = shop_name.replace('"', '')
    shop_name = shop_name + '%'
    cursor = db.cursor()
    get_shop_id_sql = """select * from Luckin_shop_detail WHERE shopName like '%s'""" % shop_name
    cursor.execute(get_shop_id_sql)
    results = cursor.fetchone()
    if results:
        results = results[0]
    return results


# 清洗数据
def cleaning_menu(page_source, city, shop_name):
    """
    :param page_source: appnium获取到的源码
    :return: 门店列表大列表嵌套小列表
    """
    results = re.findall('<android.widget.TextView index="\d+" text=(.*?) class', page_source)
    """results = ['"选择咖啡与小食"', '"人气Top"', '"大师咖啡"', '"零度拿铁"', '"瑞纳冰"', '"经典饮品"', '"BOSS午餐"', '"健康轻食"', '"鲜榨果蔬汁"', '"充2赠1"', '"焦糖拿铁"', '"Caramel Latte"', '"默认：大/单糖/热"', '"¥27"', '"充2赠1"', '"标准美式"', '"Americano"', '"默认：大/无糖/无奶/热"', '"¥21"', '"充2赠1"', '"加浓美式"', '"Extra Americano"', '"默认：大/无糖/无奶/热"', '"¥24"', '"充2赠1"', '"焦糖标准美式"', '"Caramel Americano"', '"默认：大/单糖/无奶/热"', '"¥24"', '"充2赠1"', '"焦糖加浓美式"', '"Caramel Extra Americano"', '"默认：大/单糖/无奶/热"', '"¥27"', '"充2赠1"', '"黑金气泡美式"', '"Black Gold Soda Americano"', '"默认：大"', '"¥24"', '"充2赠1"', '"澳瑞白"', '"Flat White"', '"默认：大/无糖/热"', '"¥27"', '"充2赠1"', '"卡布奇诺"', '"Cappuccino"', '"默认：大/无糖/热"', '"¥24"', '"首页"', '"菜单"', '"订单"', '"购物车"', '"我的"']"""
    # print(results)
    # 先要删除前面几个大类列表
    if '"充2赠1"' in results:
        p = results.index('"充2赠1"')
        remove_class_results = results[p:]  # 取值取到最后
        # 再删除后面的购物车之类的
        t = remove_class_results.index('"首页"')
        remove_end_results = remove_class_results[:t]  # 取值取到最后
        # print(remove_end_results)
    else:
        # print(results)
        # 这种是没有充2赠1的也是需要解析
        """['"选择咖啡与小食"', '"人气Top"', '"大师咖啡"', '"零度拿铁"', '"瑞纳冰"', '"经典饮品"', '"BOSS午餐"', '"健康轻食"', '"鲜榨果蔬汁"', '"经典牛肉土豆泥沙拉"', '"Beef and Mashed potato Salad"', '"¥25.08"', '"¥38"', '"川味鸡丝拌面套餐"', '"Szechuan Cold Noodles with Pulled Chicken"', '"¥23.1"', '"¥35"', '"樱桃番茄五谷食盒"', '"luckin Combo with Cherry Tomatoes"', '"¥23.1"', '"¥35"', '"10:00 6.6折"', '"夏威夷菠萝火腿卷(单卷)"', '"Hawaii Pineapple Ham Wrap"', '"¥8.58"', '"¥13"', '"蔓越莓司康"', '"Cranberry Scone"', '"¥9.9"', '"¥15"', '"巧克力麦芬"', '"Chocolate Muffin"', '"¥8.58"', '"¥13"', '"香椰提子麦芬"', '"Coconut Raisin Muffin"', '"¥8.58"', '"¥13"', '"香蕉核桃麦芬"', '"Banana Walnut Muffin"', '"¥8.58"', '"¥13"', '"首页"', '"菜单"', '"订单"', '"购物车"', '"我的"']"""
        remove_class_results = results[9:]  # 取值取到最后
        if '"首页"' in remove_class_results:
            t = remove_class_results.index('"首页"')
            remove_end_results = remove_class_results[:t]
        # print(remove_end_results)
        else:
            logger.info('当前解析数据没有包含首页')
            logger.info(remove_class_results)
            remove_end_results = []
    # 解析完成后都用同一个函数存入
    storage__menu(remove_end_results, city, shop_name)


# 存储数据
def storage__menu(results, city, shop_name):
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "shops")
    cursor = db.cursor()
    local_time = time.localtime(time.time())
    crawlTime = time.strftime('%Y-%m-%d', local_time)
    while '"10:00 6.6折"' in results:
        results.remove('"10:00 6.6折"')
    while '"08:00 6.6折"' in results:
        results.remove('"08:00 6.6折"')
    while '"07:00 6.6折"' in results:
        results.remove('"07:00 6.6折"')

    while '"不含咖啡的拿铁"' in results:
        results.remove('"不含咖啡的拿铁"')
    # 售罄可能会有很多个,所以需要循环
    while '"售罄"' in results:
        results.remove('"售罄"')
    if '"WBC（世界咖啡师大赛）冠军团队拼配"' in results:
        results.remove('"WBC（世界咖啡师大赛）冠军团队拼配"')
    # 上面是简单的数据清洗
    if '"充2赠1"' in results:
        counts = results.count('"充2赠1"')
        for i in range(counts):
            try:
                start = results.index('"充2赠1"')
                start = start + 1
                results = results[start:]
                end = results.index('"充2赠1"')
                data = results[:end]
                # 这里需要给数据列表添加优惠信息
                data.insert(2, "充2赠1")
                # 为了把默认字段删掉
                for tt in data:
                    if '默认' in tt:
                        data.remove(tt)
                if len(data) == 4:
                    print(data)
                    ShopId = get_shop_id(shop_name)
                    FoodName = data[0]
                    FoodName = FoodName.replace('"', '')
                    FoodEngName = data[1]
                    FoodEngName = FoodEngName.replace('"', '')
                    MemberPrice = data[2]
                    MemberPrice = MemberPrice.replace('"', '')
                    MemberPrice = MemberPrice.replace('¥', '')
                    Price = data[3]
                    Price = Price.replace('"', '')
                    Price = Price.replace('¥', '')  # 把符号去掉
                    shop_name = shop_name.replace('"', '')
                    insert_sql2 = """insert ignore Luckin_Menu (ShopId,CityName ,ShopName,FoodName,FoodEngName ,Price,MemberPrice ,CrawlTime ) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s") """ % (
                        ShopId, city, shop_name, FoodName, FoodEngName, Price, MemberPrice, crawlTime)
                    print(insert_sql2)
                    # logger.info(insert_sql2)
                    cursor.execute(insert_sql2)
            except Exception as e:
                pass
    # 如果不在
    else:
        for result in results:
            # print(result)
            is_chinese = is_Chinese(result.strip())
            if is_chinese is True:
                start = results.index(result)
                end = start + 4
                # print(start)
                try:
                    food_data = results[start:end]
                    if len(food_data) == 4:
                        print(food_data)
                        # 这里存的是每天的流水表
                        ShopId = get_shop_id(shop_name)
                        FoodName = food_data[0]
                        FoodName = FoodName.replace('"', '')
                        FoodEngName = food_data[1]
                        FoodEngName = FoodEngName.replace('"', '')
                        MemberPrice = food_data[2]
                        MemberPrice = MemberPrice.replace('"', '')
                        MemberPrice = MemberPrice.replace('¥', '')
                        Price = food_data[3]
                        Price = Price.replace('"', '')
                        Price = Price.replace('¥', '')  # 把符号去掉
                        shop_name = shop_name.replace('"', '')
                        insert_sql2 = """insert ignore Luckin_Menu (ShopId,CityName ,ShopName,FoodName,FoodEngName ,Price,MemberPrice ,CrawlTime ) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s") """ % (
                            ShopId, city, shop_name, FoodName, FoodEngName, Price, MemberPrice, crawlTime)
                        print(insert_sql2)
                        # logger.info(insert_sql2)
                        cursor.execute(insert_sql2)
                except Exception as e:
                    pass
