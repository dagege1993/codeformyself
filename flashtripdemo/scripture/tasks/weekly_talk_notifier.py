# coding: utf8

from datetime import datetime, timedelta

import requests
from celery.utils.log import get_task_logger

from .application import app
from . import settings

logger = get_task_logger('tasks')

md_content = """
![img](http://img3.weegotr.com/cms/uploads/201311171008518292.jpg)
### 又到周五啦，开不开森?
想好周末去哪儿嗨了没？别忘了下班之前写周报哦！
""".strip()


@app.task
def weekly_talk_notifier():
    """在dingtalk上发送周报提醒."""
    wikihost = 'http://wiki.feifanweige.com'
    uri = '/rest/api/content'

    auth = requests.auth.HTTPBasicAuth('auto0', 'auto0')

    dt = datetime.now()
    title = '{} - {}'.format(
        (dt - timedelta(days=4)).strftime('%Y/%m/%d'),
        dt.strftime('%Y/%m/%d')
    )
    payload = {
        "type": "page",
        "title": title,
        "ancestors": [{"id": 7536650}],
        "space": {"key": "WEB"},
        "body": {
            "storage": {
                "representation": "storage"
            }
        }
    }
    resp = requests.post('{}{}'.format(wikihost, uri), json=payload, auth=auth)
    url = '{}{}'.format(wikihost, resp.json()['_links']['tinyui'])

    webhook = 'https://oapi.dingtalk.com/robot/send'

    payload = {
        "actionCard": {
            "title": "又到周五啦，开不开森?",
            "text": md_content,
            "hideAvatar": "1",
            "btnOrientation": "0",
            "singleTitle": "去写周报",
            "singleURL": url
        },
        "msgtype": "actionCard"
    }
    resp = requests.post(
        webhook,
        json=payload,
        params={'access_token': settings.DINGTALK_NOTIFY['']}
    )
    if resp.status_code != 200:
        logger.error(
            'Failed to send dingtalk message to notify weekly talk. %s',
            resp.text
        )
        return False
    return True
