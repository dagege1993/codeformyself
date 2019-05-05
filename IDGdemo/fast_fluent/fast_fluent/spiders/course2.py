# encoding=utf-8
# course爬虫只是为了获取课程ID
import json
import math
import time
import scrapy

from config_log import Config
from course.mysql_get_course_id import course_id_count
from fast_fluent.items import CourseItem
from fast_fluent.starturl_list import get_token
from mysql_couse import get_course_id

conf = Config()
logger = conf.getLog()
fluent_id_list = []


class Community(scrapy.Spider):
    name = 'Course'
    start_urls = [
        "https://apineo.llsapp.com/api/v1/curriculums/filtered?type=1&pageSize=20&level=&sort=diamond_consume_desc&page=1&appVer=6&deviceId=354730011088642&sDeviceId=354730010301566&appId=lls&token=" + get_token()
    ]
    custom_settings = {
        # 重试机制
        "RETRY_ENABLED": True,
        "RETRY_TIMES": 5,
        "COOKIES_ENABLED": False,
        "HTTPERROR_ALLOWED_CODES": [429, 401],  # 429的状态码不报错
        # "DOWNLOAD_DELAY": 0.2,
        # 'AUTOTHROTTLE_ENABLED': True,  # 启动[自动限速]
        "ITEM_PIPELINES": {
            'fast_fluent.pipelines.Mysql_Course_ID_Pipeline': 300},
        "DOWNLOADER_MIDDLEWARES": {
            # 'fast_fluent.middlewares.ProxyMiddleware': None,#代理是否启用
            'fast_fluent.middlewares.ProxyMiddleware': 543,  # 代理是否启用
        },
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            'Accept-Language': "zh-cn",
            'User-Agent': "Lingome/5.0 (SM-G955N;Android 4.4.2;)",
            'Accept-Encoding': "gzip,deflate",
            'Host': "apineo.llsapp.com",
            'cache-control': "no-cache",
        }
    }

    # 获取全部课程
    def parse(self, response):
        if "操作过于频繁，请稍后再试" in response.text:
            url = "https://apineo.llsapp.com/api/v1/curriculums/filtered?type=1&pageSize=20&level=&sort=diamond_consume_desc&page=1&appVer=6&deviceId=354730011088642&sDeviceId=354730010301566&appId=lls&token=" + get_token()
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)
        response_text = json.loads(response.text)
        total = response_text.get("total")
        id_count = int(course_id_count())  # 返回的是有多少个课程ID
        # if total > id_count:
        total_int = int(total)
        total_page = math.ceil(total_int / 20)  # 向上取整
        total_page += 1
        for page in range(1, int(total_page)):
            url = "https://apineo.llsapp.com/api/v1/curriculums/filtered?type=1&pageSize=20&level=&sort=diamond_consume_desc&page=" + str(
                page) + "&appVer=6&deviceId=354730011088642&sDeviceId=354730010301566&appId=lls&token=" + get_token()
            yield scrapy.Request(url, callback=self.parse_list, dont_filter=True)
        # print('当前没有新增的课程')

    def parse_list(self, response):
        ID_count = get_course_id()  # 获取自己建立的ID库的ID
        print('课程id库课程总长度', len(ID_count))
        if "操作过于频繁，请稍后再试" in response.text:
            yield scrapy.Request(url=response.url, callback=self.parse_list, dont_filter=True)
        else:
            response_text = json.loads(response.text)
            curriculums = response_text.get("curriculums")
            for curriculum in curriculums:
                # 获取全部课程数据
                id = curriculum.get("course").get("id")
                fluent_id_list.append(id)  # 获取流利说全部课程ID
            print('获取全部流利课程ID', fluent_id_list)
            print('获取全部流利课程ID长度', len(fluent_id_list))
            left_id_list = set(fluent_id_list) - set(ID_count)
            print('剩余IDlist', left_id_list)
            if left_id_list:
                for id in left_id_list:
                    url = "https://apineo.llsapp.com/api/v1/courses/" + id + "?appVer=6&deviceId=354730011088642&sDeviceId=354730010301566&appId=lls&token=" + get_token()
                    yield scrapy.Request(url, callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):
        courseitem = CourseItem()
        logger.info('详情页的数据%s' % response.text)
        if "操作过于频繁，请稍后再试" in response.text:
            yield scrapy.Request(url=response.url, callback=self.parse_detail, dont_filter=True)
        else:
            response_text = json.loads(response.text)
            courseitem["ID"] = response_text.get("id")
            localtime = time.localtime(time.time())
            insert_time = time.strftime("%Y-%m-%d", localtime)
            courseitem["insert_time"] = insert_time
            yield courseitem
