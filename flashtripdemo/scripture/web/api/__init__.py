# coding: utf8

from sanic import Blueprint

api_v1 = Blueprint("api_v1", url_prefix="/api/v1")

from . import (
    tripadvisor,
    crawled_urls,
    create_hotel,
    price_calendar,
    hotel_sim,
    start_crawl,
    facility,
    record_user,
    relux,
    code_to_hotel,
    record_statitics,
    record_quotes,
    taspider,
)  # noqa
