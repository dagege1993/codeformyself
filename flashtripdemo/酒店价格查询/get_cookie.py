from selenium import webdriver

chrome_options = webdriver.ChromeOptions()

browser = webdriver.Chrome(chrome_options=chrome_options,
                           executable_path='/Users/huangjack/PycharmProjects/codeformyself/flashtripdemo/酒店价格查询/chromedriver')  # 加代理
browser.get("https://www.tripadvisor.cn/Hotels-g298484-Moscow_Central_Russia-Hotels.html")
cookies = browser.get_cookies()
print(cookies)



https://www.tripadvisor.cn/Hotels-g298484-oa30-Moscow_Central_Russia-Hotels.html
https://www.tripadvisor.cn/Hotels-g298484-oa60-Moscow_Central_Russia-Hotels.html
https://www.tripadvisor.cn/Hotels-g298484-Moscow_Central_Russia-Hotels.html