import pandas as pd

import pymysql


def get_city_level():
    path = r'city_level.xlsx'
    results = pd.read_excel(path)
    city_list = results['城市']
    level_list = results['城市等级']
    city_level_dict = dict(zip(city_list, level_list))
    print(city_level_dict)
    return (city_level_dict)


db = pymysql.connect('192.168.103.31', 'root', 'adminadmin', 'xibei')
cursor = db.cursor()
sql2 = """select DISTINCT  city from XIBEI_MENU"""
cursor.execute(sql2)
result = cursor.fetchall()
city_level_dict = get_city_level()
for city in result:
    try:
        shop_name = city[0].split('市')[0]
        city_level = city_level_dict.get(shop_name)
        up_sql = """update XIBEI_WAITE set city_level = '%s' WHERE city='%s'""" % (city_level, city[0])
        print(up_sql)
        cursor.execute(up_sql)
    except Exception as e:
        pass
