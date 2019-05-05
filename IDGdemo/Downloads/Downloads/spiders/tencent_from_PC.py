import json
import re
import time
import scrapy

from Downloads.items import sqlItem

i = 0


class Index(scrapy.Spider):
    name = 'tencent_from_PC'
    # 从首页进入
    start_urls = ['https://android.myapp.com/myapp/category.htm?orgame=1',
                  'https://android.myapp.com/myapp/category.htm?orgame=2']

    custom_settings = {
        "RETRY_ENABLED": True,
        "RETRY_TIMES": 3,
        "COOKIES_ENABLED": False,
        "DOWNLOAD_DELAY": 0.2,
        "HTTPERROR_ALLOWED_CODES": [429, 403],  # 429的状态码不报错
        "ITEM_PIPELINES": {
            'Downloads.pipelines.tencentPipelineweek': 300
        },
        "DOWNLOADER_MIDDLEWARES": {
            'Downloads.middlewares.ProxyMiddleware': 543,  # 代理启用
        },
        'DEFAULT_REQUEST_HEADERS': {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Host": "android.myapp.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
        }
    }

    def parse(self, response):
        # 获取首页各个类别的名字
        class_names = response.xpath("//ul[@class='menu-junior']/li").extract()
        category_names = {}
        for i, class_name in enumerate(class_names):
            category_id = re.findall('categoryId=(\d+)', class_name)
            names = re.findall('<.*>(.*)</a>', class_name)
            if category_id and names:
                category_names[category_id.pop()] = names.pop()
        for category in category_names.keys():
            orgame = re.findall('orgame=(\d)', response.url).pop()
            url = 'https://android.myapp.com/myapp/cate/appList.htm?orgame=' + orgame + '&categoryId=' + category + '&pageSize=20&pageContext=0'
            # print(url)
            yield scrapy.Request(url, callback=self.class_index)

    def class_index(self, response):
        # 每个类别的第后续页数都是js动态加载.所以直接
        response_text = json.loads(response.text)
        three_item = sqlItem()
        contents = response_text.get('obj')
        old_url = response.url
        game_or_not = re.findall('orgame=(\d)', response.url).pop()
        localtime = time.localtime(time.time())
        str_time = time.strftime("%Y-%m-%d", localtime)
        for content in contents:
            three_item['app_name'] = content.get('appName')
            three_item['app_keys'] = content.get('appId')
            three_item['app_md5'] = content.get('apkMd5')
            three_item['downs'] = content.get('appDownCount')
            if game_or_not == '2':  # url包含了软件类别
                three_item['cate'] = '游戏'  # 0 代表游戏,1代表软件
            else:
                three_item['cate'] = '软件'  # 0 代表游戏,1代表软件
            # sort二级类
            three_item['sort'] = content.get('categoryName')
            three_item['stat_dt'] = str_time  # 抓取时间
            three_item['in_dt'] = str_time  # app_list表里的插入时间
            version = content.get('versionName')
            three_item['versionname'] = version  # 版本号
            pkg_name = content.get('pkgName')
            three_item['pkgname'] = pkg_name  # pkgname
            three_item['dt_type'] = '周'  # 抓取类型为周
            three_item['source'] = 'PC'
            three_item['sub'] = ''
            global i
            i += 1
            three_item['top_num'] = i
            yield three_item
        if response_text.get('msg') == 'success':
            count = response_text.get('count')
            if count == 20:  # 当长度等于20,就证明还有下一页
                page_context = response_text.get('pageContext')  # 获取下一页的起始页码
                old_pageContext = re.findall('pageContext=\d+', old_url).pop()  # 拿到这一次请求的页码
                new_url = old_url.replace(old_pageContext, 'pageContext=' + str(page_context))  # 新页码替换掉旧页码然后发送请求
                # print(old_url)
                # print(new_url)
                yield scrapy.Request(new_url, callback=self.class_index)
