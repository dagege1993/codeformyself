# coding: utf8
"""Application of celery
Created by: songww
"""

# Standard Library
import os
import logging.config

from celery import Celery
from celery.schedules import crontab
from tasks import settings
from tasks.utils.register import register

app = Celery(  # pylint: disable=c0103
    "scripture", broker=settings.BROKER, backend=settings.BACKEND
)

app.conf.worker_max_tasks_per_child = 200
app.conf.worker_max_memory_per_child = 256000
logging.config.dictConfig(settings.CELERY_LOGGER)

if os.environ.get("AT_US", None):
    settings.PROXIES = None
    app.conf.beat_schedule = {
        "fetch_g_news_every_day": {
            "task": "tasks.gnews.make_requests",
            "schedule": crontab(hour=5, minute=30),
            "args": (),
        }
    }

    register("tasks.gnews")
    register("tasks.gmail")

else:
    app.conf.beat_schedule = {
        "send_4xxcdnlogs_every_day": {
            "task": "tasks.alicdn.audit_cdn_logs",
            "schedule": crontab(hour=2, minute=30),
            "args": (),
        },
        # "packeage-price-checker-every-day": {
        #     "task": "tasks.package_prices.packages",
        #     "schedule": crontab(hour=0, minute=30),
        #     "args": (),
        # },
        # 流量投放暂未开始，供应商(hotelspro)反馈查询过多，暂停
        # "hotel-online-check": {
        #     "task": "tasks.inventories.hotel_online_check",
        #     "schedule": crontab(hour='5,17'),
        #     "args": (),
        # },
        "hotel-price-calendar": {
            "task": "tasks.inventories.calendar_all",
            "schedule": crontab(hour='0-23/4', minute=0),
            "args": (),
        },
        # 'fetch_new_proxies': {
        #     'task': 'tasks.proxy.update_proxies',
        #     'schedule': crontab(minute='*/10'),
        #     'args': ()
        # },
        # 'validate_exists_proxies': {
        #     'task': 'tasks.proxy.validate_exists',
        #     'schedule': crontab(minute='*/10'),
        #     'args': ()
        # },
        # 'push_price_from_parity_to_influxdb': {
        #     'task': 'tasks.crawlers.prices.booking_com',
        #     'schedule': crontab(minute=1, hour=17),
        #     'args': ()
        # }
        'update_statics_bonotel': {
            'task': 'tasks.supplier_statics.update_bonotel',
            'schedule': crontab(minute='10', hour='15', day_of_week='6'),
            'args': ()
        },
        'update_statics_hotelbeds': {
            'task': 'tasks.supplier_statics.update_hotelbeds',
            'schedule': crontab(minute='10', hour='15', day_of_week='6'),
            'args': ()
        },
        'update_statics_hotelspro': {
            'task': 'tasks.supplier_statics.update_hotelspro',
            'schedule': crontab(minute='10', hour='15', day_of_week='6'),
            'args': ()
        },
        'update_statics_reluxhotels': {
            'task': 'tasks.supplier_statics.update_relux_hotels',
            'schedule': crontab(hour='18', minute='30'),
            'args': ()
        },
        'update_statics_reluxrooms': {
            'task': 'tasks.supplier_statics.update_relux_rooms',
            'schedule': crontab(hour='18', minute='0'),
            'args': ()
        },
        'update_online_hotel_statics_data': {
            'task': 'tasks.supplier_statics.update_online_hotel_statics_data',
            'schedule': crontab(hour='9', minute='0'),
            'args': ()
        },
        'update_traveflex_hotel_code': {
            'task': 'tasks.supplier_statics.update_traveflex_hotel_code',
            'schedule': crontab(day_of_month='28', hour='12', minute='0'),
            'args': ()
        },
        'update_bug_price': {
            'task': 'tasks.inventories.bug_price_all',
            'schedule': crontab(
                day_of_week=str(settings.BUG_PRICE_TASK_STARTTIME[0]), 
                hour=str(settings.BUG_PRICE_TASK_STARTTIME[1]),
                minute=str(settings.BUG_PRICE_TASK_STARTTIME[2])
            ),
            'args': ()
        },
        'baidu_statics_report': {
            'task': 'tasks.baidu_statics_report.export_baidu_statics',
            'schedule': crontab(hour='9', minute='0'),
            'args': ()
        },
    }

    register("tasks.inventories")
    register("tasks.alicdn")
    register("tasks.proxy")
    # register("tasks.crawlers.prices")
    register("tasks.supplier_statics")
    register("tasks.hotelmatching")
    register("tasks.package_prices")
    register("tasks.upload_image")
    register("tasks.check_prices")
    register("tasks.create_hotel")
    register("tasks.baidu_statics_report")
    app.conf.task_routes = {
        "tasks.alicdn.*": {"queue": "alicdn"},
        "tasks.inventories.*": {"queue": "scripture"},
        "tasks.supplier_statics.*": {"queue": "scripture"},
        "tasks.upload_image.*": {"queue": "scripture"},
        "tasks.check_prices.*": {"queue": "scripture"},
        "tasks.hotelmatching.*": {"queue": "scripture"},
        "tasks.proxy.*": {"queue": "scripture"},
        "tasks.package_prices.*": {"queue": "scripture"},
        "tasks.create_hotel.*": {"queue": "scripture"},
        "tasks.baidu_statics_report.export_baidu_statics": {"queue": "scripture"},
    }
