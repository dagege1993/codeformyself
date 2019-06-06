# coding : utf8
"""
Create by songww
"""

import logging

from aioredis import create_redis
from sanic import Blueprint
from sanic.request import Request
from sanic.response import stream

from web import settings

logger = logging.getLogger(__name__)   # pylint: disable=C0103
cdnlogs_bp = Blueprint('cdnlogs', url_prefix='/views/cdn/logs')   # noqa pylint: disable=C0103


@cdnlogs_bp.get('/<date>')
async def viewlogs(unused_request: Request, date: str):
    """List all logs of cdn
    """
    R = await create_redis(settings.REDIS)   # pylint: disable=C0103
    keys = await R.keys(f'{date}_*')

    async def streaming(response):
        """Make streaming response
        """
        await response.write(f'<h1>{date} 4xx logs</h1>')
        for key in keys:
            await response.write(
                f'<h3>{key.decode("utf8").split("_", 1)[1]}</h3>')
            logs = await R.lrange(key, 0, (await R.llen(key)))
            for log in logs:
                await response.write(f'<li>{log.decode("utf8")}</li>')
    logger.info(f'get cdnlogs success')
    return stream(streaming, content_type="text/html; charset=utf8")
