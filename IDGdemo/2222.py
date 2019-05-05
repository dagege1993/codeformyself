# selenium模拟登录知乎
## 模拟登陆代码
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
# executable_path指的是webdriver的存放路径
browser = webdriver.Chrome(executable_path=r'C:\Users\Administrator.DESKTOP-DV7S27B\Desktop\IDGdemo\selenium\chromedriver.exe', options=chrome_options)

browser.get('https://www.zhihu.com/signup?next=%2F')

# print(browser.page_source)  # 打印输出网页的源码
# 点击跳转到登录页面
browser.find_element_by_css_selector('.SignContainer-switch span').click()
time.sleep(10)
# 用户名
browser.find_element_by_css_selector('.SignFlow-account .Input').send_keys('XXX')

time.sleep(3)
# 密码
browser.find_element_by_css_selector('.SignFlow-password .Input').send_keys('YYY')
time.sleep(3)
# 点击登录
browser.find_element_by_css_selector('.SignFlow button[type="submit"]').click()
time.sleep(5)
# browser.quit()


## 浏览器环境配置
# 0. 这个方法的思路就是让系统接管浏览器，从而避免被网站识别出是selenium，但是频繁登录会弹验证码
# 1. 在环境变量中找到'Path'
# 2. 编辑，然后将chrome的路径加进去:'C:\Program Files (x86)\Google\Chrome\Application'(路径可能不一样)
# 3. 然后一路点击OK退出
# 4. 在cmd中输入如下代码:chrome.exe --remote-debugging-port=9222 --user-data-dir="H:\extensions\selenium\AutomationProfile" (其中的路径可以自己指定),输入之后会出现一个浏览器，不要关闭
# 5. 此时运行上述代码即可