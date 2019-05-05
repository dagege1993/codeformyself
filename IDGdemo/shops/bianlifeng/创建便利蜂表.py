import pymysql

db = pymysql.connect(host='192.168.103.31', user='root', password="adminadmin",
                     database='shops')
course = db.cursor()
sql = """
CREATE TABLE BianLiFeng (
id varchar(10) NOT NULL ,
city varchar(30) NOT NULL ,
shop_name varchar(30) NOT NULL ,
district varchar(30) NOT NULL ,
address  varchar(100) NOT NULL ,
crawlTime date NOT NULL
)
"""

course.execute(sql)
