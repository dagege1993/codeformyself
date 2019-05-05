import pymysql

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "downloads")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
new_sql = """select * from 360_downloads2"""
cursor.execute(new_sql)
results = cursor.fetchall()
for result in results:
    print(result)


    insert_sql = """"""