import pymysql

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "xibei")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用预处理语句创建表
sql = """
CREATE TABLE XIBEI_WAITE (
storeId varchar(30) NOT NULL ,
storeName varchar(30) NOT NULL ,
wait varchar(30)  ,
qname varchar(30)  ,
waittime varchar(30) ,
city varchar(30) NOT NULL ,
open_or_not int NOT NULL,
crawlTime datetime NOT NULL)"""
cursor.execute(sql)
# 提交到数据库执行
db.commit()

# 关闭数据库连接
db.close()
