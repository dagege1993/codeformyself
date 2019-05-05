import pymysql

db = pymysql.connect(host='192.168.103.31', user='root', password="adminadmin",
                     database='shops')
course = db.cursor()
sql = """
CREATE TABLE Starbucks_menu (
food_id varchar(18) NOT NULL ,
shop_id varchar(10) NOT NULL ,
subCategory_name varchar(30) NOT NULL ,
shop_name varchar(30)  ,
city varchar(30)  ,
city_level varchar(30)  ,
name varchar(30) NOT NULL ,
defaultPrice  varchar(10) NOT NULL ,
crawlTime date NOT NULL
)
"""

course.execute(sql)
