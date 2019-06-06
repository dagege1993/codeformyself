#!/bin/env python3
# coding: utf8
"""Web server based Sanic
"""

import os
import logging.config

from sanic import Sanic
from sanic.response import json
from sanic_cors import CORS

from web import settings

logging.getLogger('sanic').propagate = False
logging.getLogger('network').propagate = False
DEBUG = os.environ.get('DEBUG', False) is not False
if DEBUG:
    logging.basicConfig(level='DEBUG')
logging.config.dictConfig(settings.WEB_LOGGER)
app = Sanic(__name__)  # pylint: disable=C0103
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

from web.api.webhooks.solr import solr_bp  # noqa
from web.api.webhooks.gmail import gmail_cb  # noqa pylint: disable=C0413, E0401
from web.api.webhooks.eventbrite import event_cb  # noqa pylint: disable=C0413, E0401
from web.api import api_v1  # noqa pylint: disable=C0413, E0401
from web.datas import publish_v1, select_v1
from web.views import views_bp  # noqa pylint: disable=C0413, E0401
from web.views.google import google_bp, google_auth_bp  # noqa pylint: disable=C0413, E0401
from web.views.privacy import privacy_bp  # noqa pylint: disable=C0413, E0401
from web.views.cdn_logs import cdnlogs_bp  # noqa pylint: disable=C0413,E0401
from web.views.package_prices import package_bp  # noqa
from web.http_proto import HttpProto  # noqa
from web.utils.database import pg_databases, redis_db

app.config.RESPONSE_TIMEOUT = 18000

app.blueprint(api_v1)
app.blueprint(publish_v1)
app.blueprint(select_v1)
app.blueprint(solr_bp)
app.blueprint(gmail_cb)
app.blueprint(event_cb)
app.blueprint(views_bp)
app.blueprint(google_bp)
app.blueprint(privacy_bp)
app.blueprint(cdnlogs_bp)
app.blueprint(package_bp)
app.blueprint(google_auth_bp)


@app.listener('before_server_start')
async def init(sanic, loop):
    pg = pg_databases('record')
    await pg.set_bind(settings.PGSQL["record"])
    await redis_db(settings.REDIS)
    

@app.head('/healthcheck')
def health_check(request):
    """Health check"""
    return json({'status': 200, 'message': 'alive'})


def index():
    """Main"""
    return app.run(
        host="0.0.0.0",
        port=4010,
        protocol=HttpProto,
        debug=DEBUG,
        workers=4,
        backlog=511
    )


if __name__ == '__main__':
    index()
