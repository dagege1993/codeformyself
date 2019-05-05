import pymysql

from union.insert_union import insert
from union.red_list import red_vc

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "company")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# SQL 插入语句
# sql = """Select * From ITORANGE Where DATE_FORMAT(finance_time,'%Y-%m-%d') >= '2018-10-01' and DATE_FORMAT(finance_time,'%Y-%m-%d') <= '2018-10-31' ORDER BY finance_time ;"""
sql = """Select * From ITORANGE Where DATE_FORMAT(finance_time,'%Y-%m-%d') >= '2018-11-26' and DATE_FORMAT(finance_time,'%Y-%m-%d') <= '2018-12-9' ORDER BY finance_time ;"""
try:
    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
    # 使用 fetchone() 方法获取一条数据
    datas = cursor.fetchall()
    for data in datas:
        # print(data[-1])
        # print(data)
        agency = data[7]
        for red in red_vc:
            if red in agency:
                red_or_not = 1
                break
            else:
                red_or_not = 0
        # print(red_or_not)
        results = list(data)
        results.append(red_or_not)
        data_tuple = tuple(results)
        print(data_tuple)
        sql = """INSERT INTO unions1203(project_name,brief,industry,city,finance_time,finance,money,agency,legal_person,legal_name,registered_capital,competing_product,past_financing,teams,types,insert_times,red_or_not) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%d","%s","%d")""" % data_tuple
        insert(sql)
except Exception as e:
    # 如果发生错误则回滚
    print(e)

    db.rollback()
db.close()
