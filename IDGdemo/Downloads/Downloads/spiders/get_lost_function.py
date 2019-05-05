import pymysql

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "downloads")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()


def get_lost_item(sql):
    # print(sql)
    cursor.execute(sql)
    results = cursor.fetchone()

    # print(results)
    return results


def get_app_id(sql):
    cursor.execute(sql)
    results = cursor.fetchone()
    # print(results)
    return results[0]


def get_lost_app_keys(sql):
    app_key_list = []
    cursor.execute(sql)
    results = cursor.fetchall()
    for result in results:
        if result:
            app_key_list.append(result[0])
    return app_key_list


# 查询拿到缺失的app_pkg
def get_lost_app_pkg(sql):
    cursor.execute(sql)
    results = cursor.fetchone()
    if results:
        return results[0]
