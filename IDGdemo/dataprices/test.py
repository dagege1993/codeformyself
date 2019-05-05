# encoding=utf-8
import csv
import time

import pandas as pd
import datetime

head_lists = ['name', "2018-11-16", "2018-11-17", "2018-11-21", "2018-11-22", "2018-11-23", "2018-11-24", "2018-11-25",
              "2018-11-26", "2018-11-27", "2018-11-28", "2018-11-29", "2018-11-30", "2018-12-01", "2018-12-02",
              "2018-12-03", "2018-12-04", "2018-12-05", "2018-12-06", "2018-12-07"]

course_stats = ['吃瓜英语怎么说', '2018-11-16', '2018-11-17', '2018-11-21', '2018-11-22', '2018-11-23', '2018-11-24',
                '2018-11-25', '2018-11-26', '2018-11-27', '2018-11-28', '2018-11-29', '2018-11-30', '2018-12-01',
                '2018-12-02', '2018-12-03', '2018-12-04', '2018-12-05', '2018-12-06', '2018-12-07']

# filename = str(int(time.time())) + '.xlsx'
# with open(filename, 'w', newline='') as f:
#     writer = csv.writer(f)
#     header = head_lists
#     writer.writerow(header)
#     writer.writerows(course_stats)
list1 = ['吃瓜英语怎么说', 'b']
list2 = [['apple', 'banana', 'grapes'], ['cheery']]
with open('0706.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    header = "col1", "col2"
    # writer.writerow(header)
    writer.writerow(list1)
    writer.writerow(header)
    #     writer.writerows(course_stats)

