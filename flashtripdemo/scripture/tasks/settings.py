# coding: utf8

import os
import warnings

GOOGLE_GEO_KEY = 'AIzaSyBZ0NPcFi-t38QR4BbOSDnaXlx5oR7fzOk'
GOOGLE_CLIENT_SECRET = '902452316761-6fhp7r9h0hnada033kv09sif6e324fsq.apps.googleusercontent.com'  # noqa pylint: disable=C0301
GOOGLE_CLIENT_ID = 'XLQlP_Y6qjVmkZWfcUs5gmrS'

ALIYUN_ACCESS_KEY_ID = 'LTAIwHXVgRkPRxcw'
ALIYUN_ACCESS_KEY_SECRET = 'PCm6kdpeyjAG2gJz4B4C2js3TIifrc'
ALIYUN_CDN_ACCESS_KEY_ID = 'LTAItMIppKbN3agn'
ALIYUN_CDN_ACCESS_KEY_SECRET = '84wMilAFeJQ8iHkXo4jSj93EA68IZe'

if os.environ.get('AT_US', None):
    BROKER = 'redis://127.0.0.1:6379/8'
    BACKEND = 'redis://127.0.0.1:6379/9'
    REDIS = 'redis://127.0.0.1:6379/2'
    DATABASES = {
        'scripture': 'mongodb://scripture_write:AYDBVmJqXEue353z@dds-rj92f2e050df2d541.mongodb.rds.aliyuncs.com:3717,dds-rj92f2e050df2d542.mongodb.rds.aliyuncs.com:3717/scripture?replicaSet=mgset-4391563',
    # noqa pylint: disable=C0301
        'hub': 'mongodb://hub_write:hvAnfbwByFMG27tT@dds-rj92f2e050df2d541.mongodb.rds.aliyuncs.com:3717,dds-rj92f2e050df2d542.mongodb.rds.aliyuncs.com:3717/hub?replicaSet=mgset-4391563',
    # noqa pylint: disable=C0301
        'ai': 'mongodb://hub_write:hvAnfbwByFMG27tT@dds-rj92f2e050df2d541.mongodb.rds.aliyuncs.com:3717,dds-rj92f2e050df2d542.mongodb.rds.aliyuncs.com:3717/hub?replicaSet=mgset-4391563'
    # noqa pylint: disable=C0301
    }
    LOG_LEVEL = "INFO"
    DINGTALK_NOTIFY = {
        '': 'e794af17cbb02db3010d98bc832713f8935037622427e289c714868d880c56f9',
        'provider': '990ffdbc22d9544e7168f20cd89c6cab307f7f112c2c6a9b34de16249b5baaea'
        }
    GET_COMMENTS = 'http://scripture.weegotr.com/api/v1/comments/ta'
    UPLOAD_HOTEL = 'http://scripture.weegotr.com/api/v1/creating/hotel'
    CMS_API = 'https://api.weegotr.com'
    QUOTES = "http://172.16.1.221"
elif os.environ.get('IS_PRODUCTION', None):
    BROKER = 'redis://:ZbIm1XohoCmOdAKk@r-2ze1a1caa2705d14.redis.rds.aliyuncs.com:6379/8'
    BACKEND = 'redis://:ZbIm1XohoCmOdAKk@r-2ze1a1caa2705d14.redis.rds.aliyuncs.com:6379/9'
    REDIS = 'redis://:ZbIm1XohoCmOdAKk@r-2ze1a1caa2705d14.redis.rds.aliyuncs.com:6379/2'
    DATABASES = {
        'scripture': 'mongodb://scripture_writer:S8i82xsWKquS9CCBTd3wZA@'
                     'dds-2ze65b22201f9f141.mongodb.rds.aliyuncs.com:3717,'
                     'dds-2ze65b22201f9f142.mongodb.rds.aliyuncs.com:3717/'
                     'scripture?replicaSet=mgset-5392677',
        'agent': 'mongodb://scripture_writer:S8i82xsWKquS9CCBTd3wZA@'
                 'dds-2ze65b22201f9f141.mongodb.rds.aliyuncs.com:3717,'
                 'dds-2ze65b22201f9f142.mongodb.rds.aliyuncs.com:3717/'
                 'scripture?replicaSet=mgset-5392677',
        'hub': 'mongodb://hub_write:hvAnfbwByFMG27tT@'
               'dds-2ze2ae2045feb3e41.mongodb.rds.aliyuncs.com:3717,'
               'dds-2ze2ae2045feb3e42.mongodb.rds.aliyuncs.com:3717/'
               'hub?replicaSet=mgset-4931065',
        'ai': ''
    }
    LOG_LEVEL = "INFO"
    DINGTALK_NOTIFY = {
        '': 'e794af17cbb02db3010d98bc832713f8935037622427e289c714868d880c56f9',
        'provider': '990ffdbc22d9544e7168f20cd89c6cab307f7f112c2c6a9b34de16249b5baaea'
        }
    GET_COMMENTS = 'http://scripture.weegotr.com/api/v1/comments/ta'
    UPLOAD_HOTEL = 'http://scripture.weegotr.com/api/v1/creating/hotel'
    CMS_API = 'https://api.weegotr.com'
    QUOTES = "http://172.16.4.113:8000"
else:
    BROKER = 'redis://127.0.0.1:6379/8'
    BACKEND = 'redis://127.0.0.1:6379/9'
    REDIS = 'redis://127.0.0.1:6379/2'
    DATABASES = {
        'scripture': 'mongodb://172.16.4.110:27017/scripture',
        'agent': 'mongodb://172.16.4.110:27017/scripture',
        'hub': 'mongodb://172.16.4.110:27017/hub',
        'ai': 'mongodb://172.16.4.110:27017/hub',
    }
    LOG_LEVEL = "DEBUG"
    DINGTALK_NOTIFY = {
        '': "a62b85f7b99970415b11c866b75ee4f6b185c02f460acbb928c6a56dab57612f",
        'provider': 'a62b85f7b99970415b11c866b75ee4f6b185c02f460acbb928c6a56dab57612f',
    }
    GET_COMMENTS = 'http://localhost:4010/api/v1/comments/ta'
    UPLOAD_HOTEL = 'http://localhost:4010/api/v1/creating/hotel'
    CMS_API = 'http://172.16.4.110:8289'
    QUOTES = "http://172.16.1.221"
PROXIES = {
    'http': 'http://172.16.4.110:1090',
    'https': 'https://172.16.4.110:1090'
}

ALLOW_DOMAIN = [
    'booking.com',
    'opentable',
    'agoda',
    'hotels',
    'americanairlines',
    'united',
    'expedia',
    'priceline',
    'delta',
    'spg',
    'marriott',
    'hilton',
    'hyatt',
    'ihg',
    'accor',
    'us airlines',
    'british airways',
    'wyndham',
    'travelzoo',
    'tripadvisor'
]

INFLUXDB = 'http://172.16.2.199:8086/write'
PARITY = 'http://172.17.0.216:8100/api/v1/portal'

OSS_ACCESS_KEY_ID = 'LTAIwHXVgRkPRxcw'
OSS_SECRET_ACCESS_KEY = 'PCm6kdpeyjAG2gJz4B4C2js3TIifrc'
OSS_ENDPOINT = 'http://oss-cn-beijing-internal.aliyuncs.com'
OSS_BUCKET = 'weegotr-statics'


CELERY_LOGGER = {
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
        'tasks_terminal': {
            'level': LOG_LEVEL,
            'formatter': 'default',
            'class': 'logging.StreamHandler',
        },
        "tasks_filestream": {
            "filename": "logs/tasks/tasks.log",
            "level": LOG_LEVEL,
            "formatter": "default",
            "class": "logging.handlers.TimedRotatingFileHandler",
            'when': 'D',
            'interval': 1,
            'backupCount': 30,
        },
    },
    'loggers': {
        'celery.task': {
            'handlers': ['tasks_terminal', "tasks_filestream"],
            'level': LOG_LEVEL,
            "propagate": False,
        },
        'celery.worker': {
            'handlers': ['tasks_terminal', "tasks_filestream"],
            'level': LOG_LEVEL,
            "propagate": False,
        },
        'tasks': {
            'handlers': ['tasks_terminal', "tasks_filestream"],
            'level': LOG_LEVEL,
            "propagate": False,
        }
    }
}


CHECK_PRICE_FREQUENCY = 10
CHECK_PRICE_SIMILARITY = 0.5

BUG_PRICE_TASK_TIMEDELTA = 5 # minute
BUG_PRICE_TASK_STARTTIME = (6, 0 ,0) # day_of_week, hour, minute

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

BAIDU_STATICS = {
    'account': {
        "token": "cbffc598129128bb6700680054aab8aa",
        "username": "Flashtrip",
        "password": "Flashtrip123",
        "site_id": "12798669"
    },
    "receivers": "zhujiayao@weego.me,zhangzhenqiang@weego.me",
    "from": "reservation@flashtrip.cn"
}

EMAIL_ACCOUNT = {
    "host": "smtp.mxhichina.com",
    "port": 465,
    "user": "reservation@flashtrip.cn",
    "password": "Dingdan1122"
}

try:
    from .local_settings import *  # noqa
except ImportError:
    warnings.warn('tasks.local_settings is missing!')
