#!/usr/bin/env python

import logging
from datetime import datetime
from decimal import Decimal

from tornado.web import RequestHandler, HTTPError
import json

from api.types.consts import const
from api import settings


class BaseHandler(RequestHandler):
    def __init__(self, *args, **kwargs):
        self.user_id = None
        self.username = None
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

        super(BaseHandler, self).__init__(*args, **kwargs)

    async def prepare(self):
        logger = self.logger.getChild('prepare')
            
        if self.request.body:
            if "Content-Type" not in self.request.headers:
                raise HTTPError(400, reason="Content-Type is required.")
            if not self.request.headers['Content-Type'].startswith('application/json'):
                raise HTTPError(400, reason="Invalid Content-Type")
            self.request.json = json.loads(self.request.body)

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.set_status(status_code)
            return self.finish('not found - 404')

        elif status_code == 400:
            self.set_status(status_code)
            return self.finish('bad request.')

        elif status_code == 402:
            self.set_status(status_code)
            return self.finish('csrf error.')

        elif status_code == 403:
            self.set_status(status_code)
            return self.finish('sorry, you have no permission. Please '
                               'contact the administrator.')

        elif status_code == 500:
            self.set_status(status_code)
            return self.finish('server error.')

        elif status_code == 401:
            self.set_status(status_code)
            return self.finish('please login.')

        else:
            self.set_status(status_code)
            return self.finish('unknown error.')
    
    @staticmethod
    def validate_required_field(name, body):
        if name not in body:
            raise HTTPError(400, f"{name} is required.")

    @staticmethod
    def validate_string_field(name, value):
        if not isinstance(value, str):
            raise HTTPError(400, f"{name} is invalid.")

    @staticmethod
    def validate_boolean_field(name, value):
        if not isinstance(value, bool):
            raise HTTPError(400, f"{name} is invalid.")

    @staticmethod
    def validate_enum_field(name, value, enum_type):
        if not isinstance(value, str):
            raise HTTPError(400, f"{name} is invalid.")
        if value not in enum_type.__members__.keys():
            raise HTTPError(400, f"{name} is invalid.")

    @staticmethod
    def validate_and_convert_numerical_field(name, value, allow_string=False, to_type=Decimal):
        if allow_string and isinstance(value, str):
            try:
                return to_type(value)
            except Exception as exc:
                raise HTTPError(400, f"{name} is invalid: {exc}.")
        if not isinstance(value, (int, float)):
            raise HTTPError(400, f"{name} is invalid: {type(value)}.")
        return to_type(str(value))

    @staticmethod
    def validate_and_convert_datetime_field(name, value, _format):
        if not isinstance(value, str):
            raise HTTPError(400, f"{name} is invalid.", reason=f"{name} is invalid.")
        try:
            return datetime.strptime(value, _format)
        except Exception as exc:
            raise HTTPError(400, str(exc), reason=f"{name} format is invalid.")

    @staticmethod
    def validate_dict_field(name, value):
        if not isinstance(value, dict):
            raise HTTPError(400, f'{name} is invalid, expecting mapping, actually {type(value)}.', reason=f'{name} is invalid')
        return value

    @staticmethod
    def validate_list_field(name, value):
        if not isinstance(value, list):
            raise HTTPError(400, f'{name} is invalid, expecting array, actually {type(value)}.', reason=f'{name} is invalid')
        return value
        
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Allow-Headers', 'X-Auth-Key, Content-Type')

    def options(self, *args, **kwargs):
        self.set_status(204)
        self.finish()


class HealthCheck(BaseHandler):
    def head(self, *args, **kwargs):
        self.write("I'm OK")
