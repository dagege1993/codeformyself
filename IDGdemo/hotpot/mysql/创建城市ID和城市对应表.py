import pymysql

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "hotpot")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用预处理语句创建表
sql = """
CREATE TABLE CITY_ID (

cityId int NOT NULL ,

city varchar(30) NOT NULL ,
py  varchar(10) NOT NULL ,
crawlTime date NOT NULL
)


             """
cursor.execute(sql)
# 提交到数据库执行
db.commit()

# 关闭数据库连接
db.close()
