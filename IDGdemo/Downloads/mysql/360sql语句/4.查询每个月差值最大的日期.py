import csv
import pymysql

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "downloads")
cursor = db.cursor()
month_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
data_list = []
for i, month in enumerate(month_list):

    if i < len(month_list) - 1:
        sql = """select max(stat_dt),min(stat_dt) from ANDROID_SAFE_APP_DAILY where dt_type='周' and stat_dt>='2018-%s-01' and stat_dt<'2018-%s-01'""" % (
            month, month_list[i + 1])
        cursor.execute(sql)
        data_set = cursor.fetchone()
        start_time = data_set[1]
        end_time = data_set[0]
        if start_time:
            change_sql = """
            select category,count(0) app_num, sum(chg_month) chg_month from (
    select b.app_name,b.category,a.*,chg/datediff('%s','%s')*30 as chg_month from (
    select *,(downs-f_downs) as chg from (
            select app_keys,downs,(select downs from ANDROID_SAFE_APP_DAILY where dt_type='周' and stat_dt='%s' and app_keys=a.app_keys) as f_downs
                from ANDROID_SAFE_APP_DAILY a where dt_type='周' and stat_dt='%s'
    ) a
    where f_downs is not null  
    ) a 
    left join ANDROID_SAFE_APP b on (a.app_keys=b.app_keys)
    ) a group by category
            """ % (end_time, start_time, start_time, end_time)
            print(change_sql)
            cursor.execute(change_sql)
            # 提交到数据库执行
            serch_data = cursor.fetchall()
            for serch in serch_data:
                serch = list(serch)
                serch.append(start_time)
                data_list.append(serch)

filename = 'change' + '.csv'
with open(filename, 'a+', newline='') as f:
    writer = csv.writer(f)
    for row in data_list:
        writer.writerow(row)
print(data_list)
