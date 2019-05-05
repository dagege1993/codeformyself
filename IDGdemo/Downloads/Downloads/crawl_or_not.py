import pymysql

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "downloads")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()


def determine_craw(sql):
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
    data = cursor.fetchone()
    if data:
        return 1
    else:
        return 0


# 返回未抓取得id
def get_lost_id(sql):
    id_list = []
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
    dataes = cursor.fetchall()
    for data in dataes:
        id = data[0]
        id_list.append(id)
    return id_list


# 给定id,返回id对应的类别
def get_lost_types(sql):
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
    data = cursor.fetchone()
    return data[0]
