import time

from pencilnews_dayup import first_requests
from selenium_daily import main_progress

SECOND_DAY = 24 * 60 * 60


def delta_seconds():
    from datetime import datetime
    cur_time = datetime.now()
    des_time = cur_time.replace(hour=0, minute=1, second=0, microsecond=0)
    # 这里添加时间 replace()= Return a new datetime with new values for the specified fields.返回一个替换指定日期字段的新date对象
    delta = des_time - cur_time
    skip_seconds = delta.total_seconds() % SECOND_DAY  # total_seconds()是获取两个时间之间的总差
    print("Must sleep %d seconds" % skip_seconds)
    return skip_seconds


while True:
    s = delta_seconds()
    time.sleep(s)
    print("work it!")  # 这里可以替换成作业
    main_progress()
    first_requests()  # 启动两个抓取函数