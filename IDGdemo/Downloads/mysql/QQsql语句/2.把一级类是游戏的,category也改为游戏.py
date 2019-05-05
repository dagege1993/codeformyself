# encoding=utf-8
import pymysql

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "downloads")

cursor = db.cursor()

sql = """UPDATE ANDROID_QQ_APP SET category = '游戏' WHERE category_lv1 = '游戏'"""
print(sql)
cursor.execute(sql)
# 提交到数据库执行
db.commit()
