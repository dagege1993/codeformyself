# -*- coding: utf-8 -*-

# Scrapy settings for scripture project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = "scripture"

SPIDER_MODULES = ["scripture.spiders"]
NEWSPIDER_MODULE = "scripture.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'scripture (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Enable splash
SPLASH_URL = "http://127.0.0.1:8040"
# SPLASH_URL = 'http://172.17.1.198:8050'
# SPLASH_URL = 'http://splash.c7d3b2b0f81e141ca9494fc888ca56132.cn-beijing.alicontainer.com'
# SPLASH_URL = 'http://172.17.0.214:8050'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 60

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0
# DOWNLOAD_DELAY = 5
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 60
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'scripture.middlewares.ScriptureSpiderMiddleware': 543,
# }
SPIDER_MIDDLEWARES = {"scrapy_splash.SplashDeduplicateArgsMiddleware": 100}

# Set a custom DUPEFILTER_CLASS:
# DUPEFILTER_CLASS = "scrapy_splash.SplashAwareDupeFilter"
# If you use Scrapy HTTP cache then a custom cache storage backend is required.
# scrapy-splash provides a subclass of scrapy.contrib.httpcache.FilesystemCacheStorage:
HTTPCACHE_STORAGE = "scrapy_splash.SplashAwareFSCacheStorage"
# Enable debugging cookies in the `SplashCookiesMiddleware`.
SPLASH_COOKIES_DEBUG = True

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'scripture.middlewares.MyCustomDownloaderMiddleware': 543,
# }
DOWNLOADER_MIDDLEWARES = {
    "scrapy_splash.SplashCookiesMiddleware": None,
    "scrapy_splash.SplashMiddleware": 725,
    "scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware": 810,
    # "scrapy.downloadermiddlewares.redirect.RedirectMiddleware": 999,
    # 'scripture.middlewares.SeleniumDownloadMiddleware': 500,
    "scripture.middlewares.UserAgentMiddleware": 400,
    "scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware": None,
    "scripture.middlewares.LocalRetryMiddleware": 302,
    # 'scripture.middlewares.AutoProxyMiddleware': None,
    'scripture.middlewares.ProxyMiddleware': 543,

    "scripture.middlewares.JsetCompatibleMiddleware": 398,
    # 'scripture.middlewares.HotelsFilterMiddleware': 399,
    "scripture.middlewares.HtmlSaverMiddleware": 401,
    "scripture.middlewares.DingDingMiddleware": 100,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
EXTENSIONS = {"scrapy.extensions.telnet.TelnetConsole": None}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'scripture.pipelines.ScripturePipeline': 300,
# }
ITEM_PIPELINES = {
    "scripture.pipelines.MongoPipeline": 300,
    "scripture.pipelines.GalleryPipeline": 299,
    # 'scrapy_redis.pipelines.RedisPipeline': 400
    # "scripture.pipelines.MatchingPipeline": 400,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# Standard Library
###############################################################################
# local settings
###############################################################################
# mongodb uri
import os

if os.environ.get("AT_US", None):
    MONGO = "mongodb://scripture_write:AYDBVmJqXEue353z@dds-rj92f2e050df2d541.mongodb.rds.aliyuncs.com:3717,dds-rj92f2e050df2d542.mongodb.rds.aliyuncs.com:3717/scripture?replicaSet=mgset-4391563"
    HUB_MONGO = "mongodb://hub_write:hvAnfbwByFMG27tT@dds-2ze2ae2045feb3e41.mongodb.rds.aliyuncs.com:3717,dds-2ze2ae2045feb3e42.mongodb.rds.aliyuncs.com:3717/hub?replicaSet=mgset-4931065"
    AI_MONGO = "mongodb://hub_write:hvAnfbwByFMG27tT@dds-rj92f2e050df2d541.mongodb.rds.aliyuncs.com:3717,dds-rj92f2e050df2d542.mongodb.rds.aliyuncs.com:3717/hub?replicaSet=mgset-4391563"
    REDIS_URL = 'redis://:ZbIm1XohoCmOdAKk@r-2ze1a1caa2705d14.redis.rds' \
                '.aliyuncs.com:6379/2'
    DINGTALK_ACCESS_TOKEN = 'e794af17cbb02db3010d98bc832713f8935037622427e289c714868d880c56f9'
    LOG_LEVEL = "INFO"
    DOWNLOAD_HTML = False
    PRICES_DING_TOKEN = '67432a424d3c76c13ac380dff16c8d8bfb61fc22e93e15f4183955ff7c5dd61a'
elif os.environ.get("IS_PRODUCTION", None):
    MONGO = 'mongodb://scripture_writer:S8i82xsWKquS9CCBTd3wZA@' \
            'dds-2ze65b22201f9f141.mongodb.rds.aliyuncs.com:3717,' \
            'dds-2ze65b22201f9f142.mongodb.rds.aliyuncs.com:3717/' \
            'scripture?replicaSet=mgset-5392677'
    HUB_MONGO = "mongodb://hub_write:hvAnfbwByFMG27tT@dds-2ze2ae2045feb3e41.mongodb.rds.aliyuncs.com:3717,dds-2ze2ae2045feb3e42.mongodb.rds.aliyuncs.com:3717/hub?replicaSet=mgset-4931065"
    AI_MONGO = "mongodb://hub_write:hvAnfbwByFMG27tT@dds-rj92f2e050df2d541.mongodb.rds.aliyuncs.com:3717,dds-rj92f2e050df2d542.mongodb.rds.aliyuncs.com:3717/hub?replicaSet=mgset-4391563"
    REDIS_URL = 'redis://:ZbIm1XohoCmOdAKk@r-2ze1a1caa2705d14.redis.rds' \
                '.aliyuncs.com:6379/2'
    DINGTALK_ACCESS_TOKEN = 'e794af17cbb02db3010d98bc832713f8935037622427e289c714868d880c56f9'
    LOG_LEVEL = "INFO"
    DOWNLOAD_HTML = False
    PRICES_DING_TOKEN = '67432a424d3c76c13ac380dff16c8d8bfb61fc22e93e15f4183955ff7c5dd61a'
else:
    MONGO = "mongodb://172.16.4.110:27017/scripture"
    REDIS_URL = 'redis://127.0.0.1:6379/2'
    DINGTALK_ACCESS_TOKEN = "a62b85f7b99970415b11c866b75ee4f6b185c02f460acbb928c6a56dab57612f"
    LOG_LEVEL = "INFO"
    DOWNLOAD_HTML = False
    PRICES_DING_TOKEN = "a62b85f7b99970415b11c866b75ee4f6b185c02f460acbb928c6a56dab57612f"

AGENT_DB = (
    "mongodb://scripture_writer:S8i82xsWKquS9CCBTd3wZA@"
    "dds-2ze65b22201f9f141.mongodb.rds.aliyuncs.com:3717,"
    "dds-2ze65b22201f9f142.mongodb.rds.aliyuncs.com:3717/"
    "scripture?replicaSet=mgset-5392677"
)

# Baidu Translate Api
BAIDU_TRANSLATE = {
    "HOST": "https://fanyi-api.baidu.com",
    "URI": "/api/trans/vip/translate",
    "SECRET": "g7xdIRqc5bAMfhIYW2Il",
    "APPID": "20170512000047180",
}

GOOGLE_GEO_KEY = "AIzaSyBZ0NPcFi-t38QR4BbOSDnaXlx5oR7fzOk"

# User-Agent
USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;  Trident/5.0)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0;  Trident/5.0)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36 OPR/44.0.2510.1449",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36 OPR/45.0.2552.812",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/603.2.5 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.5",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/58.0.3029.110 Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/58.0.3029.81 Chrome/58.0.3029.81 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/58.0.3029.96 Chrome/58.0.3029.96 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36",
]

HTTP_PROXY = "http://127.0.0.1:8123"

# 启用Redis调度存储请求队列
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# 确保所有的爬虫通过Redis去重
DUPEFILTER_CLASS = "scripture.middlewares.dupefilter.ScriptureDupefilter"

# 不清除Redis队列、这样可以暂停/恢复 爬取
SCHEDULER_PERSIST = True

DUPEFILTER_DEBUG = True

GOOGLE_TRANSLATE_SERVICE = ["translate.google.cn"]

import logging.config

SCRIPTURE_LOGGER = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s - %(name)s: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'scripture_terminal': {
            'level': LOG_LEVEL,
            'formatter': 'default',
            'class': 'logging.StreamHandler',
        },
        "scripture_filestream": {
            "filename": "logs/scripture/scripture.log",
            "level": LOG_LEVEL,
            "formatter": "default",
            "class": "logging.handlers.TimedRotatingFileHandler",
            'when': 'D',
            'interval': 1,
            'backupCount': 30,
        },
    },
    'loggers': {
        'scripture': {
            'handlers': ['scripture_terminal', "scripture_filestream"],
            'level': LOG_LEVEL,
            "propagate": False,
        }
    }
}
logging.config.dictConfig(SCRIPTURE_LOGGER)
OSS_SCRIPTURE_ENDPOINT = "http://oss-cn-beijing-internal.aliyuncs.com"
OSS_SCRIPTURE_ACCESS_KEY_ID = "LTAIwHXVgRkPRxcw"
OSS_SCRIPTURE_ACCESS_KEY_SECRET = "PCm6kdpeyjAG2gJz4B4C2js3TIifrc"
OSS_SCRIPTURE_BUCKET = "weegotr-backups"

CELERY_BROKER = "redis://:ZbIm1XohoCmOdAKk@r-2ze1a1caa2705d14.redis.rds.aliyuncs.com:6379/8"
CELERY_BACKEND = "redis://:ZbIm1XohoCmOdAKk@r-2ze1a1caa2705d14.redis.rds.aliyuncs.com:6379/9"
