#!/usr/bin/env python

from .exception import ConstError


class _const(object):
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise ConstError("Can't rebind const (%s)" % name)
        if not name.isupper():
            raise ConstError("Const must be upper.")
        self.__dict__[name] = value


const = _const()

const.IS_PRODUCTION = 'is_production'
const.DEBUG = 'debug'
const.AUTO_RELOAD = 'auto_reload'

const.REDIS_EXPIRE_TIME = 'redis_expire_time' # 6 * 60

const.HUB_API_ENDPOINT = 'hub_api_endpoint'
const.HUB_JWT_APP = 'hub_jwt_app'
const.HUB_JWT_APP_SECRET = 'hub_jwt_app_secret'

const.DEFAULT_USER = 'default_user'
const.UA = 'User-Agent'