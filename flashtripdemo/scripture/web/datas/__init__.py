# coding: utf8

from sanic import Blueprint

publish_v1 = Blueprint('publish_data_v1', url_prefix='/api/v1/data/publish')
select_v1 = Blueprint('select_data_v1', url_prefix='/api/v1/data/select')

from . import publish, select