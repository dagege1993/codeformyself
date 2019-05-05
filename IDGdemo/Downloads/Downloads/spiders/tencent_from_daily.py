import json
import re
import time
import scrapy
from Downloads.items import sqlItem
from Downloads.spiders.get_lost_function import get_lost_app_keys, get_lost_app_pkg

i = 0
localtime = time.localtime(time.time())
str_time = time.strftime("%Y-%m-%d", localtime)
# str_time = '2019-01-20'


class Index(scrapy.Spider):
    name = 'tencent_from_daily'
    # 从首页进入
    start_urls = ['https://android.myapp.com/myapp/category.htm?orgame=1',
                  'https://android.myapp.com/myapp/category.htm?orgame=2'
                  ]

    custom_settings = {
        "RETRY_ENABLED": True,
        "RETRY_TIMES": 3,
        "COOKIES_ENABLED": False,
        "DOWNLOAD_DELAY": 0.2,
        "HTTPERROR_ALLOWED_CODES": [429, 403, 400],  # 429的状态码不报错
        "ITEM_PIPELINES": {
            'Downloads.pipelines.tencent_daily_sqlPipeline': 300
        },
        "DOWNLOADER_MIDDLEWARES": {
            'Downloads.middlewares.ProxyMiddleware': 543,  # 代理启用
            # 'Downloads.middlewares.RandomUserAgentMiddleware': 544,  # 随机头
            # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        },
        'DEFAULT_REQUEST_HEADERS': {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Referer": "https://sj.qq.com/myapp/category.htm?orgame=1",
            "Connection": "keep-alive",
            # "Host": "android.myapp.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
        }
    }

    def parse(self, response):
        # 获取首页各个类别的名字
        # 从app库获取的app_keys - daily当天已经入库的app_keys 然后去app_list拿app_keys对应的app_pkg,去访问详情页数据
        sql = """SELECT a.* FROM(
            SELECT app_keys FROM ANDROID_QQ_APP_DAILY WHERE stat_dt = '%s'
            UNION ALL
            SELECT app_keys FROM ANDROID_QQ_APP 
        )a GROUP BY a.app_keys HAVING COUNT(a.app_keys)=1""" % (str_time)
        # 拿到所有的未抓取过得id
        app_keys_list = get_lost_app_keys(sql)
        for app_keys in app_keys_list:
            if app_keys:
                # 通过app_keys 拿到对应的app_pkg
                get_app_pkg_sql = """select app_pkg from ANDROID_QQ_APP_LIST WHERE app_keys = '%s'""" % app_keys
                app_pkg = get_lost_app_pkg(get_app_pkg_sql)
                if app_pkg:
                    url = 'https://sj.qq.com/myapp/detail.htm?apkName=' + app_pkg
                    # print(url)
                    # app_key和app_pkg对应的一个键值对
                    app_keys_pkg_dict = {}
                    app_keys_pkg_dict['app_keys'] = app_keys
                    app_keys_pkg_dict['app_pkg'] = app_pkg
                    # url = "https://sj.qq.com/myapp/detail.htm?apkName=com.sinyee.babybus.qqfish"
                    yield scrapy.Request(url, callback=self.class_index, meta=app_keys_pkg_dict, )

    def class_index(self, response):
        # 每个类别的第后续页数都是js动态加载.所以直接
        three_item = sqlItem()
        # localtime = time.localtime(time.time())
        # str_time = time.strftime("%Y-%m-%d", localtime)
        three_item['stat_dt'] = str_time
        app_keys_pkg_dict = response.meta
        three_item['app_keys'] = app_keys_pkg_dict.get('app_keys')
        result = re.findall('downTimes:"(\d+)",', response.text)
        three_item['downs'] = result.pop()  # pkgname
        three_item['dt_type'] = '周'  # 抓取类型为周
        yield three_item
