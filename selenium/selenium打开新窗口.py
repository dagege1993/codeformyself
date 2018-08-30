# coding = utf-8
'''
多窗口句柄
获取
切换
'''

from selenium import webdriver

driver = webdriver.Chrome()
driver.get("http://home.zhiyoo.com/")
driver.implicitly_wait(3)

# 获取当前窗口句柄
h = driver.current_window_handle
print(h)  # 打印首页句柄

driver.find_element_by_link_text(u'智友论坛').click()
driver.implicitly_wait(3)

all_h = driver.window_handles
print(all_h)  # 打印所有的句柄

# 切换句柄
# 方法一：
for i in all_h:
	if i != h:
		driver.switch_to_window(i)
		print(driver.title)
# 方法二：
# driver.switch_to_window(all_h[1])
# print(driver.title)

# 关闭新窗口
driver.close()
# 切换到首页句柄
driver.switch_to_window(h)
# 打印当前的title
print(driver.title)
