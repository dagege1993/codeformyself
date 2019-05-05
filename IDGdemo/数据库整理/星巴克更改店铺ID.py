import pymysql

db = pymysql.connect('192.168.103.31', 'root', 'adminadmin', 'shops')
cursor = db.cursor()
sql2 = """select DISTINCT  shop_name from Starbucks_menu"""
cursor.execute(sql2)
result = cursor.fetchall()
for shop_name in result:
    try:
        shop_name = shop_name[0]
        sql = """select DISTINCT id from Starbucks WHERE shop_name ='%s'; """ % (shop_name)
        cursor.execute(sql)
        result = cursor.fetchone()
        id = result[0]
        up_sql = """update Starbucks_menu set shop_id = '%s' WHERE shop_name='%s'""" % (id, shop_name)
        print(up_sql)
        cursor.execute(up_sql)
    except Exception as e:
        pass
