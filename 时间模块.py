import datetime
import time

startTime = '2016-07-06 '
endTime = '2016-07-12 '
# startTime = '2016-07-06 '
# endTime = '2016-07-06 '
startTime = datetime.datetime.strptime(startTime, '%Y-%m-%d ')
endTime = datetime.datetime.strptime(endTime, '%Y-%m-%d ')
# print(type(startTime), endTime)
time_difference = endTime - startTime
# print(type(time_difference))
# print(startTime.strftime('%Y-%m-%d'))
str_time = time_difference.days
# print(str_time)

# if str_time > 0:
#     print('时间差距大于1天')
#     for i in range(1, str_time + 1):
#         endTime = startTime + datetime.timedelta(days=1)
#         startTime = endTime
#         print(endTime)
# if str_time == 0:
#     print('查询时间为当天')
#
# timestamp = time.time()
# print(str(int(timestamp)))


for i in range(1, 5):
    startTime = startTime
    endTime = startTime + datetime.timedelta(hours=6)

    print(startTime, endTime)
    startTime = endTime
#
# list1 = [
#     {
#         "customerNum": "10021014679680366408447",
#         "completeTime": "2016-07-12 15:43:13",
#         "orderAmount": "0.01",
#         "orderNum": "10021014683093339018474",
#         "refundTime": "2016-07-12 15:43:13",
#         "memberNum": "10001214641783052104486",
#         "status": "REFUND"},
#     {
#         "customerNum": "10021014679680366408447",
#         "completeTime": "2016-07-08 16:54:08",
#         "orderAmount": "0.01",
#         "orderNum": "10021014679680366408447",
#         "requestNum": "1467968309017215",
#         "memberNum": "10001214641783052104486",
#         "status": "SUCCESS"
#     },
#     {
#         "customerNum": "10021014679680366408447",
#         "completeTime": "2016-07-08 16:54:08",
#         "orderAmount": "0.01",
#         "orderNum": "10021014679487197128438",
#         "requestNum": "1467948989004654",
#         "memberNum": "10001214641783052104486",
#         "status": "INIT"
#     }
# ]
# list2 = []

import random

# a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# b = random.sample(a, 1)
# print(b)
# for j in range(1, 334):
#     for i in list1:
#         list2.append(i)
#
# print(len(list2), list2)
# startTime = time.time()
# print(datetime.datetime.strptime(startTime, '%Y-%m-%d '))

starttime = time.time()
# 本地时间戳改时间
st = time.localtime()

print(1, time.strftime('%Y-%m-%d %H:%M:%S', st))

start_time = datetime.datetime.now()

end_time = datetime.datetime.now()
print('结束时间', (end_time - start_time).seconds)

# long running
# do something other
endtime = time.time()
linutime = time.localtime(endtime - starttime)
print(time.strftime("%Y-%m-%d %H:%M:%S", linutime))


# 输入一个日期范围,返回的是每个月的起始日期和结束日期

def get_month_day():
    import calendar
    import time
    day_now = time.localtime()
    day_begin = '%d-%02d-01' % (day_now.tm_year, day_now.tm_mon)  # 月初肯定是1号
    wday, monthRange = calendar.monthrange(day_now.tm_year, day_now.tm_mon)  # 得到本月的天数 第一返回为月第一日为星期几（0-6）, 第二返回为此月天数
    day_end = '%d-%02d-%02d' % (day_now.tm_year, day_now.tm_mon, monthRange)
    print('月初日期为：', day_begin, '月末日期为：', day_end)


def get_date_list(start, end):
    import pandas as pd
    date_list = [d.strftime("%Y-%m-%d") for d in pd.date_range(start, end, freq="M")]
    print(date_list)
    return date_list


if __name__ == '__main__':
    # get_month_day()
    start = '2017-01-01'
    end = '2019-01-30'
    get_date_list(start, end)
