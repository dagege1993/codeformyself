import pymysql


def get_course_ids():
    # 打开数据库连接
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "fluent", charset="utf8mb4")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # SQL 查询语句
    sql = """SELECT ID FROM COURSE_ID"""

    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        id_set = set()
        for row in results:
            id_set.add("".join(row))  # 元祖转字符串
        print(id_set)
        print('课程ID总数', len(id_set))
        return id_set
    except:
        print("Error: unable to fetch data")
    # 关闭数据库连接
    db.close()


# 返回的是ID总数
def course_id_count():
    # 打开数据库连接
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "fluent", charset="utf8mb4")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # SQL 查询语句
    sql = """SELECT count(*) from COURSE_ID"""
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 使用 fetchone() 方法获取一条数据
        data = cursor.fetchone()

        for i in data:  # 包含一个数字的元祖类型
            pass
        return i
    except:
        print("get course_id count is failed")
        return 0
    # 关闭数据库连接
    db.close()

#
# if __name__ == '__main__':
#     print(course_id_count())
