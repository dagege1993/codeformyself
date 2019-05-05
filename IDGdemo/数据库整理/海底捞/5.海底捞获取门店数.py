import datetime
import time

import pandas as pd

import pymysql


def get_day_list():
    day_list = []
    datestart = datetime.datetime.strptime(start_day, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(end_day, '%Y-%m-%d')
    d = datestart
    delta = datetime.timedelta(days=1)
    while d <= dateend:
        # print(d.strftime("%Y-%m-%d"))
        day = d.strftime("%Y-%m-%d")
        day_list.append(day)
        d += delta
    return day_list


if __name__ == '__main__':
    start_day = '2019-01-24'
    end_day = '2019-02-10'
    # end_day = '2019-01-26'
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "hotpot")
    cursor = db.cursor()
    # 获取起止时间的时间范围
    day_list = get_day_list()
    data_list = []
    for change_day in day_list:
        sql = """SELECT storeId,storeName,city,city_level from SHOP_DETAIL WHERE storeId in (select DISTINCT storeId from SHOP_WAITE WHERE crawlTime='%s') GROUP BY storeId ;""" % change_day
        cursor.execute(sql)
        results = cursor.fetchall()
        for data in results:
            storeName = data[1]
            city_level = data[3]
            city = data[2]
            storeId = str(data[0])
            crawlTime = change_day
            data = [storeName, city_level, city, storeId, crawlTime ]
            data_list.append(data)
    print(data_list)
    # 写入文件
    import csv
    filename = '海底捞门店数' + str(int(time.time())) + '.csv'
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        head_list = ['店铺名字', '城市级别', '城市', '店铺ID', '抓取时间']
        writer.writerow(head_list)
        for row in data_list:
            writer.writerow(row)
    import pandas as pd
    csv_data = pd.read_csv(filename,
                           engine='python')  # 发现调用pandas的read_csv()方法时，默认使用C engine作为parser engine，
    # 而当文件名中含有中文的时候，用C engine在部分情况下就会出错。所以在调用read_csv()方法时指定engine为Python就可以解决问题了。
    csv_data.to_excel(filename.replace('csv', 'xlsx'), index=False)
