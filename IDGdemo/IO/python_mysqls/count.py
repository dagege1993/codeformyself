import pymysql


def find(query_conditions):
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "company")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # SQL 插入语句
    sql = """SELECT * FROM XINIU WHERE {}='{}'""".format(query_conditions['Inquire_key'],
                                                         query_conditions['Inquire_value'])
    # sql = """SELECT * FROM XINIU WHERE {name}='微纳星空'""".format(name=query_conditions['Inquire_key'])
    # sql = """SELECT * FROM XINIU WHERE company_name='微纳星空'"""

    try:
        # 执行sql语句
        cursor.execute(sql)
        data = cursor.fetchall()
        print(data)
        if data:
            print('dang')
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        # 如果发生错误则回滚
        print(e)
        db.rollback()

    db.close()


if __name__ == '__main__':
    query_conditions = {'Inquire_key': 'company_name', 'Inquire_value': '微纳星空'}
    find(query_conditions)
