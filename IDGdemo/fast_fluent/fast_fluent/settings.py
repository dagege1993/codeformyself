# -*- coding: utf-8 -*-

# Scrapy settings for fast_fluent project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import datetime

BOT_NAME = 'fast_fluent'

SPIDER_MODULES = ['fast_fluent.spiders']
NEWSPIDER_MODULE = 'fast_fluent.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'fast_fluent (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'fast_fluent.middlewares.FastFluentSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'fast_fluent.middlewares.ProxyMiddleware': 543,
    "scrapy.downloadermiddlewares.redirect.RedirectMiddleware": None,
    "fast_fluent.middlewares.LocalRetryMiddleware": 302
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'fast_fluent.pipelines.MongodbPipeline': 300,
}
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
HOST = 'localhost'
PORT = 27017
# MONGODB_HOST = 'localhost'
MONGODB_HOST = '192.168.103.31'
MONGODB_PORT = 27017
MONGODB_DBNAME = 'fluent'
MONGODB_DOCNAME = 'user1115'

MYSQL_HOST = "192.168.103.31"
# MYSQL_HOST = "localhost"
MYSQL_DBNAME = "fluent"
MYSQL_USER = "root"
MYSQL_PASSWORD = "adminadmin"
# 自定义重试状态码
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429, 401]  # 429是请求过于频繁,401是token过期,

# 提升抓取速度的配置
# LOG_LEVEL = ''
# LOG_LEVEL = 'ERROR'
LOG_LEVEL = 'WARNING'
from datetime import datetime

today = datetime.now()
log_file_path = "logs/{}-{}-{}.log".format(today.year, today.month, today.day)
LOG_FILE = log_file_path
CONCURRENT_REQUESTS = 100
CONCURRENT_REQUESTS_PER_DOMAIN = 100
CONCURRENT_REQUESTS_PER_IP = 100
DOWNLOAD_TIMEOUT = 15  # 其中15是设置的下载超时时间
