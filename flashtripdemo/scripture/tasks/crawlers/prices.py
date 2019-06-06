# coding: utf8
"""从其它地方抓取针对套餐内酒店的价格，并接入influxdb."""

import re
import time

from decimal import Decimal
from datetime import datetime, timedelta

import requests

from bson import ObjectId
from celery.utils.log import get_task_logger

from tasks import settings
from tasks.application import app
from tasks.utils.database import databases

PRE = re.compile(r'([0-9,]*\.?[0-9,]*)')

logger = get_task_logger('tasks')


@app.task
def booking_com():
    """从booking.cn抓取酒店价格."""
    packages = databases('hub').sku_packages.find()
    checkin = datetime.now() + timedelta(days=15)
    for pkg in packages:
        for htl in pkg['hotels']:
            oid = str(htl['hotel'])
            days = htl['days']
            for interval in range(10):
                checkin += timedelta(days=interval)
                checkout = checkin + timedelta(days=days)
                fetch_price_by_hotel.delay(
                    oid,
                    checkin.strftime('%Y-%m-%d'),
                    checkout.strftime('%Y-%m-%d'),
                    days
                )


@app.task
def fetch_price_by_hotel(oid, checkin, checkout, days):
    """Fetch price from booking.cn."""
    hotel = databases('hub').poi_items.find_one({'_id': ObjectId(oid)})

    booking_com_id = hotel.get('booking_com_id')
    if booking_com_id:
        logger.error('Can not be here.')
        return
    else:
        name = hotel.get('name')
        city_id = hotel.get('city')
        city_name = (databases('hub')
                     .meta_cities
                     .find_one({'_id': city_id})
                     .get('name'))

    resp = requests.get(
        settings.PARITY,
        params={
            'checkin': checkin,
            'checkout': checkout,
            'hotel': name,
            'city': city_name
        }
    )
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data['status'] == 200, data
    try:
        price = data['prices'][0]['price']
    except (IndexError, KeyError) as exc:
        logger.warning(f'Hotel({name}) not found. {data}', exc_info=exc)
        return
    if '元' in price:
        currency = 'CNY'
    elif '￥' in price:
        currency = 'CNY'
    elif '€' in price:
        currency = 'EUR'
    elif '$' in price:
        currency = 'USD'
    else:
        raise TypeError(price)

    price = Decimal(PRE.search(price).group(1).replace(',', ''))
    if currency != 'CNY':
        exchange_rate = get_exchange_rate(currency, 'CNY')
        price *= exchange_rate

    return push_to_influxdb(oid, hotel['name'], checkin, checkout, days, price)


def get_exchange_rate(src, dest):
    """Get exchange rate from mongodb."""
    rates = databases('hub').sys_rate.find_one()
    return rates['rate'][src]


def push_to_influxdb(hotel_id, hotel_name, checkin, checkout,
                     nights, value):
    """Push to influxdb."""
    host = settings.INFLUXDB
    tags = {
        'checkin': checkin,
        'checkout': checkout,
        'duration': nights,
        'hotel_id': hotel_id,
        'hotel_name': hotel_name,
        'room_type': 'booking_cn',
        'meal_type': 'unknown',
        'provider': 'booking_cn',
    }
    fields = {'value': value}

    tagstring = ','.join('{}={}'.format(k, v) for k, v in tags.items())
    fieldstring = ','.join('{}={}'.format(k, v) for k, v in fields.items())

    name = 'reservation_price_histories'
    timestamp = str(int(time.time() * 1000 * 1000 * 1000))

    d = f"{name},{' '.join((tagstring, fieldstring, timestamp))}"

    params = {'db': 'quotes'}

    resp = requests.post(host, params=params, data=d.encode('utf8'))
    assert resp.status_code == 200, resp.text
    return True
