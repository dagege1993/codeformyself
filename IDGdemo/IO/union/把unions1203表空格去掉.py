import pymysql

from union.insert_union import insert
from union.red_list import red_vc

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "company")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# SQL 插入语句
sql = """Select * From unions1203;"""

# 执行sql语句
cursor.execute(sql)
# 提交到数据库执行
db.commit()
# 使用 fetchone() 方法获取一条数据
datas = cursor.fetchall()
for data in datas:
    print(data)
    # old_name = data[0]
    # new_name = old_name.strip()
    # new_sql = "UPDATE unions1203 SET project_name = '%s' WHERE project_name = '%s'" % (new_name, old_name)
    # print(new_sql)
    # try:
    #     # 执行sql语句
    #     cursor.execute(new_sql)
    #     # 提交到数据库执行
    #     db.commit()
    # except Exception as e:
    #     print(e)
    #     # 如果发生错误则回滚
    #     db.rollback()

