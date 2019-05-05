import time
from appium import webdriver
from clean_storage import cleaning
from selenium.webdriver.support.ui import WebDriverWait
from config_logs import Config

conf = Config()
logger = conf.getLog()
cap = {
    "platformName": "Android",
    "platformVersion": "4.4.2",
    "deviceName": "127.0.0.1:62001",
    "appPackage": "com.lucky.luckyclient",
    "appActivity": "com.lucky.luckyclient.splash.splash.SplashActivity",
    "noReset": True
}


def get_size():
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    return (x, y)


driver = webdriver.Remote("http://192.168.103.104:4723/wd/hub", cap)
# 点击不切换新版本
time.sleep(2)
# appnium的点击办法
time.sleep(30)

'''
# 差掉立即升级
el1 = driver.find_element_by_id("com.lucky.luckyclient:id/dismiss_btn")
time.sleep(2)
el1.click()
time.sleep(2)
# 点击切换城市
el2 = driver.find_element_by_id("com.lucky.luckyclient:id/confirm_btn")
time.sleep(2)
el2.click()
'''
# autoview版本
# 差掉升级
e11 = driver.find_element_by_xpath(
    "//android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.RelativeLayout[1]/android.widget.LinearLayout[1]/android.widget.ImageView[2]")
e11.click()
e12 = driver.find_element_by_xpath(
    "//android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[2]/android.widget.Button[1]")
e12.click()

# 获取屏幕大小,以及确定下滑的距离
l = get_size()
x1 = int(l[0] * 0.5)
y1 = int(l[1] * 0.75)
y2 = int(l[1] * 0.25)
# 滑到最后,为了展示全部的城市

# 1-21只能是到南京,定位元素是20,下面的元素又不一样
for i in range(1, 21):
    logger.info('当前是第%s页' % i)
    try:
        time.sleep(0.5)
        el3 = driver.find_element_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout[2]/android.widget.ListView/android.widget.LinearLayout[" + str(
                i) + "]/android.widget.TextView")
        time.sleep(0.5)
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
        el1.click()
        logger.info('当前城市抓取完毕,退出当前城市')
    # 点击切换城市
    if WebDriverWait(driver, 5).until(lambda x: x.find_element_by_id("com.lucky.luckyclient:id/confirm_btn")):
        el2 = driver.find_element_by_id("com.lucky.luckyclient:id/confirm_btn")
        el2.click()
        logger.info('切换城市')

# 后面几个城市
for i in range(4, 21):
    logger.info('当前是第%s页' % i)
    try:
        driver.swipe(x1, y1, x1, y2)  # appnium的滑动函数
        time.sleep(1)
        driver.swipe(x1, y1, x1, y2)  # appnium的滑动函数
        time.sleep(0.5)
        el3 = driver.find_element_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout[2]/android.widget.ListView/android.widget.LinearLayout[" + str(
                i) + "]/android.widget.TextView")
        time.sleep(0.5)
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
            logger.info('第一次以后的数据%s' % data)
            cleaning(data, city)
    # 点击进去没有数据,就退出来
    if '抱歉' in data:
        # 滑到最后,得点击退出来
        pass
    # 最后都要点击退出,然后重新进入
    if WebDriverWait(driver, 5).until(lambda x: x.find_element_by_id("com.lucky.luckyclient:id/iv_back")):
        el1 = driver.find_element_by_id("com.lucky.luckyclient:id/iv_back")
        el1.click()
        logger.info('当前城市抓取完毕,退出当前城市')
    # 点击切换城市
    if WebDriverWait(driver, 5).until(lambda x: x.find_element_by_id("com.lucky.luckyclient:id/confirm_btn")):
        el2 = driver.find_element_by_id("com.lucky.luckyclient:id/confirm_btn")
        el2.click()
        logger.info('切换城市')
