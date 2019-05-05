# encoding=utf-8
import pymysql

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "downloads")
cursor = db.cursor()
sql = """select app_keys,app_id from ANDROID_QQ_APP """

cursor.execute(sql)
# 提交到数据库执行
result_data = cursor.fetchall()
for result in result_data:
    app_keys = result[0]
    app_id = result[1]
    # print(app_keys)
    change_sql = """update ANDROID_QQ_APP_DAILY SET app_keys = '%s'where app_id = '%s'""" % (app_keys, app_id)
    cursor.execute(change_sql)
    try:
        # 执行sql语句
        cursor.execute(change_sql)
        # 提交到数据库执行
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
