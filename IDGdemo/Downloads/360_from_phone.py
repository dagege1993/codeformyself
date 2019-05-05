# encoding=utf-8
import os
import sys
import time
from scrapy.cmdline import execute


# 添加系统环境变量
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
localtime = time.localtime(time.time())
str_time = time.strftime("%Y-%m-%d %H:%M", localtime)
print(str_time)
execute(["scrapy", "crawl", "360_from_phone", ])
end_time = time.strftime("%Y-%m-%d %H:%M", localtime)
print(end_time)