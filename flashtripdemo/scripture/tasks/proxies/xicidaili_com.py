# coding: utf8

import requests
from lxml import etree

from . import Provider


def take_first(l, *, default=None):
    try:
        return l[0]
    except (IndexError, ValueError):
        return default


class XicidailiCom(Provider):

    dest = 'http://www.xicidaili.com/nn/'
    ua = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
          '(KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')

    def _fetch(self):
        resp = requests.get(self.dest, headers={'User-Agent': self.ua})
        assert resp.status_code == 200, resp.status_code

        parser = etree.HTMLParser()
        self.element = etree.fromstring(resp.text, parser)

    def parse(self):
        for elem in self.element.xpath('//table[@id="ip_list"]/tr')[1:]:
            tds = elem.xpath('.//td')
            yield {
                'country': take_first(
                    tds[0].xpath('.//img/@alt'), default='').upper(),
                'ip': tds[1].text,
                'port': tds[2].text,
                'loc': take_first(tds[3].xpath('.//a/text()')),
                'type': tds[4].text,
                'protocal': tds[5].text.lower(),
                'alived': tds[-2].text,
                'updated_at': tds[-1].text,
            }
