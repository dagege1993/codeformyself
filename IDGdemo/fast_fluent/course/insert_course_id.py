import pymysql


from course.mysql_get_course_id import get_course_id


def insert_id():
    # 打开数据库连接
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "fluent", charset="utf8mb4")

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    id_set = get_course_id()  # 获取所有课程去重后的id
    for id in id_set:
        # SQL 查询语句
        sql = """INSERT INTO COURSE_ID(ID)
                                VALUES ("%s")""" % (id)
        try:
            # 执行SQL语句
            cursor.execute(sql)

        except:
            print("insert id is wrong")

    # 关闭数据库连接
    db.close()


if __name__ == '__main__':
    insert_id()
