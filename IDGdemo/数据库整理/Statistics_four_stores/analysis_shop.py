#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
import os

import pandas as pd
import time
import pymysql

check_dict_list = [
    {'company': '海底捞',
     'category': '门店数',
     'type': '总数',
     'database': 'hotpot',
     'table': 'SHOP_DETAIL',
     'param': 'crawlTime',
     'open_or_not': ''
     },
    {'company': '星巴克',
     'category': '门店数',
     'type': '总数',
     'database': 'shops',
     'table': 'Starbucks',
     'param': 'crawlTime',
     'open_or_not': ''
     },
    {'company': '永辉超市',
     'category': '门店数',
     'type': '总数',
     'database': 'shops',
     'table': 'YongHui',
     'param': 'crawlTime',
     'open_or_not': 'open_or_not'
     },
    {'company': '瑞幸咖啡',
     'category': '门店数',
     'type': '总数',
     'database': 'shops',
     'table': 'Luckin',
     'param': 'crawlTime',
     'open_or_not': 'open'
     }
]


# 获取当天日期的城市级别以及城市级别店铺数
def get_payload(check_dict, today_times):
    database = check_dict.get('database')
    table = check_dict.get('table')
    company = check_dict.get('company')
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", database)
    cursor = db.cursor()
    open_or_not = check_dict.get('open_or_not')
    if open_or_not:
        inquery_sql = """select count(*),crawlTime,city_level,%s from %s WHERE crawlTime = '%s' GROUP BY crawlTime,city_level,%s;""" % (
            open_or_not, table, today_times, open_or_not)
        print(inquery_sql)
        cursor.execute(inquery_sql)
        cursor.execute(inquery_sql)
        results = cursor.fetchall()
        df = pd.DataFrame(list(results))  # 转换成DataFrame格式
    else:
        inquery_sql = """select count(*),crawlTime,city_level from %s WHERE crawlTime = '%s' GROUP BY crawlTime,city_level;""" % (
            table, today_times)
        print(inquery_sql)
        cursor.execute(inquery_sql)
        results = cursor.fetchall()
        df = pd.DataFrame(list(results))  # 转换成DataFrame格式
        df['open_or_not'] = 1  # 这里门店是全部开业

    df['city'] = company  # 给dataframe增加一列
    print(df)
    # for result in results:
    return df


# 获取起止日期,返回一个日期字符串列表
def get_day_list(start_day, end_day):
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
    # 这是按天配置的
    # today_time = time.localtime(time.time())
    # today_times = time.strftime("%Y-%m-%d", today_time)
    # print('日期%s' % today_times)
    # # today_times = '2019-01-24'
    # for check_dict in check_dict_list:
    #     df_data = get_payload(check_dict,today_times)
    #     df_data.to_csv('excel_output.csv', mode='a', header=False, encoding="gbk", index=False)
    # # 最后再把文件转为xlsx,是为了利用可以追加写入csv
    # csv_data = pd.read_csv('excel_output.csv', encoding="gbk")  # 再去读信息
    # csv_data.to_excel('excel_output.xlsx', encoding="utf-8", index=False)  # index=False不保留列名，header设置好像会替掉第一列的内容，:指定列名行，默认0，即取第一行

    # 如果想获取一段时间范围内的
    start_day = '2019-01-24'
    end_day = datetime.date.today()
    end_day = end_day.strftime("%Y-%m-%d")  # 格式化为字符串
    day_list = get_day_list(start_day, end_day)
    for day in day_list:
        for check_dict in check_dict_list:
            df_data = get_payload(check_dict, day)
            df_data.to_csv('shops.csv', mode='a', header=False, encoding="gbk", index=False)
    # 最后再把文件转为xlsx,是为了利用可以追加写入csv
    csv_data = pd.read_csv('shops.csv', encoding="gbk")  # 再去读信息
    csv_data.to_excel('shops.xlsx', encoding="utf-8",
                      index=False)  # index=False不保留列名，header设置好像会替掉第一列的内容，:指定列名行，默认0，即取第一行
    os.remove('shops.csv')
