import pandas as pd

import pymysql

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "downloads")

path = r'C:\Users\Administrator.DESKTOP-DV7S27B\Desktop\需要维护的数据\下载量\下载量二级类和对应的种类.xlsx'
data_excel = pd.read_excel(path)
lv2 = data_excel['二级类']
category = data_excel['种类']
category_dict = dict(zip(lv2, category))
cursor = db.cursor()
inqury_sql = """select DISTINCT category_lv2 from ANDROID_QQ_APP where  category is null """
cursor.execute(inqury_sql)
category_lv2s = cursor.fetchall()
for category_lv2 in category_lv2s:
    category_lv2 = category_lv2[0]
    category = category_dict.get(category_lv2)
    print(category_lv2, category)
    sql = """UPDATE ANDROID_QQ_APP SET category = '%s' WHERE category_lv2 = '%s'""" % (category, category_lv2)
    print(sql)
    cursor.execute(sql)
    # # 提交到数据库执行
    db.commit()
print(category_dict)
