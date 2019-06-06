# coding: utf8

from sanic import Blueprint

views_bp = Blueprint('views', url_prefix='/views')


from . import start_spiders  # noqa
from . import static_hotel_search # noqa
from . import download_online_hotel # noqa
from . import create_hotel_excel # noqa
from . import match_hotels # noqa
from . import download_user_record