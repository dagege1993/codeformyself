import pymysql

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "company")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# SQL 插入语句

sql = """select types,legal_name,count(*) as count from unions1203  group by legal_name having count>1;"""
# sql = """select types,project_name,count(*) as count from unions1203  group by project_name having count>1;"""

# 执行sql语句
cursor.execute(sql)
# 提交到数据库执行
db.commit()
# 使用 fetchone() 方法获取一条数据
datas = cursor.fetchall()
for data in datas:
    print(data)
