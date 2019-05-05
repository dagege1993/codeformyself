import pymysql

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "company")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# SQL 插入语句
data_list = []

sql = """select project_name  from unions1203 where verification_or_not = 0  and legal_name !='' and IDG_industry!=''"""
# sql = """select project_name  from unions1203  """

# 执行sql语句
cursor.execute(sql)
# 提交到数据库执行
db.commit()
# 使用 fetchone() 方法获取一条数据
datas = cursor.fetchall()
for data in datas:
    data_list.append(data[0])
print(data_list)
print(len(data_list))

for project_name in data_list:
    if '+' in project_name:
        print('项目名称包含+,需要手动处理一下', project_name)
    new_sql = """SELECT * FROM unions1203 where project_name   like "%{}%" ;""".format(project_name)

    cursor.execute(new_sql)
    # 提交到数据库执行
    db.commit()
    results = cursor.fetchall()
    result_len = len(results)
    if result_len > 1:
        print(new_sql)
    else:
        # 如果项目名称没有重复的,就把检查过verification_or_not这个字段改为1  UPDATE 表名称 SET 列名称 = 新值 WHERE 列名称 = 某值
        change_sql = """UPDATE unions1203 set verification_or_not = 1 where project_name = '%s'""" % project_name
        # print(change_sql)
        cursor.execute(change_sql)
        # 提交到数据库执行
        db.commit()
