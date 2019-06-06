# coding: utf8

import requests

from stem import Signal
from stem.control import Controller


def refresh_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
    with requests.Session() as request:
        with request.get('http://ipecho.net/plain') as resp:
            ip = resp.text
    return ip
