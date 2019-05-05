import pymysql
import csv

results = ['微信', 'QQ', '支付宝', '百度地图', '今日头条', '爱奇艺', '58同城', '快手', '手机淘宝', '京东']
mysql_dbs = ['360_downloads2', 'baidu_downloads2', 'tencent_downloads2']
result_list = []
db = pymysql.connect("192.168.103.31", "root", "adminadmin", "downloads")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
for result in results:
    for mysql_db in mysql_dbs:
        sql = """SELECT * from %s WHERE app_names = '%s'""" % (mysql_db, result)
        # print(sql)
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        # 使用 fetchone() 方法获取一条数据
        data = cursor.fetchone()
        if data:
            data = list(data)

            data.append(mysql_db)
            # print(data)
            result_list.append(data)

with open("test.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    for result in result_list:
        writer.writerow(result)
