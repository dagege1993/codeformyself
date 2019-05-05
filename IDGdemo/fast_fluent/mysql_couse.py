import os
import sys
import time
import pymysql

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# 获取已经抓取到的ID
def get_crawled_id(table_name, times):
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "fluent")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = """select  ID from %s where times='%s'""" % (table_name, times)
    cursor.execute(sql)
    db.commit()
    # 获取所有记录列表
    results = cursor.fetchall()
    id_list = []
    for result in results:
        # print(result)
        result = ''.join(result)
        id_list.append(result)
    # print(id_list)
    # 关闭数据库连接
    db.close()
    return id_list


# 获取自己建立的课程ID库
def get_course_id():
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "fluent")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = """select  ID from COURSE_ID """
    cursor.execute(sql)
    db.commit()
    # 获取所有记录列表
    results = cursor.fetchall()
    id_list = []
    for result in results:
        # print(result)
        result = ''.join(result)
        id_list.append(result)
    # print(id_list)
    # 关闭数据库连接
    db.close()
    return id_list


# 返回未抓取的课程ID
def un_get_id():
    course_id_list = get_course_id()
    table_name = 'COURSE'
    localtime = time.localtime(time.time())
    strtime = time.strftime("%Y-%m-%d", localtime)
    times = strtime
    crawled_id_list = get_crawled_id(table_name, times)
    un_get_id_list = set(course_id_list) - set(crawled_id_list)  # 转为集合后取差值
    print(un_get_id_list)
    print(len(un_get_id_list))
    return un_get_id_list


if __name__ == '__main__':
    un_get_id()
