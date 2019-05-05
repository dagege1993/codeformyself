import pymysql

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "downloads")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用预处理语句创建表
sql = """
CREATE TABLE ANDROID_QQ_APP_2 (
app_id bigint NOT NULL ,
app_name varchar(120) NOT NULL ,
app_keys varchar(60) NOT NULL ,
app_shortname varchar(120) NOT NULL ,
app_pkg varchar(250) NOT NULL ,
app_md5 varchar(60) NOT NULL ,
author_id varchar(60) NOT NULL ,
author varchar(120) NOT NULL ,
version_id varchar(60) NOT NULL ,
in_dt date NOT NULL )
"""
cursor.execute(sql)
# 提交到数据库执行
db.commit()

# 关闭数据库连接
db.close()
