# coding:utf-8
# Standard Library
import logging
from datetime import datetime

# Third Party
from tasks import settings
from tasks.application import app

from .bug_price import update_bug_price_type, get_next_day_of_week_timedelta

logger = logging.getLogger(__name__)
delay_time = settings.BUG_PRICE_TASK_TIMEDELTA*60

@app.task
def check_bug_price(cms_id, checkin, fir=False):
    update_bug_price_type(cms_id, checkin)
    if (
        get_next_day_of_week_timedelta(*settings.BUG_PRICE_TASK_STARTTIME)
        > delay_time * 2
    ):
        check_bug_price.apply_async(
            (cms_id, checkin), countdown=delay_time
        )  # 继续发布任务
        logger.info(f"{cms_id} : {checkin} bug_price check task continue")
        return f"{cms_id} : {checkin} bug_price check task continue"
    else:
        logger.info(f"{cms_id} : {checkin} bug_price check task complete")
        return f"{cms_id} : {checkin} bug_price check task complete"
    if fir:
        logger.info(
            f"find & publish bug_price check of {cms_id}: {checkin} at {datetime.now()}"
        )
    return f"{cms_id}: {checkin} publish succeed"
