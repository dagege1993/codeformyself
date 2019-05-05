import datetime

import pymysql

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "fluent")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# SQL 插入语句
data_list = []


def serch(sql):
    sql = sql

    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
    # 使用 fetchone() 方法获取一条数据
    datas = cursor.fetchall()
    print(datas[0][0])
    return datas[0][0]


begin = datetime.date(2018, 11, 16)
end = datetime.date(2018, 12, 20)
dicts = {}
for i in range((end - begin).days + 1):
    day = begin + datetime.timedelta(days=i)
    print(day)
    sql = """select sum(studyUsersCount) from COURSE WHERE times = '%s';""" % day
    values = serch(sql)
    dicts[str(day)] = values
print(dicts)
