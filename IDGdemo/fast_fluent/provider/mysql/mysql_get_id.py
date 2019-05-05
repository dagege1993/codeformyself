import pymysql


def get_id():
    # 打开数据库连接
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "fluent", charset="utf8mb4")

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # SQL 查询语句
    sql = """SELECT ID FROM PROVIDER"""

    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        id_set = set()
        for row in results:
            id_set.add("".join(row))  # 元祖转字符串
        print(id_set)
        print(len(id_set))
        return id_set
    except:
        print("Error: unable to fecth data")

    # 关闭数据库连接
    db.close()
    # cursor.execute(sql)
    # # 提交到数据库执行
    # db.commit()
    #
    # # 关闭数据库连接
    # db.close()


if __name__ == '__main__':
    get_id()
