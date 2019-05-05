import json
import math
import re
import time
import scrapy
from Downloads.items import sqlItem
from Downloads.spiders.get_lost_function import get_lost_app_pkg, get_lost_app_keys

i = 0
localtime = time.localtime(time.time())
str_time = time.strftime("%Y-%m-%d", localtime)


class Index(scrapy.Spider):
    name = '360_from_daily'
    # 从首页进入
    start_urls = [
        'http://openbox.mobilem.360.cn/app/getNewTags?lid=90&prepage=categorygame_90&curpage=categorygame_90&page=1&os=19',
    ]
    custom_settings = {
        "RETRY_ENABLED": True,
        "RETRY_TIMES": 3,
        "COOKIES_ENABLED": False,
        "HTTPERROR_ALLOWED_CODES": [429, 403],  # 429的状态码不报错
        "ITEM_PIPELINES": {
            'Downloads.pipelines.Safe_daily_sqlPipeline': 300,
            # 'Downloads.pipelines.MysqlTwistedPipeline': 300
        },
        "DOWNLOADER_MIDDLEWARES": {
            'Downloads.middlewares.ProxyMiddleware': 543,  # 代理启用
        },
        'DEFAULT_REQUEST_HEADERS': {
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "Mozilla/5.0 (Linux; U; Android 4.4.2; zh-cn; OPPO R11 Build/NMF26X) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30;360appstore",
            "X-403": "2",
            "Host": "openbox.mobilem.360.cn",
            "Connection": "Keep-Alive"
        }
    }

    def parse(self, response):
        # 从app库获取的app_keys - daily当天已经入库的app_keys 然后去app_list拿app_keys对应的app_pkg,去访问详情页数据
        sql = """SELECT a.* FROM(
    SELECT app_keys FROM ANDROID_SAFE_APP_DAILY WHERE stat_dt = '%s'
    UNION ALL
    SELECT app_keys FROM ANDROID_SAFE_APP 
)a GROUP BY a.app_keys HAVING COUNT(a.app_keys)=1""" % (str_time)
        app_keys_list = get_lost_app_keys(sql)
        app_keys_list = list(set(app_keys_list))
        # 这里传的是app_pkg
        # for app_keys in app_keys_list:
        #     if app_keys:
        #         get_app_pkg_sql = """select app_pkg from ANDROID_SAFE_APP_LIST WHERE app_keys = '%s'""" % app_keys
        #         app_pkg = get_lost_app_pkg(get_app_pkg_sql)
        #         if app_pkg:
        #             url = 'http://openbox.mobilem.360.cn/Iservice/AppDetail?s_stream_app=1&market_id=360market&sort=1&pname=' + app_pkg + '&pos=55&label=zuixin&prelabel=zuixin&prepage=categorygame_90_%E7%BB%8F%E8%90%A5&curpage=appinfo&v=7.0.71'
        #             print(url)
        #             yield scrapy.Request(url, callback=self.detail)
        for app_keys in app_keys_list:
            if app_keys:
                url = 'http://openbox.mobilem.360.cn/Iservice/AppDetail?s_stream_app=1&market_id=360market&sort=1&pname=' + app_keys + '&pos=55&label=zuixin&prelabel=zuixin&prepage=categorygame_90_%E7%BB%8F%E8%90%A5&curpage=appinfo&v=7.0.71'
                # print(url)
                yield scrapy.Request(url, callback=self.detail)

    def detail(self, response):
        old_url = response.url
        response_text = json.loads(response.text)
        data_set = response_text.get('data')
        if len(data_set) == 1:
            data = data_set.pop()
            three_item = sqlItem()
            id = data.get('id')
            three_item['app_keys'] = int(id)
            downloads_nums = data.get('download_times')
            three_item['downs'] = int(downloads_nums)
            type = data.get('type')
            if 'soft' in type:
                three_item['cate'] = '应用'  # 0 代表游戏,1代表软件
            if 'game' in type:
                three_item['cate'] = '游戏'  # 0 代表游戏,1代表软件
            # sort是二级类,cate是一级类
            # query_param = response_text.get('queryParam')
            # three_item['sort'] = query_param.get('tag')
            global i
            i += 1
            three_item['top_num'] = i
            localtime = time.localtime(time.time())
            str_time = time.strftime("%Y-%m-%d", localtime)
            # str_time = '2018-12-29'  # 抓取时间
            three_item['stat_dt'] = str_time  # 抓取时间
            three_item['in_dt'] = str_time  # app_list表里的插入时间
            three_item['dt_type'] = '周'  # 抓取类型为周
            pkg_name = data.get('apkid')
            three_item['pkgname'] = pkg_name  # json数据源显示的是apkid
            app_name = data.get('name')
            three_item['app_name'] = app_name  # app名
            app_md5 = data.get('apk_md5')
            three_item['app_md5'] = app_md5  # appmd5
            versionname = data.get('version_name')
            three_item['versionname'] = versionname  # 版本号
            three_item['source'] = 'Phone'
            if 'weekpure' in old_url:
                three_item['sub'] = '最热'
            if 'newest' in old_url:
                three_item['sub'] = '最新'
            # print(three_item)
            yield three_item
