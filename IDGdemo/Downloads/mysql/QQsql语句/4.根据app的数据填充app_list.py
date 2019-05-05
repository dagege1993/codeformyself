# encoding=utf-8
import pymysql

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "downloads")
cursor = db.cursor()
sql = """select * from ANDROID_QQ_APP """

cursor.execute(sql)
# 提交到数据库执行
result_data = cursor.fetchall()
for result in result_data:
    app_keys = result[0]
    app_id = result[1]
    app_name = result[2]
    app_shortname = result[3]
    app_pkg = result[4]
    app_md5 = result[5]
    # author_id = result[6]
    # author = result[7]
    version_id = result[8]
    in_dt = result[9]
    insert_sql = """insert into ANDROID_QQ_APP_LIST (app_id, app_name, app_keys, app_shortname, app_pkg, app_md5, version_id, in_dt) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s") """ % (
        app_id, app_name, app_keys, app_shortname, app_pkg, app_md5, version_id, in_dt)
    # print(insert_sql)
    cursor.execute(insert_sql)
