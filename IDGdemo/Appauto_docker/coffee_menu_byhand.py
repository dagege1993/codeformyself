import datetime
import os
import pandas as pd
import time
import re
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from clean_menu import cleaning_menu
from config_logs import Config


conf = Config()
logger = conf.getLog()
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
y1 = int(l[1] * 0.50)
y2 = int(l[1] * 0.25)


# 前面的准备工作
def front():
    # 点击不切换新版本
    time.sleep(2)
    # appnium的点击办法
    # time.sleep(30)
    time.sleep(15)
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


# 点击首页的时候获取shopname
def get_shop_name(source):
    results = re.findall('<android.widget.TextView index="\d+" text=(.*?) class', source)
    logger.info(results)
    if results:
        result = results[0]
    else:
        result = '0'
    return result


# 滑到最后,为了展示全部的城市
def get_source():
    # 这里是点击第一家店
    logger.info('城市列表页第一页第一家店================================================')
    logger.info('中间页面第一家店==============================')
    # 这里是处理中间城市页面第一家店

    for i in range(2, 19):
        logger.info('当前是第%s页' % i)
        try:
            time.sleep(1)
            # 划四下滑到最后面
            city = '南京'  # 手动输入吧
            time.sleep(0.5)
            logger.info('当前抓取城市%s' % city)
            time.sleep(0.5)
            # 测试手动点击
            # 这里应该要获取店铺名称
            shop_name_source = driver.page_source
            shop_name = get_shop_name(shop_name_source)
            # logger.info(shop_name)
            # 再点击现在下单
            el5 = driver.find_element_by_xpath(
                "//android.widget.RelativeLayout[@resource-id='com.lucky.luckyclient:id/rl_order_now']")
            time.sleep(0.5)
            el5.click()
            time.sleep(0.5)
            data = driver.page_source
            if '打烊' in data:
                # 点击了我知道了
                e17 = driver.find_element_by_xpath(
                    "//android.widget.TextView[@resource-id='com.lucky.luckyclient:id/submit']")
                e17.click()
            else:
                pass
                # 这是首页解析
                cleaning_menu(data, city, shop_name)
                for i in range(20):
                    if '已经全部加载完成' in driver.page_source:
                        break
                    time.sleep(1.0)
                    # 划两次,划一个全屏,还是只能半屏划,全屏划数据会有丢失
                    driver.swipe(x1, y1, x1, y2, 300)  # appnium的滑动函数
                    time.sleep(1.0)
                    data = driver.page_source
                    # logger.info('第一次以后的数据%s' % data)
                    # logger.info(data)
                    # 后续页面解析
                    cleaning_menu(data, city, shop_name)

                #  有内容的时候退出到城市列表
                if WebDriverWait(driver, 5).until(lambda x: x.find_element_by_xpath(
                        "//android.widget.LinearLayout[@resource-id='com.lucky.luckyclient:id/custom_tab_container']/android.widget.LinearLayout[1]")):
                    el1 = driver.find_element_by_xpath(
                        "//android.widget.LinearLayout[@resource-id='com.lucky.luckyclient:id/custom_tab_container']/android.widget.LinearLayout[1]")
                    el1.click()
                    logger.info('当前城市抓取完毕,退出当前城市')

                # 点击店铺名称进入切换城市
                if WebDriverWait(driver, 5).until(
                        lambda x: x.find_element_by_id("com.lucky.luckyclient:id/ll_select_dept")):
                    el2 = driver.find_element_by_id("com.lucky.luckyclient:id/ll_select_dept")
                    el2.click()
                    logger.info('点击店铺名称进入切换城市')
                # 点击切换城市
                if WebDriverWait(driver, 5).until(
                        lambda x: x.find_element_by_id("com.lucky.luckyclient:id/tv_select_city")):
                    el2 = driver.find_element_by_id("com.lucky.luckyclient:id/tv_select_city")
                    el2.click()
                    logger.info('点击切换城市')

            # 点击进去没有数据,就退出来
            if '抱歉' in data:
                # 没有内容的时候退出到城市列表
                # 点击切换城市
                if WebDriverWait(driver, 5).until(
                        lambda x: x.find_element_by_id("com.lucky.luckyclient:id/tv_select_city")):
                    el2 = driver.find_element_by_id("com.lucky.luckyclient:id/tv_select_city")
                    el2.click()
                    logger.info('切换城市')
            # logger.info(111111111)
        except Exception as e:
            # 可能是这家城市只有一家店是可点击的,需要点击切换到城市列表
            # 点击切换城市
            if WebDriverWait(driver, 5).until(
                    lambda x: x.find_element_by_id("com.lucky.luckyclient:id/tv_select_city")):
                el2 = driver.find_element_by_id("com.lucky.luckyclient:id/tv_select_city")
                el2.click()
                logger.info('点击切换到城市列表')
            else:
                pass
            logger.info(e)




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
    logger.info(end_day)
    for j in (1, 4):
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
    # check_data()
    # 关闭APP
    driver.close_app()
