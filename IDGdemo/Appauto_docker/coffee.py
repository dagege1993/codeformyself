import datetime
import os
import pandas as pd
import time
import pymysql
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from clean_storage import cleaning
from config_logs import Config
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

conf = Config()
logger = conf.getLog()

# 这是dockerappnium,先用docker_appnium跑着
# cap = {
#     "platformName": "Android",
#     "platformVersion": "4.4.2",
#     "deviceName": "192.168.103.167:5555",
#     "appPackage": "com.lucky.luckyclient",
#     "appActivity": "com.lucky.luckyclient.splash.splash.SplashActivity",
#     "noReset": True
# }
# docker的虚拟IP
# driver = webdriver.Remote("http://192.168.99.100:4723/wd/hub", cap)

# 这是docker_appnium
cap = {
    "platformName": "Android",
    "platformVersion": "4.4.2",
    "deviceName": "127.0.0.1:62001",
    "appPackage": "com.lucky.luckyclient",
    "appActivity": "com.lucky.luckyclient.splash.splash.SplashActivity",
    "noReset": True
}
driver = webdriver.Remote("http://192.168.103.104:4723/wd/hub", cap)


def get_size():
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    return (x, y)


# 获取屏幕大小,以及确定下滑的距离
l = get_size()
x1 = int(l[0] * 0.5)
y1 = int(l[1] * 0.75)
y2 = int(l[1] * 0.25)


# 前面的准备工作
def front():
    # 点击不切换新版本
    time.sleep(2)
    # appnium的点击办法
    time.sleep(30)
    # 叉掉升级
    e11 = driver.find_element_by_xpath(
        "//android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.RelativeLayout[1]/android.widget.LinearLayout[1]/android.widget.ImageView[2]")
    e11.click()
    e12 = driver.find_element_by_xpath(
        "//android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[2]/android.widget.Button[1]")
    e12.click()
    if "无响应" in driver.page_source:
        return 0
    else:
        return 1


# 滑到最后,为了展示全部的城市
def get_source():
    # 1-21只能是到南京,定位元素是20,下面的元素又不一样
    logger.info('当前是城市列表页第一页')
    for i in range(2, 21):
        logger.info('当前是第%s页' % i)
        try:
            time.sleep(0.5)
            el3 = driver.find_element_by_xpath(
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout[2]/android.widget.ListView/android.widget.LinearLayout[" + str(
                    i) + "]/android.widget.TextView")
            time.sleep(1.5)
            city = el3.text
            logger.info('当前抓取城市%s' % city)
            el3.click()
        except Exception as e:
            logger.info(e)
        data = driver.page_source
        logger.info('第一次%s' % data)
        # 证明有数据
        if 'No' in data:
            cleaning(data, city)
            # 滑动操作
            time.sleep(0.8)
            while True:
                if '已经全部加载完成' in driver.page_source:
                    break
                driver.swipe(x1, y1, x1, y2)  # appnium的滑动函数
                time.sleep(1.0)
                data = driver.page_source
                logger.info('第二次%s' % data)
                cleaning(data, city)

        # 点击进去没有数据,就退出来
        if '抱歉' in data:
            # 滑到最后,得点击退出来
            pass
        # 最后都要点击退出,然后重新进入
        if WebDriverWait(driver, 5).until(lambda x: x.find_element_by_id("com.lucky.luckyclient:id/iv_back")):
            el1 = driver.find_element_by_id("com.lucky.luckyclient:id/iv_back")
            time.sleep(1)
            el1.click()
            logger.info('当前城市抓取完毕,退出当前城市')
        # 点击切换城市
        if WebDriverWait(driver, 5).until(lambda x: x.find_element_by_id("com.lucky.luckyclient:id/confirm_btn")):
            el2 = driver.find_element_by_id("com.lucky.luckyclient:id/confirm_btn")
            time.sleep(1)
            el2.click()
            logger.info('切换城市')
    logger.info('当前是城市列表页最后页')
    # 这里是滑到最后面去处理最后面的城市
    for i in range(1, 20):
        logger.info('当前是第%s页' % i)
        try:
            driver.swipe(x1, y1, x1, y2)  # appnium的滑动函数
            driver.swipe(x1, y1, x1, y2)  # appnium的滑动函数
            time.sleep(1)
            el3 = driver.find_element_by_xpath(
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout[2]/android.widget.ListView/android.widget.LinearLayout[" + str(
                    i) + "]/android.widget.TextView")
            time.sleep(0.5)
            city = el3.text
            logger.info('当前抓取城市%s' % city)
            time.sleep(1)
            el3.click()
        except Exception as e:
            logger.info(e)
        data = driver.page_source
        logger.info('第一次%s' % data)
        # 证明有数据
        if 'No' in data:
            cleaning(data, city)
            # 滑动操作
            time.sleep(0.8)
            while True:
                if '已经全部加载完成' in driver.page_source:
                    break
                driver.swipe(x1, y1, x1, y2)  # appnium的滑动函数
                time.sleep(1.0)
                data = driver.page_source
                logger.info('第一次以后的数据%s' % data)
                cleaning(data, city)
        # 点击进去没有数据,就退出来
        if '抱歉' in data:
            # 滑到最后,得点击退出来
            pass
        # 最后都要点击退出,然后重新进入
        if WebDriverWait(driver, 5).until(lambda x: x.find_element_by_id("com.lucky.luckyclient:id/iv_back")):
            el1 = driver.find_element_by_id("com.lucky.luckyclient:id/iv_back")
            time.sleep(1)
            el1.click()
            logger.info('当前城市抓取完毕,退出当前城市')
        # 点击切换城市
        if WebDriverWait(driver, 5).until(lambda x: x.find_element_by_id("com.lucky.luckyclient:id/confirm_btn")):
            el2 = driver.find_element_by_id("com.lucky.luckyclient:id/confirm_btn")
            time.sleep(1)
            el2.click()
            logger.info('切换城市')
    logger.info('当前是城市列表页第中间页')
    # 这里来处理中间城市,区别就是这里只要划一下
    for i in range(2, 18):
        logger.info('当前是第%s页' % i)
        try:
            driver.swipe(x1, y1, x1, y2)  # appnium的滑动函数
            # driver.swipe(240, 600, 240, 200)  # appnium的滑动函数
            time.sleep(1)
            el3 = driver.find_element_by_xpath(
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout[2]/android.widget.ListView/android.widget.LinearLayout[" + str(
                    i) + "]/android.widget.TextView")
            time.sleep(0.5)
            city = el3.text
            logger.info('当前抓取城市%s' % city)
            time.sleep(1)
            el3.click()
        except Exception as e:
            logger.info(e)
        data = driver.page_source
        logger.info('第一次%s' % data)
        # 证明有数据
        if 'No' in data:
            cleaning(data, city)
            # 滑动操作
            time.sleep(0.8)
            while True:
                if '已经全部加载完成' in driver.page_source:
                    break
                driver.swipe(x1, y1, x1, y2)  # appnium的滑动函数
                time.sleep(1.0)
                data = driver.page_source
                logger.info('第一次以后的数据%s' % data)
                cleaning(data, city)
        # 点击进去没有数据,就退出来
        if '抱歉' in data:
            # 滑到最后,得点击退出来
            pass
        # 最后都要点击退出,然后重新进入
        if WebDriverWait(driver, 5).until(lambda x: x.find_element_by_id("com.lucky.luckyclient:id/iv_back")):
            el1 = driver.find_element_by_id("com.lucky.luckyclient:id/iv_back")
            time.sleep(1)
            el1.click()
            logger.info('当前城市抓取完毕,退出当前城市')
        # 点击切换城市
        if WebDriverWait(driver, 5).until(lambda x: x.find_element_by_id("com.lucky.luckyclient:id/confirm_btn")):
            el2 = driver.find_element_by_id("com.lucky.luckyclient:id/confirm_btn")
            time.sleep(1)
            el2.click()
            logger.info('切换城市')


def sed_email(key):
    import smtplib
    from email.header import Header
    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = "156350439@qq.com"  # 用户名
    mail_pass = "anqqfdztzgascbde"  # 口令,QQ邮箱是输入授权码，在qq邮箱设置 里用验证过的手机发送短信获得，不含空格
    sender = '156350439@qq.com'
    receivers = ['156350439@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    msg = MIMEMultipart()
    msg['From'] = Header("156350439@qq.com", 'utf-8')  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
    msg['To'] = Header("156350439@qq.com", 'utf-8')
    if key == 0:
        path = "coffee_check.xlsx"
        xlsxpart = MIMEApplication(open(path, 'rb').read())
        basename = "lost_data.xlsx"
        xlsxpart.add_header('Content-Disposition', 'attachment',
                            filename=('gbk', '', basename))  # 注意：此处basename要转换为gbk编码，否则中文会有乱码。
        msg.attach(xlsxpart)  # 添加附件
    if key == 1:
        # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
        msg = MIMEText('数据没问题,不信自己可以看一下', 'plain', 'utf-8')
    subject = '爬虫日志'
    msg['Subject'] = Header(subject, 'gbk')
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, msg.as_string())
        smtpObj.quit()
        print("邮件发送成功")
    except Exception as e:
        print(e)


def check_data():
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "shops")
    cursor = db.cursor()
    inquery_sql = """select shopId,CityName from Luckin_shop_detail where shopId not in  (select shopId from Luckin WHERE crawlTime = '%s')""" % end_day
    print(inquery_sql)
    cursor.execute(inquery_sql)
    results = cursor.fetchall()
    len_results = len(results)
    print('当前剩余数据长度%s' % len_results)
    if len_results > 14:
        # 查到缺失的数据,并且生成excel表格
        path = get_lost_data()
        # 发送邮件,0代表有问题,1代表没什么问题
        sed_email(0)
    else:
        sed_email(1)


# 获取缺失数据的
def get_data(date):
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "shops")
    cursor = db.cursor()
    inquery_sql = """select count(*),CityName,city_level from Luckin_shop_detail WHERE shopId in  (select shopId  from Luckin WHERE crawlTime = '%s') GROUP BY CityName""" % date
    print(inquery_sql)
    cursor.execute(inquery_sql)
    results = cursor.fetchall()
    df = pd.DataFrame(list(results))  # 转换成DataFrame格式
    df['crawlTime'] = date
    return df


# 获取缺失的数据逻辑函数,返回的是文件的路径名
def get_lost_data():
    day_list = []
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    day_list.append(yesterday)
    day_list.append(today)
    for date in day_list:
        df_data = get_data(date)
        df_data.to_csv('coffee_check.csv', mode='a', header=False, encoding="gbk", index=False)
    csv_data = pd.read_csv('coffee_check.csv', encoding="gbk")  # 再去读信息
    # csv_data.to_excel('coffee_check.xlsx', encoding="gbk", index=False)
    csv_data.to_excel('coffee_check.xlsx', index=False)
    os.remove('coffee_check.csv')
    return 'coffee_check.xlsx'


if __name__ == '__main__':
    today_time = time.localtime(time.time())
    end_day = time.strftime("%Y-%m-%d", today_time)
    print(end_day)
    for j in (1, 2):
        result = 0
        while result == 0:
            try:
                # 启动APP
                result = front()
            except Exception as e:
                # 跳出去之前再重启APP
                result = 0
                driver = webdriver.Remote("http://192.168.103.104:4723/wd/hub", cap)
        get_source()
    # 检查数据发送邮件
    check_data()
    # 关闭APP
    driver.close_app()
