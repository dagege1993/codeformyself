import pymysql

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "company")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# SQL 插入语句

# sql = """select types,legal_name,count(*) as count from unions1203  group by legal_name having count>1;"""
sql = """select project_name,count(*) as count from unions1203  group by project_name having count>1;"""

# 执行sql语句
cursor.execute(sql)
# 提交到数据库执行
db.commit()
# 使用 fetchone() 方法获取一条数据
datas = cursor.fetchall()
for data in datas:
    company_name = data[0]
    delete_sql = """delete from unions1203 where project_name = '%s' and types = 3""" % (company_name)
    cursor.execute(delete_sql)
