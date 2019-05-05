import time

import pymysql


db = pymysql.connect("192.168.103.31", "root", "adminadmin", "company")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# SQL 插入语句
sql = """Select * From ITORANGE;"""




# 执行sql语句
cursor.execute(sql)
# 提交到数据库执行
db.commit()
# 使用 fetchone() 方法获取一条数据
datas = cursor.fetchall()
for data in datas:
    print(data)
    old_name = data[0]
    ss = data[4]
    timeArray = time.strptime(ss, "%Y-%m-%d")
    ss = time.strftime("%Y-%m-%d", timeArray)
    print(ss)
    new_sql = "UPDATE ITORANGE SET finance_time = '%s' WHERE project_name = '%s'" % (ss, old_name)
    # print(new_sql)
    try:
        # 执行sql语句
        cursor.execute(new_sql)
        # 提交到数据库执行
        db.commit()
        # print(data)
    except Exception as e:
        print(e)
        # 如果发生错误则回滚
        db.rollback()