# coding: utf8

import os
from sanic import Blueprint
from sanic.response import html

template = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates')
privacy_bp = Blueprint('privacy', url_prefix='/views/privacy')


@privacy_bp.get('/')
def privacy(request):
    html_file = os.path.join(template, 'privacy.html')
    with open(html_file) as f:
        content = f.read()

    return html(content)
