#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pandas as pd
import time
import pymysql

check_dict_list = [
    {'company': '海底捞',
     'category': '门店数',
     'type': '总数',
     'database': 'hotpot',
     'table': 'SHOP_DETAIL',
     'param': 'crawlTime'
     },
    {'company': '星巴克',
     'category': '门店数',
     'type': '总数',
     'database': 'shops',
     'table': 'Starbucks',
     'param': 'crawlTime'
     },
    {'company': '永辉',
     'category': '门店数',
     'type': '总数',
     'database': 'shops',
     'table': 'YongHui',
     'param': 'crawlTime'
     },
    {'company': '瑞幸咖啡',
     'category': '门店数',
     'type': '总数',
     'database': 'shops',
     'table': 'Luckin',
     'param': 'crawlTime'
     }
]


# 获取当天日期的城市级别以及城市级别店铺数
def get_payload(check_dict):
    database = check_dict.get('database')
    table = check_dict.get('table')
    company = check_dict.get('company')
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", database)
    cursor = db.cursor()
    inquery_sql = """select count(*),crawlTime,city_level from %s WHERE crawlTime = '%s' GROUP BY crawlTime,city_level;""" % (
        table, today_times)
    print(inquery_sql)
    cursor.execute(inquery_sql)
    results = cursor.fetchall()
    df = pd.DataFrame(list(results))  # 转换成DataFrame格式
    df['city'] = company  # 给dataframe增加一列
    print(df)
    # for result in results:
    return df


if __name__ == '__main__':
    today_time = time.localtime(time.time())
    today_times = time.strftime("%Y-%m-%d", today_time)
    print('日期%s' % today_times)

    for check_dict in check_dict_list:
        df_data = get_payload(check_dict)
        # df_data.to_csv('excel_output.csv', mode='a', header=False, encoding="utf-8")
        df_data.to_csv('excel_output.csv', mode='a', header=False, encoding="gbk", index=False)

    # 最后再把文件转为xlsx,是为了利用可以追加写入csv
    csv = pd.read_csv('excel_output.csv', encoding="gbk")
    header = ['门店数', '日期', '城市等级', '公司名称']
    csv.to_excel('excel_output.xlsx', encoding="utf-8", index=False, header=header)  # index=False不保留列名
