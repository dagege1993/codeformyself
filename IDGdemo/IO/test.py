# encoding=utf8
import time

import pymysql

print(len([1, 2, 3, 4]))
print(len(['你好', '是吗']))
print(len(['nihjao', 'shima']))

result = '以孕产瑜伽为切入点，为瑜伽馆提供线上教学等服务的互联网＋平台'
print(len(bytes(result, encoding='utf-8')))
localtime = time.localtime(time.time())
str_time = time.strftime("%Y-%m-%d", localtime)
db = pymysql.connect("192.168.103.31", "root", "adminadmin", "company")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# SQL 插入语句
sql = """INSERT INTO XINIU(company_name,brief,industry,city,finance_time,finance,money,agency,insert_times) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s")""" % (
    '酷袋科技', '游戏产品开发商', '文化娱乐', '上海', '2016-03-17', '天使轮', '未披露', 'None', str_time)

# 执行sql语句
cursor.execute(sql)
# 提交到数据库执行
db.commit()
# 关闭数据库连接
db.close()
