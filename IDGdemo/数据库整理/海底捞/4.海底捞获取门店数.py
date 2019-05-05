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
    filename = '海底捞门店数' + str(int(time.time())) + '.csv'
    for change_day in day_list:
        sql = """SELECT storeId,storeName,city,city_level from SHOP_DETAIL WHERE storeId in (select DISTINCT storeId from SHOP_WAITE WHERE crawlTime='%s') GROUP BY storeId ;""" % change_day
        cursor.execute(sql)
        results = cursor.fetchall()
        df = pd.DataFrame(list(results))
        df['crawlTime'] = change_day
        df.to_csv(filename, mode='a', header=False, index=False)
    csv_data = pd.read_csv(filename,engine='python')  # 再去读信息
    csv_data.to_excel('海底捞门店数.xlsx', index=False)
