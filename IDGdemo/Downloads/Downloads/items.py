# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DownloadsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ThreeItem(scrapy.Item):
    # define the fields for your item here like:

    id = scrapy.Field()
    name = scrapy.Field()
    software = scrapy.Field()  # 软件或游戏
    downloads_nums = scrapy.Field()
    types = scrapy.Field()
    crawl_time = scrapy.Field()
    pkgname = scrapy.Field()  # 包名字
    versionname = scrapy.Field()  # 版本号


class sqlItem(scrapy.Item):
    log_id = scrapy.Field()
    stat_dt = scrapy.Field()
    in_dt = scrapy.Field()  # 这两个字段都是时间
    source = scrapy.Field()
    cate = scrapy.Field()
    sort = scrapy.Field()
    sub = scrapy.Field()
    app_id = scrapy.Field()
    app_name = scrapy.Field()
    app_keys = scrapy.Field()
    downs = scrapy.Field()
    top_num = scrapy.Field()  # 按照抓取顺序
    dt_type = scrapy.Field()  # 确定是周数据还是月数据
    app_md5 = scrapy.Field()
    pkgname = scrapy.Field()  # 包名字
    versionname = scrapy.Field()  # 版本号
    category_lv3 = scrapy.Field()  # 360手机助手三级类,方便做统计是否抓全
    page_num = scrapy.Field()  # 360手机助手页数,确定是否抓全
