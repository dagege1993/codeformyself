import pymysql

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "shops")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# 使用预处理语句创建表
sql = """CREATE TABLE Luckin_Menu (
ShopId varchar(10) NOT NULL   ,
CityName varchar(30) NOT NULL ,
ShopName varchar(30) NOT NULL ,
FoodName varchar(30) NOT NULL ,
FoodEngName varchar(30) NOT NULL ,
Price varchar(30) NOT NULL ,
MemberPrice varchar(30) NOT NULL ,
CrawlTime date NOT NULL
)"""
cursor.execute(sql)
# 提交到数据库执行
db.commit()

# 关闭数据库连接
db.close()
