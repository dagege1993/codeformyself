# encoding=utf8
import pymysql

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "downloads")

cursor = db.cursor()

sql = """UPDATE ANDROID_SAFE_APP SET category = '游戏' WHERE category_lv1 = '游戏'"""
print(sql)
cursor.execute(sql)
# �ύ�����ݿ�ִ��
db.commit()
