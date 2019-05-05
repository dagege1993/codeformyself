import csv
import time
import pymysql

last_result_list = []
fluent_results = ['name', "2018-11-16", "2018-11-17", "2018-11-21", "2018-11-22", "2018-11-23", "2018-11-24",
                  "2018-11-25",
                  "2018-11-26", "2018-11-27", "2018-11-28", "2018-11-29", "2018-11-30", "2018-12-01", "2018-12-02",
                  "2018-12-03", "2018-12-04", "2018-12-05", "2018-12-06", "2018-12-07", ]
research_times = ["2018-11-16", "2018-11-17", "2018-11-21", "2018-11-22", "2018-11-23", "2018-11-24",
                  "2018-11-25",
                  "2018-11-26", "2018-11-27", "2018-11-28", "2018-11-29", "2018-11-30", "2018-12-01", "2018-12-02",
                  "2018-12-03", "2018-12-04", "2018-12-05", "2018-12-06", "2018-12-07", ]


def reader_csv():
    csv_reader = csv.reader(open("111.csv"))
    for i, row in enumerate(csv_reader):
        if i > 0:
            course_name = row[0]
            times = research_times
            research_result = get_price_from_mysql(course_name, times)
            row[1:] = research_result

        last_result_list.append(row)  # 全部写完后在一起写入

    filename = 'studyUsersCount' + '.csv'
    with open(filename, 'a+', newline='') as f:
        writer = csv.writer(f)
        for row in last_result_list:
            writer.writerow(row)


def get_price_from_mysql(course_name, times):
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "fluent")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    research_result = []
    for Timestamp in times:
        sql = """select studyUsersCount from COURSE where translatedTitle='%s' and times='%s';""" % (
            course_name, Timestamp)
        cursor.execute(sql)
        db.commit()
        # 有一条记录
        results = cursor.fetchone()
        if results:
            result = str(results[0])
        else:
            result = '0'
        research_result.append(result)
    db.close()
    return research_result


if __name__ == '__main__':
    start_time = time.time()
    reader_csv()
    print(time.time() - start_time)
# 优化了查询看写入需要多长时间
