import pymysql
import pandas as pd


def delete_city_shi():
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "shops")
    cursor = db.cursor()
    inqury_sql = """select id,city from Starbucks"""
    cursor.execute(inqury_sql)
    results = cursor.fetchall()
    for result in results:
        id = str(result[0])
        city = result[1]
        city = city.replace("市", "")
        update_sql = """update Starbucks set city = '%s' where id = '%s'""" % (city, id)
        cursor.execute(update_sql)


if __name__ == '__main__':
    delete_city_shi()
