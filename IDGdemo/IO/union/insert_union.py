import pymysql


def insert(sql):
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "company")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # SQL 插入语句
    sql = sql

    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        print(e)
        # 如果发生错误则回滚
        db.rollback()
        # print(sql)

    db.close()
