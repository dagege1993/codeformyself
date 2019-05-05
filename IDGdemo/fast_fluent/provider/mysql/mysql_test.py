import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "adminadmin", "TESTDB", charset="utf8mb4")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# SQL 插入语句
# sql = """INSERT INTO PROVIDER(ID,
#          TITLE, BODY, subscribesCount, episodesCount,times)
#          VALUES ('NDM0MWYwMDAwMDAwMDBiYQ==', '雅思流利说口语小课堂', '雅思口语话题练习', 61905, 184,'2018-11-14')"""


sql = """INSERT INTO PROVIDER(ID,
                         TITLE, BODY, subscribesCount, episodesCount,times)
                        VALUES ("NDM0MWYwMDAwMDAwMDBiYQ==",  "苏珊教美语创始人","\"苏珊教美语\"创始人，原创英语主播，资深在线美语老师。每日跟苏珊学性感美语。", 61905, 184, "2018-11-14")"""
# try:
#     # 执行sql语句
#     cursor.execute(sql)
#     # 提交到数据库执行
#     db.commit()
# except:
#     # 如果发生错误则回滚
#     db.rollback()

cursor.execute(sql)
# 提交到数据库执行
db.commit()

# 关闭数据库连接
db.close()
