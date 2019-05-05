import pymysql
import datetime

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "fluent")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()


def get_max_course(sql):
    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
    # 使用 fetchone() 方法获取一条数据
    datas = cursor.fetchall()
    for data in datas:
        print('data', data)
        datas = data[0]
    return datas


def week_get():
    day_dict = {}
    begin = datetime.date(2018, 12, 17)
    end = datetime.date(2018, 12, 23)

    for i in range((end - begin).days + 1):
        day = begin + datetime.timedelta(days=i)
        sql = """select count(*) from COURSE WHERE  times = '%s';""" % day
        # print(day)
        data_len = get_max_course(sql)
        day_dict[str(day)] = data_len

    return day_dict


if __name__ == '__main__':
    import operator
    results = week_get()
    print(results)
    sorted_x = sorted(results.items(), key=operator.itemgetter(1), reverse=True)
    print(sorted_x)
