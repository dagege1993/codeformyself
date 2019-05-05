import pymysql

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "shops")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# 使用预处理语句创建表
sql = """
CREATE TABLE Luckin (
shopId varchar(10) NOT NULL primary key ,
CityName varchar(30) NOT NULL ,
shopName varchar(30) NOT NULL ,
shopAddress  varchar(100) NOT NULL ,
shopTime  varchar(10) NOT NULL ,
crawlTime date NOT NULL
)
             """
cursor.execute(sql)
# 提交到数据库执行
db.commit()

# 关闭数据库连接
db.close()
