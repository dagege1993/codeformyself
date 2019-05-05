# encoding=utf8
import time
from appium import webdriver


cap = {
    "platformName": "Android",
    "platformVersion": "4.4.2",
    "deviceName": "127.0.0.1:62001",
    "appPackage": "com.bullet.messenger",
    "appActivity": "com.smartisan.flashim.main.activity.MainActivity",
    "noReset": "true"
}

driver = webdriver.Remote("http://localhost:4723/wd/hub", cap)
try:
    el1 = driver.find_element_by_id("com.bullet.messenger:id/bullet_close_btn")
    if el1:
        el1.click()
except Exception as e:
    pass
el2 = driver.find_element_by_xpath(
    "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.RelativeLayout[3]/android.widget.ImageView")
el2.click()
time.sleep(1)
el3 = driver.find_element_by_xpath(
    "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.support.v4.view.ViewPager/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.RelativeLayout[1]/android.widget.TextView")
el3.click()


def get_size():
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    return (x, y)


# 获取屏幕大小,以及确定下滑的距离
l = get_size()
x1 = int(l[0] * 0.5)
y1 = int(l[1] * 0.75)
y2 = int(l[1] * 0.25)
while True:
    driver.swipe(x1, y1, x1, y2)  # appnium的滑动函数
    time.sleep(1.0)
