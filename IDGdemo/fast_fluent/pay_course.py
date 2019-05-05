import json
import time

import pymysql
import requests
from fast_fluent.starturl_list import start_url_list, get_token


def course():
    url = "https://apineo.llsapp.com/api/v1/curriculums/3-cccccccccccccccccccccccc"
    querystring = {"appVer": "6", "clientAppVersion": "5.", "token": "6ff2fce0cf5b0136652b0a5864605265",
                   "deviceId": "354730011088642", "sDeviceId": "354730010301566", "appId": "lls",
                   "orderSourceType": "1"}
    payload = ""
    headers = {
        'cache-control': "no-cache",
        'Postman-Token': "ad36915a-dc71-43ee-a819-779ddf840eb9"
    }
    querystring['token'] = get_token()
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    print(response.text)
    response.encoding = "utf-8"  # 指定编码格式,防止乱码
    response_text = json.loads(response.text)
    storage(response_text)


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


# 入库
def storage(response_text):
    print('当前请求的用户详情页', response_text)
    id = response_text.get("id")
    diamondPrice = response_text.get("priceInCents") / 100 * 30
    translatedTitle = '懂你英语'
    studyUsersCount = response_text.get("coreCourse").get('paidStudents')
    localTime = time.localtime(time.time())
    strTime = time.strftime("%Y-%m-%d", localTime)
    print("当前入库的数据为:", id, diamondPrice, translatedTitle, studyUsersCount)
    # 打开数据库连接
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "fluent")

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # SQL 插入语句
    sql = """INSERT INTO COURSE(ID,
             diamondPrice, studyUsersCount, translatedTitle,times)
           VALUES  ("%s","%d","%d","%s","%s")""" % (id, diamondPrice, studyUsersCount, translatedTitle, strTime)

    try:
        # 执行sql语句
        print(sql)
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
    # 执行sql语句
    # cursor.execute(sql)
    # # 提交到数据库执行
    # db.commit()
    # 关闭数据库连接
    db.close()


# while True:
#     s = delta_seconds()
#     time.sleep(s)
#     print("work it!")  # 这里可以替换成作业
#     course()

if __name__ == '__main__':
    course()
