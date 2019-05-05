import datetime
import time

import pymysql

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "hotpot")
cursor = db.cursor()


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
    inquery_sql = """select * from (select *,t.total/t.count_times*3 as avg_value from(select *,(select count(*)  from SHOP_WAITE  g where crawlTime >='%s'  and  crawlTime < '%s' and g.storeId = e.storeId and g.webque = e.webque) as count_times from (select f.*,s.storeName,s.city_level,s.city from SHOP_DETAIL s,(select d.webque,d.storeId,d.crawlTime,sum(num) total from 
    (select 0.6*waitNum num ,a.* as waitvalue from (select  storeId,waitNum,typeName,crawlTime,webque from SHOP_WAITE where crawlTime >='%s' and  crawlTime < '%s' and typeName='小桌' ) a UNION ALL
    select 0.2*waitNum num,b.* as waitvalue from (select  storeId,waitNum,typeName,crawlTime,webque from SHOP_WAITE where crawlTime >= '%s' and  crawlTime < '%s' and typeName='中桌' ) b UNION ALL
    select 0.2*waitNum num,c.* as waitvalue from (select  storeId,waitNum,typeName,crawlTime,webque from SHOP_WAITE where crawlTime >= '%s' and  crawlTime < '%s' and typeName='大桌' ) c) d group by d.storeId,d.webque) f 
where s.storeId=f.storeId and  s.crawlTime = '%s') e)t) f GROUP BY f.storeId,f.webque
    """ % (start_day, end_day, start_day, end_day, start_day, end_day, start_day, end_day, shopDetail_max_crawlTime)
    return inquery_sql


if __name__ == '__main__':
    start_day = '2019-02-10'
    end_day = '2019-02-25'
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "hotpot")
    cursor = db.cursor()
    # 获取起止时间的时间范围
    day_list = get_day_list()
    # 获取店铺详情表的最大日期
    shopDetail_max_crawlTime = get_max_crawl_time()
    data_list = []
    for i in range(len(day_list)):
        if int(i) < len(day_list) - 1:
            start_day = day_list[int(i)]
            # 16代表的是今天下午四点开始计算
            start_day = start_day + ' 16'
            end_day = day_list[int(i) + 1]
            print(start_day, end_day)
            # 格式化生成sql语句
            inquery_sql = format_sql()
            print(inquery_sql)
            cursor.execute(inquery_sql)
            results = cursor.fetchall()
            for data in results:
                storeName = data[4]
                web_queue = data[0]
                city_level = data[5]
                city = data[6]
                storeId = str(data[1])
                crawlTime = data[2].strftime("%Y-%m-%d")
                total = data[3]
                count_times = data[7]
                avg_value = data[8]
                data = [storeName, web_queue, city_level, city, storeId, crawlTime, total, count_times, avg_value]
                data_list.append(data)
    print(data_list)
    # 写入文件
    import csv
    # filename = '海底捞' + end_day + '.csv'
    filename = '海底捞' + str(int(time.time())) + '.csv'
    # filename = '海底捞' + end_day + '.xls'
    # filename = '海底捞' + str(int(time.time())) + '.xlsx'
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        head_list = ['店铺名字', '是否开启网络排队', '城市级别', '城市', '店铺ID', '抓取时间', '热力值总数', '抓取次数', '平均值']
        writer.writerow(head_list)
        for row in data_list:
            writer.writerow(row)
    import pandas as pd
    csv_data = pd.read_csv(filename,
                           engine='python')  # 发现调用pandas的read_csv()方法时，默认使用C engine作为parser engine，
    # 而当文件名中含有中文的时候，用C engine在部分情况下就会出错。所以在调用read_csv()方法时指定engine为Python就可以解决问题了。
    csv_data.to_excel(filename.replace('csv', 'xlsx'), index=False)
