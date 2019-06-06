import logging

from yarl import URL
import redis

from scripture import settings
from tasks.utils.notifiers import DingtalkMessage, DingtalkNotifier
from tasks.errors import NotifyFailed

logger = logging.getLogger(__name__)
redis_url = URL(settings.REDIS_URL)
db = int(redis_url.path.split('/')[1])

class DingDingMiddleware:
    def process_response(self, request, response, spider):
        redis_conn = redis.Redis(host=redis_url.host, port=redis_url.port, db=db)
        _url = URL(response.url)
        _host = _url.host
        if _host == 'www.booking.com' and not _url.query:
            hid = _url.path[7:]
            redis_conn.sadd('crawled_booking', hid)
            crawl_booking = len(redis_conn.smembers('crawl_booking'))
            crawled_booking = len(redis_conn.smembers('crawled_booking'))
            if crawl_booking == crawled_booking:
                task_info = {'任务总计': crawled_booking}
                text = f'## [通知]bookings抓取任务已完成\n{task_info}'
                msg = DingtalkMessage(title='booking数据抓取', text=text)
                try:
                    DingtalkNotifier().send(msg, settings.DINGTALK_ACCESS_TOKEN )
                except NotifyFailed as exc:
                    logger.error('钉钉告警失败', exc_info=exc)
        elif _host == 'www.hotels.cn':
            hid = _url.path.strip("/").split("/")[0][2:]
            redis_conn.sadd('crawled_hcom', hid)
            crawl_hcom = len(redis_conn.smembers('crawl_hcom'))
            crawled_hcom = len(redis_conn.smembers('crawled_hcom'))
            if crawl_hcom == crawled_hcom:
                task_info = {'任务总计': crawled_hcom}
                text = f'## [通知]hotelsCN抓取任务已完成\n{task_info}'
                msg = DingtalkMessage(title='hotels数据抓取', text=text)
                try:
                    DingtalkNotifier().send(msg, settings.DINGTALK_ACCESS_TOKEN)
                except NotifyFailed as exc:
                    logger.error('钉钉告警失败', exc_info=exc)
        return response
