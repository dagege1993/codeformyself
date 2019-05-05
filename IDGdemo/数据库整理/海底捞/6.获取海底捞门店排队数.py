import datetime
import time
import pandas as pd
import pymysql
import csv

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "hotpot")
cursor = db.cursor()


# 获取一个店铺ID对应的城市信息的表
def storeId_city():
    sql = """select storeId,storeName,city,city_level from SHOP_DETAIL  GROUP BY storeId  """
    cursor.execute(sql)
    data_list = cursor.fetchall()
    df_data = pd.DataFrame(list(data_list))  # 转换成DataFrame格式
    # dataframe便利行,loc做数据切分用的
    city_Id_dict = {}
    for indexs in df_data.index:
        id_city = df_data.loc[indexs].values[0:]
        city_Id_dict[id_city[0]] = list(id_city[1:])

    print(city_Id_dict)
    return city_Id_dict


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


# 获取店铺详情页最大日期
def get_max_crawl_time():
    max_day_sql = """select DISTINCT crawlTime from SHOP_DETAIL ORDER BY crawlTime desc"""
    cursor.execute(max_day_sql)
    results = cursor.fetchone()
    result = results[0]
    return result


def format_sql():
    inquery_sql = """select * from SHOP_WAITE  WHERE  crawlTime = '%s' """ % day
    return inquery_sql


if __name__ == '__main__':
    start_day = '2019-01-24'
    end_day = '2019-02-25'
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "hotpot")
    cursor = db.cursor()
    id_city_dict = storeId_city()
    # 获取起止时间的时间范围
    day_list = get_day_list()
    # 获取店铺详情表的最大日期
    shopDetail_max_crawlTime = get_max_crawl_time()
    # data_list = []
    news_list = []  # 存储一天的数据
    not_data_list = ['2019-01-31', '2019-02-14', '2019-02-16'] # 不抓取列表,因为有服务器卡顿之类的原因,某些日期的数据是不能用
    for i in range(len(day_list)):
        if int(i) < len(day_list) - 1:
            start_day = day_list[int(i)]
            if start_day not in not_data_list:  # 如果不是那几个时间
                for i in [12, 18, 19]:
                    day = start_day + ' ' + str(i)
                    inquery_sql = format_sql()
                    # print(inquery_sql)
                    cursor.execute(inquery_sql)
                    results = cursor.fetchall()
                    # 拿到storeid后去重,然后自己做建立一个键值对的表
                    df_data = pd.DataFrame(list(results))  # 转换成DataFrame格式
                    for indexs in df_data.index:
                        id_city = df_data.loc[indexs].values[0:]
                        # print(id_city)
                        storeId = id_city[0]
                        detail_list = id_city_dict.get(storeId)
                        new_list = list(id_city) + (detail_list)  # 拼接成功的list
                        news_list.append(new_list)
                        # print(new_list)

    # print(news_list)
    # 写入文件

    filename = '海底捞排队人数' + str(int(time.time())) + '.csv'
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        head_list = ['店铺ID', '排队桌数', '桌面类型', '抓取时间', '是否开启网络排队', '抓取时间', '城市', '城市级别']
        writer.writerow(head_list)
        for row in news_list:
            writer.writerow(row)
    import pandas as pd

    csv_data = pd.read_csv(filename,
                           engine='python')  # 发现调用pandas的read_csv()方法时，默认使用C engine作为parser engine，
    # 而当文件名中含有中文的时候，用C engine在部分情况下就会出错。所以在调用read_csv()方法时指定engine为Python就可以解决问题了。
    csv_data.to_excel(filename.replace('csv', 'xlsx'), index=False)
