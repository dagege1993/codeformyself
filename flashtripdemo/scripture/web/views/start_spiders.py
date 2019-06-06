# conding: utf8

import os
from sanic.response import html

from . import views_bp
from .privacy import template


@views_bp.get('/crawl/start')
async def _crawl_start(request):
    _file = os.path.join(template, 'crawl.html')
    with open(_file) as f:
        content = f.read()
    return html(content)
