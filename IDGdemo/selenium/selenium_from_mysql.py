# coding = utf-8
import json
import os
import time
import pymysql
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def get_company_names():
    company_name_list = []
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "company")
    cursor = db.cursor()
    sql = """Select project_name From unions1203 Where DATE_FORMAT(finance_time,'%Y-%m-%d') >= '2019-01-18' and DATE_FORMAT(finance_time,'%Y-%m-%d') <= '2019-01-25' AND legal_name = '' AND types=1 ORDER BY finance_time;"""
    cursor.execute(sql)
    db.commit()
    datas = cursor.fetchall()
    for data in datas:
        company_name_list.append(''.join(data))
    return company_name_list


def get_ip():
    proxy = requests.get('http://192.168.103.23:9898/?qty=1&user=hlz_selenium_spider&packid=2')
    proxy_response = json.loads(proxy.text)
    data = proxy_response.get('data')
    if len(data) > 0:  # 如果有代理,就添加代理
        ip_dict = data.pop()
        ip = ip_dict.get('IP')
        print('当前代理IP', "http://" + ip)
        return "http://" + ip


def seleniums():
    # 为了selenium加上代理先
    chrome_options = webdriver.ChromeOptions()
    # 设置代理
    # chromeOptions.add_argument("--proxy-server=" + get_ip())
    # chromeOptions.add_argument('--headless')  # 设置无头浏览器,节约内存
    browser = webdriver.Chrome(chrome_options=chrome_options)  # 加代理
    browser.get("http://www.xiniudata.com/project/lib")
    time.sleep(3)
    for i in range(4):
        try:
            # 将滚动条移动到页面的底部
            js = "var q=document.documentElement.scrollTop=100000"
            browser.execute_script(js)
            time.sleep(1)
        except:
            pass
    browser.find_element_by_link_text('登录网站').click()  # 点击登录按钮
    time.sleep(10)
    # time.sleep(160)
    # 登录完成后
    # 登陆后滑到最底下
    first_handle = browser.current_window_handle  # 当前句柄
    company_name_list = get_company_names()
    print('剩余公司长度', len(company_name_list))
    # 清理一些特殊数据作为测试,remove是没有返回值的
    company_name_list.remove('掌门1对1')
    for company_name in company_name_list[0:30]:  # 截取前三十个,因为单个用户只能访问三十条
        print(company_name)
        result_text = company_name
        time.sleep(3)
        # 不然会存在有一个输入框找不到
        browser.maximize_window()
        browser.find_element_by_tag_name("input").send_keys(company_name)
        # browser.find_element_by_tag_name("input").send_keys(Keys.ENTER)  # 发送回车键,2019/01/17号回车键不能用了
        # browser.find_element_by_xpath('//*[@id="__next"]/div/div/nav/div/div[2]/div/div/div').click()  # 发送回车键
        browser.find_element_by_xpath('//*[@id="__next"]/div/div/nav/div/div[2]/div/div/div').click()  # 发送回车键
        time.sleep(10)
        # 显示等待
        browser.find_element_by_class_name('name-link').click()
        # result = browser.find_element_by_class_name('name-link')
        time.sleep(1)
        for i in range(3):
            try:
                # 将滚动条移动到页面的底部
                js = "var q=document.documentElement.scrollTop=100000"
                browser.execute_script(js)
                time.sleep(1)
            except:
                pass
        handles = browser.window_handles  # 获取当前窗口句柄集合（列表类型）
        for handle in handles:  # 切换窗口
            if handle != first_handle:
                browser.switch_to.window(handle)
                filepath = get_path() + '\\' + result_text + ".html"
                # print(filepath)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(browser.page_source)
        browser.close()  # 写完了之后关闭当前窗口
        browser.switch_to.window(first_handle)
        browser.back()
        time.sleep(1)
    browser.quit()


def get_path():
    localtime = time.localtime(time.time())
    str_time = time.strftime("%Y-%m-%d", localtime)
    abs_path = r"C:\Users\Administrator.DESKTOP-DV7S27B\Desktop\IDGdemo\selenium\日常更新/{}".format(str_time)
    if os.path.exists(abs_path) is False:
        print('路径不存在,需要创建')
        os.makedirs(abs_path)
    # else:
    #     print('路径存在')
    return abs_path


if __name__ == '__main__':
    print(get_company_names())
    print('剩余公司长度', len(get_company_names()))
    try:
        seleniums()
    except Exception as e:
        print(e)
    # get_path()
# 从数据库读取公司名字然后搜索公司详情
