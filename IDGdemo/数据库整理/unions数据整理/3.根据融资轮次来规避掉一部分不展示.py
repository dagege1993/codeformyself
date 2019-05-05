import pymysql

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "company")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# SQL 插入语句

delete_finance = ["新三板", "债权融资", "新三板定增", "定向增发", "新三板定增轮", "主板定向增发", "上市定增轮", ]

for finance in delete_finance:

    # sql = """select * from unions1203   WHERE types=4  and finance_time>= '2018-11-01' and  finance='%s' """ % finance
    sql = """select * from unions1203   WHERE   finance='%s' """ % finance
    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
    # 使用 fetchone() 方法获取一条数据
    datas = cursor.fetchall()
    for data in datas:
        # print(data)
        project_name = data[0]
        finance_time = data[4]
        # print(project_name, finance_time)
        # 如果项目名称没有重复的,就把检查过verification_or_not这个字段改为1  UPDATE 表名称 SET 列名称 = 新值 WHERE 列名称 = 某值
        change_sql = """UPDATE unions1203 set verification_or_not = 3 where project_name = '%s' and finance_time = '%s'""" % (
            project_name, finance_time)
        # print(change_sql)
        cursor.execute(change_sql)
        # 提交到数据库执行
        db.commit()
