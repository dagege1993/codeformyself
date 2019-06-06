# coding: utf8

from .auto_proxy import AutoProxyMiddleware
from .user_agent import UserAgentMiddleware
from .jset_compatible import JsetCompatibleMiddleware
from .hotels_filter import HotelsFilterMiddleware
from .spider_middleware import ScriptureSpiderMiddleware
from .html_saver_middleware import HtmlSaverMiddleware
from .dingding import DingDingMiddleware
from .proxy import ProxyMiddleware
from .retry import LocalRetryMiddleware

__all__ = [
    'AutoProxyMiddleware', 'UserAgentMiddleware', 'ScriptureSpiderMiddleware',
    'JsetCompatibleMiddleware', 'HotelsFilterMiddleware', 'HtmlSaverMiddleware',
    'DingDingMiddleware', 'ProxyMiddleware', 'LocalRetryMiddleware'
]
