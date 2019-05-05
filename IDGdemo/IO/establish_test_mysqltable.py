import pymysql

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "company")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute() 方法执行 SQL，如果表存在则删除
cursor.execute("DROP TABLE IF EXISTS TEST")

# 使用预处理语句创建表
sql = """CREATE TABLE TEST (
             company_name varchar(24)   NOT NULL unique,
             brief varchar(225) ,
             industry varchar(24)  ,
             city varchar(24)  ,
             finance_time varchar(24) ,
             finance varchar(24),
             money varchar(24),
             agency varchar(24),
             past_financing varchar(225),
             teams varchar(225),
             legal_name varchar(225),
             insert_times DATE)CHARACTER SET utf8 """
cursor.execute(sql)
# 提交到数据库执行
db.commit()

# 关闭数据库连接
db.close()
