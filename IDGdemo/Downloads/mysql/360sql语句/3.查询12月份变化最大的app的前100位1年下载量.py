import csv
import pandas as pd
import pymysql

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "downloads")
cursor = db.cursor()
start = '2018-01-01'
end = '2019-02-27'
data_list = []
month_list = [d.strftime("%Y-%m-%d") for d in pd.date_range(start, end, freq="M")]
# month_list = ['2019-01-31']
for i, month_max_day in enumerate(month_list):
    year_month_list = month_max_day.split("-")
    month = year_month_list[1]
    year = year_month_list[0]
    sql = """select max(stat_dt),min(stat_dt) from ANDROID_SAFE_APP_DAILY where dt_type='周' and stat_dt>='%s-%s-01' and stat_dt<'%s'""" % (year,
        month, month_max_day)
    cursor.execute(sql)
    data_set = cursor.fetchone()
    start_time = data_set[1]
    end_time = data_set[0]
    if start_time:
        change_sql = """
        select b.app_name,b.category,a.* from (
	select a.*,chg/datediff('%s','%s')*30 as chg_month from ( 
	select *,(downs-f_downs) as chg from (
select app_keys,downs,(select downs from ANDROID_SAFE_APP_DAILY where dt_type='周' and stat_dt='%s' and app_keys=a.app_keys) as f_downs
				from ANDROID_SAFE_APP_DAILY a where dt_type='周' and stat_dt='%s' and app_keys in (
(select t.app_keys from(select app_keys from ANDROID_SAFE_APP_DAILY a where dt_type='周' and stat_dt='2018-12-23' order by downs desc limit 100) as t)
)  ) a )a )a left join ANDROID_SAFE_APP b on (a.app_keys=b.app_keys)
""" % (end_time, start_time, start_time, end_time)
        print(change_sql)
        cursor.execute(change_sql)
        # 提交到数据库执行
        serch_data = cursor.fetchall()
        for serch in serch_data:
            serch = list(serch)
            serch.append(start_time)
            data_list.append(serch)

filename = '100app3' + '.csv'
with open(filename, 'a+', newline='') as f:
    writer = csv.writer(f)
    for row in data_list:
        writer.writerow(row)
print(data_list)
