import pymysql
import datetime
from union.insert_union import insert
from union.red_list import red_vc
from datetime import date, timedelta
db = pymysql.connect("192.168.103.31", "root", "adminadmin", "company")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

from datetime import date, timedelta
def get_day_of_day(n=0):
    '''''
    if n>=0,date is larger than today
    if n<0,date is less than today
    date format = "YYYY-MM-DD"
    '''
    if (n < 0):
        n = abs(n)
        return date.today() - timedelta(days=n)
    else:
        return date.today() + timedelta(days=n)


def today():
    '''''
    get today,date format="YYYY-MM-DD"
    '''''
    return date.today()


today = today().strftime('%Y-%m-%d')
before_day = get_day_of_day(-14).strftime('%Y-%m-%d')

# SQL 插入语句
# sql = """Select * From XINIU1203 Where DATE_FORMAT(finance_time,'%Y-%m-%d') >= '2018-10-01' and DATE_FORMAT(finance_time,'%Y-%m-%d') <= '2018-10-31' ORDER BY finance_time ;"""
sql = """Select * From XINIU1203 Where finance_time >= '%s' and finance_time <= '%s' ORDER BY finance_time ;"""%(today,before_day)
# sql = "Select * From XINIU1203 Where DATE_FORMAT(finance_time,'%Y-%m-%d') >= " + before_day + " and DATE_FORMAT(finance_time,'%Y-%m-%d') <= " + today + " ORDER BY finance_time ;"
print(sql)

try:
    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
    # 使用 fetchone() 方法获取一条数据
    datas = cursor.fetchall()
    for data in datas:
        agency = data[7]
        for red in red_vc:  # 这里是需要标红的vc
            if red in agency:
                red_or_not = 1
                break
            else:
                red_or_not = 0
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
