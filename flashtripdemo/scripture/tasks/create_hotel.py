import json
import requests

from tasks import settings
from celery.utils.log import get_task_logger
from tasks.application import app

logger = get_task_logger('tasks')


@app.task
def dispatcher(data, ta_url):
    if ta_url:
        _url = f'{settings.GET_COMMENTS}?url={ta_url}'
        req = requests.get(_url)
        if req.status_code == 200:
            comments = json.loads(req.content.decode()).get('comments')
            data['comments'] = comments
            data['comments_url'] = ta_url
    req = requests.post(settings.UPLOAD_HOTEL, json=data)
    if req.status_code != 200:
        logger.warning(f'data:{data} create hotel fail')
    else:
        logger.info(f'data:{data} create hotel success')
