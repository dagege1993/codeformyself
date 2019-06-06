# coding: utf8
import logging

from json2html import json2html
from sanic.response import html
from web.utils.database import databases

from . import views_bp

HTML = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<link href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" rel="stylesheet">
<link href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</head>
<body>
<div class="container-fluid" style="padding-top:50">
<h1 class="text-center">搜索hotelbeds</h1>
<hr/>
<form class="form-horizontal" method="post">
  <div class="form-group">
    <div class="col-sm-10">
    <label class="sr-only" for="HotelPartialName">hotel name</label>
    <input type="text" class="form-control" name="partial" value="{}" id="HotelPartialName" placeholder="hotel name">
    </div>
  <button type="submit" class="btn btn-default">搜索</button>
  </div>
</form>
<hr>
<div class="table-responsive">{}</div>
</div>
</body>
</html>'''

sandbox = None


@views_bp.get('/statics/hotels')
async def index(request):
    return html(HTML.format("", ""))


@views_bp.post('/statics/hotels')
async def search(request):
    logger = logging.getLogger(__name__)
    p = request.form.get('partial', '').lower()
    scripture = databases('scripture')
    cursor = scripture.statics.hotels.hotelbeds.find(
        {
            "$text": {
                "$search": f'"{p}"'
            }
        }
    )
    hotels = [formatted(hotel) async for hotel in cursor]
    style_classes = 'table table-bordered table-hover'
    table = json2html.convert(
        hotels,
        table_attributes=f'id="info-table" class="{style_classes}"'
    )
    logger.info(f'partial:{p} response sucess')
    return html(HTML.format(p, table))


def formatted(hotel):
    hotel['hotel_id'] = int(hotel['hotel_id'])
    hotel.pop('_id')
    hotel.pop('description')
    hotel['email'] = hotel['email'].lower()
    hotel['postal'] = hotel.pop('postal_code')
    hotel['country'] = hotel.pop('country_code')
    hotel['destination'] = hotel.pop('destination_code')
    hotel['zone'] = int(hotel.pop('zone_code'))
    return hotel
