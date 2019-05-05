# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FastFluentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CourseItem(scrapy.Item):
    # define the fields for your item here like:
    ID = scrapy.Field()
    diamondPrice = scrapy.Field()
    studyUsersCount = scrapy.Field()
    translatedTitle = scrapy.Field()  # 节目名字
    times = scrapy.Field()  # 抓取 时间
    insert_time = scrapy.Field()  # 抓取 时间


class UserItem(scrapy.Item):
    id = scrapy.Field()
    repliesCount = scrapy.Field()  # 回复数
    topicsCount = scrapy.Field()  # 发表帖子数
    coins = scrapy.Field()  # 金币数
    stars = scrapy.Field()  # 星星数
    nick = scrapy.Field()  # 昵称
    gender = scrapy.Field()  # 性别
    profession = scrapy.Field()  # 职业
    level = scrapy.Field()  # 等级
    followersCount = scrapy.Field()  # 粉丝数
    followingsCount = scrapy.Field()  # 关注数
    dialogCount = scrapy.Field()  # 闯关总数
    nonstopStudyDays = scrapy.Field()  # 连续学习天数
    studyDays = scrapy.Field()  # 累计学习天数
    dialogAvgScore = scrapy.Field()  # 累计学习天数
    theSpeakingForce = scrapy.Field()  # 口语力
    rank = scrapy.Field()  # 累计学习天数
    recordTime = scrapy.Field()  # 录音总计秒
    birthYear = scrapy.Field()  # 出生年份
    location = scrapy.Field()  # 出生地点
