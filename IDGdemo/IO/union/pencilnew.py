import pymysql

from union.insert_union import insert
from union.red_list import red_vc

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "company")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# SQL 插入语句

sql = """Select * From PENCILENEW Where DATE_FORMAT(finance_time,'%Y-%m-%d') >= '2018-02-05' and DATE_FORMAT(finance_time,'%Y-%m-%d') <= '2019-03-01' ORDER BY finance_time ;"""
# try:
# 执行sql语句
cursor.execute(sql)
# 提交到数据库执行
db.commit()
datas = cursor.fetchall()
for data in datas:
    agency = data[7]
    for red in red_vc:
        if red in agency:
            red_or_not = 1
            break
        else:
            red_or_not = 0
    results = list(data)
    # 得把最后一个公司id给去掉
    del results[-1]
    results.append(str(red_or_not))
    data_tuple = tuple(results)
    print(data_tuple)
    print(len(data_tuple))
    sql = """INSERT INTO unions1203(project_name,brief,industry,city,finance_time,finance,money,agency,legal_person,legal_name,registered_capital,competing_product,past_financing,teams,types,insert_times,red_or_not) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%d","%s","%s")""" % data_tuple
    print(sql)
    # 自定义的插入函数
    insert(sql)
