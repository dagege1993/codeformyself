import pymysql

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "water_safe")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute() 方法执行 SQL，如果表存在则删除
cursor.execute("DROP TABLE IF EXISTS PLANS2")

# 使用预处理语句创建表
sql = """CREATE TABLE PLANS2 (
             insuranceTitle  varchar(24),
             years  INT,
             months  INT,
             schedule  INT,
             joinPerson  INT,
             period   varchar(24),
             times   DATE )CHARACTER SET utf8"""
cursor.execute(sql)
# 提交到数据库执行
db.commit()

# 关闭数据库连接
db.close()
