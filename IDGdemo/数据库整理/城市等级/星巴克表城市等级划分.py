import pymysql
import pandas as pd


def add_city_level():
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "shops")
    cursor = db.cursor()
    inqury_sql = """select id,city from Starbucks"""
    cursor.execute(inqury_sql)
    city_level_dict = get_city_level()
    store_city_list = cursor.fetchall()
    for store_city in store_city_list:
        storeId = store_city[0]
        city = store_city[1]
        city = city.split('市')[0]
        city_level = city_level_dict.get(city)
        if city == '襄樊':
            city_level = '三线城市'
        if city == '西昌':
            city_level = '四/五线城市'
        if city_level:
            update_sql = """update Starbucks set city_level = '%s' where id = '%s'""" % (city_level, storeId)
            cursor.execute(update_sql)
        else:
            update_sql = """update Starbucks set city_level = '%s' where id = '%s'""" % ('中国大陆外', storeId)
            cursor.execute(update_sql)


def get_city_level():
    path = r'C:\Users\Administrator.DESKTOP-DV7S27B\Desktop\需要维护的数据\城市等级.xlsx'
    results = pd.read_excel(path)
    city_list = results['城市']
    level_list = results['城市等级']
    city_level_dict = dict(zip(city_list, level_list))
    print(city_level_dict)
    return (city_level_dict)


if __name__ == '__main__':
    add_city_level()
