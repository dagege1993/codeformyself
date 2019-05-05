import pymysql

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "xibei")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用预处理语句创建表
sql = """
CREATE TABLE XIBEI_MENU (
storeId varchar(30) NOT NULL ,
city varchar(30) NOT NULL ,
food_name varchar(30) NOT NULL ,
food_code varchar(30) NOT NULL ,
food_unit varchar(30) NOT NULL ,
classes_name varchar(30) NOT NULL ,
food_price int ,
food_member_price int ,
crawlTime date NOT NULL)"""
cursor.execute(sql)
# 提交到数据库执行
db.commit()

# 关闭数据库连接
db.close()
