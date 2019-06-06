# coding: utf8

import re
import requests

from . import Provider


class Api66IpCn(Provider):

    dest = 'http://www.66ip.cn/nmtq.php'
    params = {
        'getnum': 500,   # 每页数量
        'isp': 0,   # 运营商， 不限
        'anonymoustype': 0,  # 匿名性， 不限
        'area': 1,  # 区域，中国
        'proxytype': 1,  # 代理类型, https
        'api': '66ip'
    }

    _RE = re.compile(r'(?P<ip>[\d\.]+):(?P<port>\d+)<br')

    def _fetch(self):
        resp = requests.get(self.dest, self.params)
        assert resp.status_code == 200

        self._text = resp.text

    def parse(self):

        for line in self._text.splitlines():
            s = self._RE.search(line.strip())
            if not s:
                continue
            d = s.groupdict()
            d['protocal'] = 'https'
            yield d


    def update(self):
        return self.parse()
