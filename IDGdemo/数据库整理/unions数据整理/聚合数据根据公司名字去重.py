import pymysql

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "company")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# SQL 插入语句
data_list = []

sql = """select legal_name  from unions1203   """

# 执行sql语句
cursor.execute(sql)
# 提交到数据库执行
db.commit()
# 使用 fetchone() 方法获取一条数据
datas = cursor.fetchall()
for data in datas:
    data = data[0]
    if data:
        print(data)
        data_list.append(data)
print(data_list)
print(len(data_list))

for project_name in data_list:
    new_sql = """SELECT * FROM unions1203 where legal_name   like "%{}%" ;""".format(project_name)

    cursor.execute(new_sql)
    # 提交到数据库执行
    db.commit()
    # 使用 fetchone() 方法获取一条数据
    results = cursor.fetchall()
    result_len = len(results)
    if result_len > 1:
        print(new_sql)
        # print(results)
