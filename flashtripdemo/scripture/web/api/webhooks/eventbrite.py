# coding: utf8

import logging
from sanic import Blueprint
from sanic.response import json

CLIENT_SECRET = '4PUQYJ6WYGC6EFZPJYNPEOBTA3CQYZTY3VLEWCSRI54VKPYLXI'
MINE_OAUTH_TOKEN = '2WJES6OJXB2OULJAURUB'
ANONYMOUS_OAUTH_TOKEN = 'AEW5WKFGSMJAAVGXLMT6'

event_cb = Blueprint(
    'eventbrite_callback',
    url_prefix='/webhooks/v1/eventbrite'
)

logger = logging.getLogger(__name__)


@event_cb.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def index(request):
    logger.info(request.args)
    logger.info(request.body)
    return json({'status': 200})
