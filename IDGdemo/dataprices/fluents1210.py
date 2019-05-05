import csv
import pymysql

from dataprices.config_log import Config

conf = Config()
logger = conf.getLog()

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "fluent")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
sql = """select ID,translatedTitle,diamondPrice,studyUsersCount,times from COURSE where ID !=0;"""
cursor.execute(sql)
db.commit()
# 获取所有记录列表
results = cursor.fetchall()
last_result_list = []
test_result = set()
fluent_results = ['ID', 'name', "2018-11-16", "2018-11-17", "2018-11-21", "2018-11-22", "2018-11-23", "2018-11-24",
                  "2018-11-25",
                  "2018-11-26", "2018-11-27", "2018-11-28", "2018-11-29", "2018-11-30", "2018-12-01", "2018-12-02",
                  "2018-12-03", "2018-12-04", "2018-12-05", "2018-12-06", "2018-12-07", ]
for result in results:
    # print(result)
    result = list(result)
    result[4] = result[4].strftime('%Y-%m-%d')
    ID = result[0]
    name = result[1]
    fluent_result = ["2018-11-16", "2018-11-17", "2018-11-21", "2018-11-22", "2018-11-23", "2018-11-24", "2018-11-25",
                     "2018-11-26", "2018-11-27", "2018-11-28", "2018-11-29", "2018-11-30", "2018-12-01", "2018-12-02",
                     "2018-12-03", "2018-12-04", "2018-12-05", "2018-12-06", "2018-12-07", ]
    if ID in test_result:
        pass
    else:
        fluent_result.insert(0, ID)
        fluent_result.insert(1, name)
        test_result.add(ID)
        last_result_list.append(fluent_result)
        print(fluent_result)

filename = '1212' + '.csv'
with open(filename, 'a+', newline='') as f:
    writer = csv.writer(f)
    # 先写入columns_name
    writer.writerow(fluent_results)
    for row in last_result_list:
        writer.writerow(row)

logger.info(last_result_list)
