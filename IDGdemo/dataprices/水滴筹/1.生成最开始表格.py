import copy
import csv
import pymysql
from dataprices.config_log import Config

conf = Config()
logger = conf.getLog()

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "water_safe")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
sql = """select insuranceTitle,years,months,schedule,joinPerson from PLANS2;"""
cursor.execute(sql)
db.commit()
# 获取所有记录列表
results = cursor.fetchall()
time_list = []
year_list = set()
month_list = set()
number_list = set()
test_result = set()
plans_list = set()
last_result_list = []
# 拿到每一列的保险计划名字,年份,月份,第几期,参加的人数
for result in results:
    print(result)
    result = list(result)
    year_list.add(result[1])
    month_list.add(result[2])
    number_list.add(result[3])
    plans_list.add(result[0])
print(year_list)
print(month_list)
print(number_list)
# 生成列名
for year in year_list:
    for month in month_list:
        for number in number_list:
            times = str(year) + '年/' + str(month) + '月/' + '第' + str(number) + '次公示'
            print(times)
            time_list.append(times)  # 为了拼凑这个时间参数,这个就是写入CSV的头信息
head_list = copy.deepcopy(time_list)  # 对象 time_list
head_list.insert(0, 'names')

# 五个保险计划表
for plan in plans_list:
    time_list.insert(0, plan)
    last_result_list.append(time_list)
    # 把时间列表归零
    time_list = head_list[1:]
filename = 'safe0218' + '.csv'
with open(filename, 'a+', newline='') as f:
    writer = csv.writer(f)
    # 先写入columns_name
    writer.writerow(head_list)
    for row in last_result_list:
        writer.writerow(row)

# logger.info(last_result_list)
