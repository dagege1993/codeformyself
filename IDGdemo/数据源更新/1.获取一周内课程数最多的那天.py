import datetime
import operator

import pymysql

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "fluent")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

begin = datetime.date(2019, 3, 4)
end = datetime.date(2019, 3, 11)
dicts = {}
for i in range((end - begin).days + 1):
    day = begin + datetime.timedelta(days=i)
    print(day)
    sql = """select count(*) from COURSE WHERE times = '%s';""" % day
    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
    # 使用 fetchone() 方法获取一条数据
    data = cursor.fetchone()
    data = data[0]
    # print(data)
    dicts[str(day)] = data
# print(dicts)


# 按字典值降序排列

sorted_x = sorted(dicts.items(), key=operator.itemgetter(1), reverse=True)
print(sorted_x)
