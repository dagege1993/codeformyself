import pymysql


def insert_mysql():
    # 打开数据库连接
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "fluent", charset="utf8mb4")

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # SQL 插入语句
    # sql = """INSERT INTO PROVIDER(ID,
    #          TITLE, BODY, subscribesCount, episodesCount,times)
    #          VALUES ('NDM0MWYwMDAwMDAwMDBiYQ==', '雅思流利说口语小课堂', '雅思口语话题练习', 61905, 184,'2018-11-14')"""

    sql = """INSERT INTO COURSE(ID,
                                 diamondPrice, studyUsersCount, translatedTitle,times)
                                VALUES ("5b75235b636f6e61a000005c",889,888,"欢迎各路小伙伴加入雅","2018-11-14")"""
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


if __name__ == '__main__':
    for i in range(1):
        insert_mysql()