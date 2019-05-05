import json
import math

import time

import scrapy

from determine_crawl import get_user
from fast_fluent.items import UserItem
from fast_fluent.starturl_list2 import start_url_list, get_token


class Index(scrapy.Spider):
    name = 'Index'
    # 从首页进入
    start_urls = start_url_list()  # 自定义函数，返回的是去重后的用户url

    custom_settings = {
        "RETRY_ENABLED": True,
        "RETRY_TIMES": 3,
        "COOKIES_ENABLED": False,
        "HTTPERROR_ALLOWED_CODES": [429],  # 429的状态码不报错
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            'Accept-Language': "zh-cn",
            'User-Agent': "Lingome/5.0 (SM-G955N;Android 4.4.2;)",
            'Accept-Encoding': "gzip,deflate",
            'Host': "apineo.llsapp.com",
            'cache-control': "no-cache",
            'Postman-Token': "84832b9d-0516-4748-a7d5-265d9ca0736d"
        }
    }

    # 流利说的粉丝数比较大的用户
    def parse(self, response):
        response_text = json.loads(response.text)
        user_id = response_text.get('user').get('id')
        url = "http://apineo.llsapp.com/api/v1/users/" + user_id + "/profile?appId=lls&deviceId=354730011650847&sDeviceId=354730010301566&appVer=4&token=" + get_token()
        yield scrapy.Request(url, callback=self.parse_detail)

    # 粉丝页
    def follow_list(self, response):
        users = json.loads(response.text).get('users')
        for user in users:
            user_id = user.get('id')
            user_count = get_user(user_id)  # 判断这个数据是否已经抓取过，返回0或者1，0是为抓取，1为已经入库
            if user_count == 1:  # 只有粉丝页才需要做这个判断
                print('当前用户已经入库')
                pass
            if user_count == 0:
                url = "http://apineo.llsapp.com/api/v1/users/" + user_id + "/profile?appId=lls&deviceId=354730011650847&sDeviceId=354730010301566&appVer=4&token=" + get_token()
                yield scrapy.Request(url, callback=self.parse_detail)

    # 用户详情页
    def parse_detail(self, response):
        user_detail = json.loads(response.text)
        useritem = UserItem()
        user = user_detail.get('user')
        useritem['id'] = user.get('id')
        useritem['repliesCount'] = user.get('repliesCount')  # 回复数
        useritem['topicsCount'] = user.get('topicsCount')  # 发表帖子数
        useritem['coins'] = user.get('coins')  # 金币数
        useritem['stars'] = user.get('stars')  # 星星数
        useritem['nick'] = user.get('nick')  # 昵称
        useritem['gender'] = user.get('gender')  # 性别
        useritem['birthYear'] = user.get('birthYear')  # 出生年份
        useritem['location'] = user.get('location')  # 出生地
        useritem['profession'] = user.get('profession')  # 职业
        useritem['level'] = user.get('level')  # 等级
        useritem['followersCount'] = user_detail.get('followersCount')  # 粉丝数
        useritem['followingsCount'] = user_detail.get('followingsCount')  # 关注数
        useritem['dialogCount'] = user_detail.get('dialogCount')  # 闯关总数
        useritem['nonstopStudyDays'] = user_detail.get('nonstopStudyDays')  # 连续学习天数
        useritem['studyDays'] = user_detail.get('studyDays')  # 累计学习天数
        useritem['dialogAvgScore'] = user_detail.get('dialogAvgScore')  # 闯关平均分
        useritem['theSpeakingForce'] = user_detail.get('theSpeakingForce')  # 口语力
        useritem['rank'] = user_detail.get('rank')  # 超过多少的人
        useritem['recordTime'] = user_detail.get('recordTime')  # 录音总计秒

        yield useritem
        followersCount = useritem['followersCount']
        followingsCount = useritem['followingsCount']
        user_id = useritem['id']
        # 如果 粉丝数大于0
        if followersCount > 0:
            followers_maxpage = math.ceil(followersCount / 20)  # 向上取整
            followers_maxpage += 1
            for page in range(1, int(followers_maxpage)):
                url = "https://apineo.llsapp.com/api/v1/users/" + user_id + "/followers?page=" + str(
                    page) + "&pageSize=20&appId=lls&deviceId=354730010301566&sDeviceId=354730010301566&appVer=4&token=" + get_token()
                yield scrapy.Request(url, callback=self.follow_list)
        # 为了提高抓取速率,不重复抓取,我们只关注粉丝,
        # 如果关注数大于0
        # if followingsCount > 0:
        #     following_maxpage = math.ceil(followingsCount / 20)  # 向上取整
        #     following_maxpage += 1
        #     for page in range(1, int(following_maxpage)):
        #         url = "https://apineo.llsapp.com/api/v1/users/" + user_id + "/followings?page=" + str(
        #             page) + "&pageSize=20&appId=lls&deviceId=354730010301566&sDeviceId=354730010301566&appVer=4&token=" + get_token()
        #         yield scrapy.Request(url, callback=self.follow_list)
