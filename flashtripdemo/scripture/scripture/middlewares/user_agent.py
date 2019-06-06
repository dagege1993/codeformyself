# coding: utf8

from random import choice
from scrapy.exceptions import NotConfigured
from yarl import URL


class UserAgentMiddleware(object):

    def __init__(self, user_agents=[]):
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawler):
        user_agents = crawler.settings.get('USER_AGENT_LIST', [])
        if not user_agents:
            raise NotConfigured("USER_AGENT_LIST not set or empty")

        return cls(user_agents)

    def process_request(self, request, spider):
        # 添加UA会导致hotelsCN抓取失败
        _url = URL(request.url)
        if _url.host == 'www.hotels.cn':
            return
        elif _url.host == 'm.ctrip.com':
            hid = _url.path.split('/')[-1].replace('.html', '')
            request.headers['User-Agent'] = 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
            request.headers['Referer'] = f"http://m.ctrip.com/webapp/hotel/oversea/hoteldetail/{hid}.html"
        else:
            request.headers['User-Agent'] = choice(self.user_agents)
