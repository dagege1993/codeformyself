import pymssql

import pymysql

conn = pymssql.connect(host='192.168.0.11', user='hlz1', password='hlz123')

cursor = conn.cursor()
sql = """select  top 100  app_id,avg(downs) downs   from  [dbo].[ANDROID_SAFE_APP_TOP]  WHERE stat_dt = '2018-12-02' group by app_id ORDER BY downs desc"""
cursor.execute(sql)
rows = cursor.fetchall()

# mysql
db = pymysql.connect("192.168.103.31", "root", "adminadmin", "downloads")
cursors = db.cursor()

for row in rows:
    # print(row)
    app_id = row[0]
    # print(app_id)
    new_sql = """select  DISTINCT stat_dt,  downs ,cate from ANDROID_SAFE_APP_TOP WHERE app_id = '%s' """ % '5726'
    cursors.execute(new_sql)
    results = cursors.fetchall()
    for result in results:
        print(result)
