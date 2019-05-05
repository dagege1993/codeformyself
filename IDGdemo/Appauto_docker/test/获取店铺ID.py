import pymysql


def get_shop_id(shop_name):
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "shops")
    shop_name = shop_name.replace('"', '')
    shop_name = shop_name+'%'
    cursor = db.cursor()
    get_shop_id_sql = """select * from Luckin_shop_detail WHERE shopName like '%s'""" % shop_name
    print(get_shop_id_sql)
    cursor.execute(get_shop_id_sql)
    results = cursor.fetchone()
    if results:
        results = results[0]
    return results


if __name__ == '__main__':
    shop_name = '"龙湖天街店"'
    get_shop_id(shop_name)
