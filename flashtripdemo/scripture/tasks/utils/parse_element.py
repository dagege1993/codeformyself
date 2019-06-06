import re
from lxml import etree

from celery.utils.log import get_task_logger
from tasks.utils.notifiers import DingtalkMessage, DingtalkNotifier
from tasks.errors import NotifyFailed
from tasks import settings

logger = get_task_logger('tasks')


def find_price(url, price):
    try:
        return int(float(re.search('\d*,?\d+\.?\d{0,2}元', price).group().replace(',', '').replace('元', '')))
    except Exception as exc:
        logger.warning(f'{url}的{price}网页解析规则变更', exc_info=exc)


def get_policies(policies):
    policies = [v.strip() for v in policies if v.strip()]
    return '-'.join(policies).replace('\n', '').replace('\r', '')


def safe_xpath(tree, xp, name):
    try:
        fnd = tree.xpath("." + xp)
        return fnd[0].strip()
    except IndexError:
        print('????',tree)
        html = etree.tostring(tree, encoding="unicode")
        logger.error("Not found %s in %s.", name, html)


def dingding(title, text):
    msg = DingtalkMessage(title=title, text=text)
    try:
        DingtalkNotifier().send(msg, settings.DINGTALK_NOTIFY[''])
    except NotifyFailed as exc:
        logger.error('钉钉告警失败', exc_info=exc)
