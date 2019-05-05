import pymysql


def update_musql():
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "company")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # SQL 插入语句
    # sql = "UPDATE XINIU SET legal_name = '%s',legal_person='%s' WHERE company_name = '%s'" % ('jack', 'jackhuang', '赛瑞特物流')
    sql = "UPDATE XINIU SET legal_name = 'jack',legal_person='jack' WHERE company_name = '赛瑞特物流'"
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        # 如果发生错误则回滚
        print(e)
        db.rollback()

    db.close()


if __name__ == '__main__':
    update_musql()
