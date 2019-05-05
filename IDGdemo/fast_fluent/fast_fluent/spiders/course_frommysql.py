# encoding=utf-8
import json
import time
import scrapy

from config_log import Config
# from course.mysql_get_course_id import get_course_id
from fast_fluent.items import CourseItem
from fast_fluent.starturl_list import get_token
from mysql_couse import un_get_id

conf = Config()
logger = conf.getLog()


class Community(scrapy.Spider):
    name = 'Course_mysql'
    start_urls = [
        "https://apineo.llsapp.com/api/v1/curriculums/filtered?type=1&pageSize=20&level=&sort=diamond_consume_desc&page=1&appVer=6&deviceId=354730011088642&sDeviceId=354730010301566&appId=lls&token=" + get_token()
    ]
    custom_settings = {
        # 重试机制
        "RETRY_ENABLED": True,
        "RETRY_TIMES": 3,
        "COOKIES_ENABLED": False,
        "HTTPERROR_ALLOWED_CODES": [429, 401],  # 429的状态码不报错.401是token过期报错
        # "DOWNLOAD_DELAY": 0.2,
        "ITEM_PIPELINES": {
            'fast_fluent.pipelines.MysqlPipeline': 300},
        "DOWNLOADER_MIDDLEWARES": {
            # 'fast_fluent.middlewares.ProxyMiddleware': None,  # 代理不启用
            'fast_fluent.middlewares.ProxyMiddleware': 543,  # 代理启用
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

    def parse(self, response):
        # id_set = get_course_id()  # 从课程池里拿到新建的ID
        id_set = un_get_id()  # 拿到还未抓取的课程ID
        if id_set:
            for id in id_set:
                url = "https://apineo.llsapp.com/api/v1/courses/" + id + "?appVer=6&deviceId=354730011088642&sDeviceId=354730010301566&appId=lls&token=" + get_token()
                yield scrapy.Request(url, callback=self.parse_detail, dont_filter=True)
        else:
            print('今日数据已经抓取完毕')

    def parse_detail(self, response):
        courseitem = CourseItem()
        logger.info('详情页数据%s', response.text)
        if "操作过于频繁，请稍后再试" in response.text:
            yield scrapy.Request(url=response.url, callback=self.parse_detail, dont_filter=True)
        else:
            response_text = json.loads(response.text)
            courseitem["ID"] = response_text.get("id")
            courseitem["diamondPrice"] = response_text.get("diamondPrice") / 10  # 除以10,统一转换为人民币
            courseitem["studyUsersCount"] = response_text.get("studyUsersCount")
            courseitem["translatedTitle"] = response_text.get("translatedTitle")
            localtime = time.localtime(time.time())
            strtime = time.strftime("%Y-%m-%d", localtime)
            courseitem["times"] = strtime
            yield courseitem
