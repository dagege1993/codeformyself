# encoding=utf8
import json
import math
import re
import time

import scrapy

from Downloads.items import sqlItem

i = 0


class Index(scrapy.Spider):
    name = '360_from_phone'
    # 从首页进入
    start_urls = [
        'http://openbox.mobilem.360.cn/app/getCatTags/cid/1?ver_type=1&prepage=recommend&curpage=categorysoft&os=19&vc=300070071&v=7.0.71',
        'http://openbox.mobilem.360.cn/app/getNewTags?lid=90&prepage=categorygame_90&curpage=categorygame_90&page=1&os=19',
        'http://openbox.mobilem.360.cn/app/getNewTags?lid=91&prepage=categorygame_91&curpage=categorygame_91&page=1&os=19',
        'http://openbox.mobilem.360.cn/app/getNewTags?lid=92&prepage=categorygame_92&curpage=categorygame_92&page=1&os=19',
    ]

    custom_settings = {
        "RETRY_ENABLED": True,
        "RETRY_TIMES": 3,
        "COOKIES_ENABLED": False,
        "HTTPERROR_ALLOWED_CODES": [429, 403],  # 429的状态码不报错
        "ITEM_PIPELINES": {
            'Downloads.pipelines.SqlserverPipelineweek': 300
        },
        # "DOWNLOAD_DELAY": 0.1,
        "DOWNLOADER_MIDDLEWARES": {
            'Downloads.middlewares.ProxyMiddleware': 543,  # 代理启用
            # 'Downloads.middlewares.RandomUserAgentMiddleware': 544,  # 随机头
            # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
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
        # 获取每个大类以及小类
        response_text = json.loads(response.text)
        data_set = response_text.get('data')
        response_url = response.url
        labels = ['weekpure', 'newest']  # 两种排序方式
        # 软件类别的处理方式
        if 'categorysoft' in response_url:
            for data in data_set:
                title_dict = {}
                if 'title2' in data:  # 只有包含了title2的才有子类
                    title_dict['title'] = data.get('title')
                    title_dict['big_tag'] = data.get('big_tag')
                    tag2_list = data.get('tag2')
                    for j, tag2 in enumerate(tag2_list):
                        tag2_dict = {}
                        tag2_dict['title2'] = data.get('title2')
                        tag2_dict['tag2'] = tag2_list
                        tag2_dict['j'] = j
                        for label in labels:
                            url = 'http://openbox.mobilem.360.cn/app/getTagAppList?s_stream_app=1&cid=1&tag=' + \
                                  title_dict[
                                      'title'] + '&tag2=' + tag2 + '&order=' + label + '&prepage=categorysoft&curpage=categorysoft_%E8%B4%AD%E7%89%A9_%E5%95%86%E5%9F%8E&page=1&os=19&vc=300070071'
                            # print('当前请求的url', url)
                            # if tag2 == '商城;电商':
                            yield scrapy.Request(url, callback=self.detail, meta=tag2_dict)
        if 'categorygame' in response_url:
            for data in data_set:
                game_tag_name = data.get('game_tag_name')
                print(game_tag_name)
                for label in labels:
                    url = 'http://openbox.mobilem.360.cn/app/getTagAppList?s_stream_app=1&cid=2&tag=' + game_tag_name + '&order=' + label + '&prepage=categorygame_91&curpage=categorygame_91_' + game_tag_name + '&page=1&os=19'
                    yield scrapy.Request(url, callback=self.detail)

    def detail(self, response):
        # 最大页数
        old_url = response.url
        response_text = json.loads(response.text)
        data_set = response_text.get('data')
        if data_set:
            for data in data_set:
                # print(data)
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
                query_param = response_text.get('queryParam')
                three_item['sort'] = query_param.get('tag')
                # 因为只有软件才有三级类,游戏只有二级类
                if 'categorysoft' in response.url:
                    tag2_dict = response.meta
                    title2 = tag2_dict.get('title2')
                    # url_tag2 = tag2_dict.get('tag2')
                    j = tag2_dict.get('j')
                    three_item['category_lv3'] = title2[j]
                else:
                    # 假如是游戏类的话
                    three_item['category_lv3'] = ''
                    tag2_dict = ''
                global i
                i += 1
                three_item['top_num'] = i
                localtime = time.localtime(time.time())
                str_time = time.strftime("%Y-%m-%d", localtime)
                # str_time = '2018-12-29'  # 抓取时间
                # str_time = '2019-01-04'  # 抓取时间
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
                current_page = response_text.get('queryParam').get('page')
                three_item['page_num'] =current_page # 为了做计数的
                three_item['versionname'] = versionname  # 版本号
                three_item['source'] = 'Phone'
                if 'weekpure' in old_url:
                    three_item['sub'] = '最热'
                if 'newest' in old_url:
                    three_item['sub'] = '最新'
                # print(three_item)
                yield three_item
            # 拿到这类app的总数,得让他先解析完你再弄
            total = response_text.get('total')
            # 当前请求page
            current_page = response_text.get('queryParam').get('page')
            # 返回结果数据个数
            step = len(data_set)
            # print(step)
            if total:
                max_page = math.ceil(total / step)  # 因为这个步数不确定
                print('总个数%s,当前页数%s,最大页数%s,步伐宽度%s' % (total, current_page, max_page, step))
                if current_page == 16:
                    print(1111)
                if int(current_page) < int(max_page):
                    next_page = current_page + 1
                    result = re.findall('(page=\d+)', old_url)
                    replace_page = result.pop()
                    new_url = old_url.replace(replace_page, 'page=' + str(next_page))
                    # print(new_url)
                    yield scrapy.Request(new_url, callback=self.detail, meta=tag2_dict)
