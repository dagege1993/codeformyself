import pandas as pd

import pymysql

path = r'city_level.xlsx'
results = pd.read_excel(path)
city_list = results['城市']
level_list = results['城市等级']
city_level_dict = dict(zip(city_list, level_list))

db = pymysql.connect('192.168.103.31', 'root', 'adminadmin', 'shops')
cursor = db.cursor()
sql = """select city  from Starbucks """
cursor.execute(sql)
results = cursor.fetchall()
for result in results:
    city = result[0]
    city_level = city_level_dict.get(city)
    if city_level:
        inquery_sql = """update Starbucks set city_level = '%s' where city = '%s' """ % (city_level, city)
        print(inquery_sql)
        cursor.execute(inquery_sql)
