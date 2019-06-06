# coding: utf8

"""
Create by songww

Website: https://www.ip-address.com/proxy-list
"""

import requests
from lxml import etree

from . import Provider


class IpAddressComProxyList(Provider):

    dest = 'https://www.ip-adress.com/proxy-list'

    def _fetch(self):
        resp = requests.get(self.dest)
        parser = etree.HTMLParser()
        self.element = etree.fromstring(resp.text, parser)

    def parse(self):
        for elem in self.element.xpath('//table/tbody/tr'):
            tds = elem.xpath('./td/text()')
            yield {
                'ip': elem.xpath('./td/a/text()')[0],
                'port': tds[0][1:],
                'type': tds[1],
                'loc': tds[2],
                'updated_at': elem.xpath('./td/time/@datetime')[0]
            }

    def update(self):
        if not self.db:
            return self.parse()
        self.db.update()


if __name__ == '__main__':
    print(list(IpAddressComProxyList().update()))
