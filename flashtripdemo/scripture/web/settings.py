# coding: utf8
"""Configure"""

# Standard Library
import logging
import os

if os.environ.get('AT_US', None):
    DATABASES = {
        'scripture': 'mongodb://scripture_write:AYDBVmJqXEue353z@dds-rj92f2e050df2d541.mongodb.rds.aliyuncs.com:3717,dds-rj92f2e050df2d542.mongodb.rds.aliyuncs.com:3717/scripture?replicaSet=mgset-4391563',   # noqa pylint: disable=C0301
    }
    REDIS = 'redis://:ZbIm1XohoCmOdAKk@r-2ze1a1caa2705d14.redis.rds.aliyuncs.com:6379/2'
    CMS_API = 'https://api.weegotr.com'
    HTTP_PROXY = 'http://172.17.1.198:1118'
    HTTPS_PROXY = 'http://172.17.1.198:1118'
    SOLR = 'http://172.16.4.110:8080'
    LOG_LEVEL = "INFO"
    HUB_API_SID = 'da1109475ae1c7a9deec1a9c49b44460'
    PGSQL = {
        "record": (
            "postgres://tableau_rw:UErS0es3egqH@postgresql.feifanweige.com/record"
        )
    }
    LOGGER_HANDLER = ['web_terminal', "web_filestream"]

elif os.environ.get('IS_PRODUCTION'):
    SOLR = 'http://172.16.1.223'
    DATABASES = {
        'scripture': 'mongodb://scripture_writer:S8i82xsWKquS9CCBTd3wZA@'
                     'dds-2ze65b22201f9f141.mongodb.rds.aliyuncs.com:3717,'
                     'dds-2ze65b22201f9f142.mongodb.rds.aliyuncs.com:3717/'
                     'scripture?replicaSet=mgset-5392677',  # noqa
        'agent': 'mongodb://scripture_writer:S8i82xsWKquS9CCBTd3wZA@'
                 'dds-2ze65b22201f9f141.mongodb.rds.aliyuncs.com:3717,'
                 'dds-2ze65b22201f9f142.mongodb.rds.aliyuncs.com:3717/'
                 'scripture?replicaSet=mgset-5392677',
        'hub': 'mongodb://hub_write:hvAnfbwByFMG27tT@'
               'dds-2ze2ae2045feb3e41.mongodb.rds.aliyuncs.com:3717,'
               'dds-2ze2ae2045feb3e42.mongodb.rds.aliyuncs.com:3717/'
               'hub?replicaSet=mgset-4931065',
        'whotel': 'mongodb://whotel_writer:YiL39RGeROhV3PLVhAVn8Z@'
                  'dds-2ze65b22201f9f141.mongodb.rds.aliyuncs.com:3717,'
                  'dds-2ze65b22201f9f142.mongodb.rds.aliyuncs.com:3717/'
                  'whotel?replicaSet=mgset-5392677',
    }
    REDIS = 'redis://:ZbIm1XohoCmOdAKk@r-2ze1a1caa2705d14.redis.rds.aliyuncs.com:6379/2'
    CMS_API = 'https://api.weegotr.com'
    HTTP_PROXY = 'http://172.16.4.110:1090'
    HTTPS_PROXY = 'http://172.16.4.110:1090'
    QUOTES_API = "http://172.16.1.221/api/v2/hotel/availability"
    EXAMINER_API = "http://172.16.3.152"
    LOG_LEVEL = "INFO"
    HUB_API_SID = "da1109475ae1c7a9deec1a9c49b44460"
    PGSQL = {
        "record": (
            "postgres://tableau_rw:UErS0es3egqH@postgresql.feifanweige.com/record"
        )
    }
    LOGGER_HANDLER = ["web_filestream"]

else:
    SOLR = 'http://172.16.4.110:8983'
    DATABASES = {
        'scripture': 'mongodb://172.16.4.110:27017/scripture',
        'agent': 'mongodb://172.16.4.110:27017/scripture',
        'hub': 'mongodb://172.16.4.110:27017/hub',
        'whotel': 'mongodb://172.16.4.110:27017/whotel',
    }
    REDIS = 'redis://127.0.0.1:6379/2'
    CMS_API = 'http://172.16.4.110:8289'
    HTTP_PROXY = 'http://172.16.4.110:1090'
    HTTPS_PROXY = 'http://172.16.4.110:1090'
    # 线下经常新增或变更查价需求，因此线下也调用线上查价接口
    QUOTES_API = "http://172.16.1.221/api/v2/hotel/availability"
    HUB_API_SID = "da1109475ae1c7a9deec1a9c49b44461"
    EXAMINER_API = "http://localhost:4020"
    LOG_LEVEL = "DEBUG"
    PGSQL = {
        "record": (
            "postgres://order_writer:8SQp6F8gzw6gXfLzXYovhg@172.16.4.110/record"
        )
    } 
    LOGGER_HANDLER = ['web_terminal']

GOOGLE_OAUTH_CLIENT_ID = '902452316761-6fhp7r9h0hnada033kv09sif6e324fsq.apps.googleusercontent.com'  # noqa
GOOGLE_OAUTH_CLIENT_SECRET = 'XLQlP_Y6qjVmkZWfcUs5gmrS'


WEB_LOGGER = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            '()': 'web.utils.jsonformatter.JsonFormatter',
            'format': 'asctime,name,message,levelname',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'web_terminal': {
            'level': LOG_LEVEL,
            'formatter': 'default',
            'class': 'logging.StreamHandler',
        },
        "web_filestream": {
            "filename": "logs/web/web.log",
            "level": LOG_LEVEL,
            "formatter": "default",
            "class": "logging.handlers.TimedRotatingFileHandler",
            'when': 'midnight',
            'interval': 1,
        },
    },
    'loggers': {
        '': {
            'handlers': LOGGER_HANDLER,
            'level': LOG_LEVEL,
        }
    }
}

SUPPLIER_NAME_2_ID = {
        'hotelbeds': "59c1f0f8e1812033000e1de8",
        "hotelspro": '59b0b048a389295de92f4815',
        'relux': '5bc41308bca48f00449c431d',
        "bonotel": '59b20729a389295de92f4952',
        "jactravel": '59b0b035a389295de92f4814',
        'roomsxml': '59afe1e0a389295de92f47f8',
        'whotel': '5aebd3ba037086003ed59b85',
        'weegotr': '5a2a83b2ebc2012b94df1e9e',
        'travflex': '5c05e9cfbdd0450040234763'
    }
SUPPLIER_ID_2_NAME = {
        "59c1f0f8e1812033000e1de8": 'hotelbeds',
        '59b0b048a389295de92f4815': "hotelspro",
        '5bc41308bca48f00449c431d': 'relux',
        '59b20729a389295de92f4952': "bonotel",
        '59b0b035a389295de92f4814': "jactravel",
        '59afe1e0a389295de92f47f8': 'roomsxml',
        '5aebd3ba037086003ed59b85': 'whotel',
        '5a2a83b2ebc2012b94df1e9e': 'weegotr',
        '5c05e9cfbdd0450040234763': 'travflex'
    }
SUPPLIER_NAME_2_COLL = {
    'hotelbeds': 'statics.hotels.hotelbeds',
    'hotelspro': 'statics.hotels.hotelspro',
    'relux': 'statics.hotels.relux',
    'bonotel': 'statics.hotels.bonotel',
    'jactravel': "statics.hotels.jactravel",
    'roomsxml': 'statics.hotels.roomsxml',
    'whotel': 'wg_hotels',
    'travflex': 'statics.hotels.travflex'
}
SUPPLIER_ID_2_COLL = {
    '59c1f0f8e1812033000e1de8': 'statics.hotels.hotelbeds',
    '59b0b048a389295de92f4815': 'statics.hotels.hotelspro',
    '5bc41308bca48f00449c431d': 'statics.hotels.relux',
    '59b20729a389295de92f4952': 'statics.hotels.bonotel',
    '59b0b035a389295de92f4814': "statics.hotels.jactravel",
    '59afe1e0a389295de92f47f8': 'statics.hotels.roomsxml',
    '5a2a83b2ebc2012b94df1e9e': 'weegotr',
    '5aebd3ba037086003ed59b85': 'whotel',
    '5c05e9cfbdd0450040234763': 'statics.hotels.travflex'
}
SUPPLIER_ID_2_INDEX = {
    '59c1f0f8e1812033000e1de8': 5,
    '59b0b048a389295de92f4815': 6,
    '5bc41308bca48f00449c431d': 7,
    '59b20729a389295de92f4952': 8,
    '59b0b035a389295de92f4814': 9,
    '59afe1e0a389295de92f47f8': 10,
    '5a2a83b2ebc2012b94df1e9e': 11,
    '5aebd3ba037086003ed59b85': 12,
    '5c05e9cfbdd0450040234763': 13
}
SUPPLIER_QUERY = {
    'hotelbeds': {'name': '1', 'address': '1', 'latitude': '1', 'longitude': '1', 'telephone': '1', 'province': '1', 'web': '1', 'website': '1'},
    'hotelspro': {'name': '1', 'name_cn': '1', 'address': '1', 'latitude': '1', 'longitude': '1', 'phone': '1', 'province': '1'},
    'relux': {
        'name': '1', 'name_cn': '1',
        'address': '1', 'latitude': '1',
        'longitude': '1', 'tel': '1', 'url': '1',
        'gallery': '1', 'policy_cn': '1', 'traffic_info_cn': '1',
        'facility_cn': '1', 'description_cn': '1',
        'ruby': '1',
        },
    'bonotel': {'name': '1', 'address': '1', 'latitude': '1', 'longitude': '1', 'phone': '1', 'province': '1', 'wgstar': '1'},
    'jactravel': {'name': '1', 'address': '1', 'latitude': '1', 'longitude': '1', 'phone': '1', 'province': '1'},
    'whotel': {'name_en': '1', 'name_cn': '1', 'address': '1', 'website': '1', 'telephone': '1', 'rating': '1',},
    'roomsxml': {'name': '1', 'address': '1', 'latitude': '1', 'longitude': '1', 'website': '1', 'wgstar': '1', 'phone': '1'},
    'travflex': {
        'name': '1', 'address': '1', 'latitude': '1', 'longitude': '1', 'wgstar': '1'
    }
}
CRAWLING_WEBSITE = ["bk_url", "hcom_id", "ta"]
DESTINATION_2_TABLE = {
    'country': 'meta_countries',
    'province': 'meta_provinces',
    'city': 'meta_cities',
    'countries': 'meta_countries',
    'provinces': 'meta_provinces',
    'cities': 'meta_cities'
}

STAGES = [
    "availability",
    "preparation",
    "booking",
    "cancellation"
]
RELUX_FORBIDDEN_ROOM_TYPE_WORD = [
    '会员楼层', '和室', '洋室', '和洋室', '早餐',
    '用餐', '浴室', '㎡', '天领', '卧龙',
    '宫', '重新装潢', '[仅限]', '[附]', '【仅限】',
    '【附】', '幽石', '忘筅', '之间', '馆',
    '侧', '风', '庵', '流水', '行云',
    '离间', '屋', '面窗', '最多', '母屋',
    '叠', '邸', '《', '》',
]

REDIS_EXPIRE_TIME = 7 * 24 * 60 * 60
CHECK_PRICE_DELAY_TIME = 3 * 60 * 60
COMPARE_TIME_PERIOD = 300000 # 5 * 60 * 1000