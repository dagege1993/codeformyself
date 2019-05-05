import json
import time

import pymysql
import requests


# 主函数
def home_page():
    url = "https://api.shuidihuzhu.com/api/hz/order/v3/allocationSummary"
    headers = {'cache-control': "no-cache", }
    response = requests.request("GET", url, headers=headers)
    print(response.text)
    storage(response)


# 存储数据函数
def storage(response):
    response_text = json.loads(response.text)
    print(response_text)
    data = response_text.get('data')
    total_member = int(data.get('totalMember'))
    total_amount = int(data.get('totalAllocationAmountInYuan'))
    localtime = time.localtime(time.time())
    str_time = time.strftime("%Y-%m-%d", localtime)
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "water_safe")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # SQL 插入语句
    sql = """INSERT INTO HOME(totalMember,totalAllocationAmountInYuan,times)VALUES  ("%d","%d","%s")""" % (
        total_member, total_amount, str_time)

    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
    # 关闭数据库连接
    db.close()


if __name__ == '__main__':
    home_page()
