import oss2
import requests
import random

from celery.utils.log import get_task_logger
from tasks.application import app
from scripture.settings import USER_AGENT_LIST
from tasks import settings

logger = get_task_logger('tasks')
endpoint = settings.OSS_ENDPOINT
auth = oss2.Auth(settings.OSS_ACCESS_KEY_ID, settings.OSS_SECRET_ACCESS_KEY)
bucket = oss2.Bucket(auth, endpoint, settings.OSS_BUCKET)

@app.task(autoretry_for=(Exception, ), retry_kwargs={'max_retries': 2})
def _upload_image(url, path):
    user_agent = random.choice(USER_AGENT_LIST)
    resp = requests.get(
        str(url),
        headers={'User-Agent': user_agent}
    )
    logger.info('Image(%s), StatusCode(%d)', url, resp.status_code)
    if resp.status_code != 200:
        logger.error(f'download image fail ,Image({url}), StatusCode({resp.status_code})')
        return False
    put_result = bucket.put_object(path, resp.content)
    logger.info(f'Fetched object {path} source {url} status {put_result.status}')
    if put_result.status != 200:
        logger.error(f'upload image fail ,Image({path}), StatusCode({put_result.status})')
        return False
    return True
