# encoding=utf-8
import pymysql

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "downloads")
cursor = db.cursor()
# sql = """select app_keys from ANDROID_QQ_APP """
sql = """select app_id from ANDROID_QQ_APP """
cursor.execute(sql)
# 提交到数据库执行
result_data = cursor.fetchall()
for result in result_data:
    # app_keys = result[0]
    app_id = result[0]
    # print(app_keys)
    Inquire_sql = """select cate,sort from ANDROID_QQ_APP_TOP where app_id = '%s' order by stat_dt desc """ % app_id
    cursor.execute(Inquire_sql)
    # 提交到数据库执行
    result_data = cursor.fetchone()
    cate = result_data[0]
    sort = result_data[1]
    print(cate)
    change_sql = """update ANDROID_QQ_APP SET category_lv1 = '%s',category_lv2='%s' where app_id = '%s'""" % (
        cate, sort, app_id)
    try:
        # 执行sql语句
        cursor.execute(change_sql)
        # 提交到数据库执行
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
