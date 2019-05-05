import sys
import os
import time

from scrapy.cmdline import execute

from mysql_couse import un_get_id

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

SECOND_DAY = 24 * 60 * 60


def delta_seconds():
    from datetime import datetime
    cur_time = datetime.now()
    des_time = cur_time.replace(hour=1, minute=1, second=0, microsecond=0)
    # 这里添加时间 replace()= Return a new datetime with new values for the specified fields.返回一个替换指定日期字段的新date对象
    delta = des_time - cur_time
    skip_seconds = delta.total_seconds() % SECOND_DAY  # total_seconds()是获取两个时间之间的总差
    print("Must sleep %d seconds" % skip_seconds)
    return skip_seconds


localtime = time.localtime(time.time())
str_time = time.strftime("%Y-%m-%d %H:%M", localtime)
if __name__ == '__main__':
    print('当前抓取时间是', str_time)
    if len(un_get_id()) > 0:  # 然后判断是否有缺失
        print('当前还有遗漏课程数据')
        execute(["scrapy", "crawl", "Course_mysql", ])
    else:
        print('当日课程已经抓取完毕')
