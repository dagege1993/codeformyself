# Faker加随机头信息
import random

import spidermodule
# from python文件读取pyMongo批量插入 import Faker


class lianjiaDownloadmiddlewareRandomUseragent(object):
    def __init__(self):
        self.fake = Faker()

    def process_request(self, request, spider):
        # print(self.fake.user_agent())
        request.headers.setdefault('User-Agent', self.fake.user_agent())


'''chrome()：随机生成Chrome的浏览器user_agent信息

firefox()：随机生成FireFox的浏览器user_agent信息

internet_explorer()：随机生成IE的浏览器user_agent信息

opera()：随机生成Opera的浏览器user_agent信息

safari()：随机生成Safari的浏览器user_agent信息

linux_platform_token()：随机Linux信息

user_agent()：随机user_agent信息'''

for i in range(1, 101):
    print(Faker().chrome())

# 利用request测试头信息,可以随机从faker头信息
# session = requests.session()
# headers = {
#     # 'referer': response.url,
#     'User-Agent': random.choice(settings.USER_AGENTS_LIST),
# }
# session.get('http://bj.meituan.com/meishi/', headers=headers)
# res = session.get('http://www.meituan.com/meishi/177842585/', headers=headers)
#
# USER_AGENTS_LIST_TEST = []
# for i in USER_AGENTS_LIST:
#     headers['User-Agent'] = i
#     session.get('http://bj.meituan.com/meishi/', headers=headers)
#     res = session.get('http://www.meituan.com/meishi/177842585/', headers=headers)
#     if '我在流年这端等你' in res.content.decode('utf-8', 'ignore').replace(u'\xa9', u''):
#         USER_AGENTS_LIST_TEST.append(i)
# print(len(USER_AGENTS_LIST))
# print(len(USER_AGENTS_LIST_TEST), USER_AGENTS_LIST_TEST)


# 随机头,代理,requests验证
# import spidermodule
# from python文件读取pyMongo批量插入 import Faker
# from faker import Faker
# 要访问的目标页面
targetUrl = "http://test.abuyun.com"

# 代理服务器
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"

# 代理隧道验证信息
proxyUser = "H109354P276SH48D"
proxyPass = "DBB899017E427078"

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}

proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}

session = spidermodule.session()
f = Faker(locale='zh_CN')
headers = {
    # 'referer': response.url,
    'User-Agent': f.chrome(),
}
# session.get('https://www.che168.com/china/list/', headers=headers, proxies=proxies)
res = session.get('https://www.che168.com/china/list/', headers=headers, proxies=proxies)
print(res.text)
