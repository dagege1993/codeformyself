# coding: utf8

import requests
from lxml import etree

from . import Provider


class KuaiDaiLiComFree(Provider):

    dest = 'http://www.kuaidaili.com/free'

    def _fetch(self):
        inha = requests.get('{}/{}'.format(self.dest, 'inha'))
        intr = requests.get('{}/{}'.format(self.dest, 'intr'))

        parser = etree.HTMLParser()

        self.elements = {
            'inha': etree.fromstring(inha.text, parser),
            'intr': etree.fromstring(intr.text, parser)
        }

    def parse(self, with_intr=False):
        table = self.elements['inha'].xpath('//div[@id="list"]/table/tbody/tr')
        for elem in table:
            u = elem.xpath('./td[@data-title="最后验证时间"]/text()')[0]
            yield {
                'ip': elem.xpath('./td[@data-title="IP"]/text()')[0],
                'port': elem.xpath('./td[@data-title="PORT"]/text()')[0],
                'type': elem.xpath('./td[@data-title="匿名度"]/text()')[0],
                'protocal': elem.xpath('./td[@data-title="类型"]/text()')[0],
                'loc': elem.xpath('./td[@data-title="位置"]/text()')[0],
                'lantency': elem.xpath('./td[@data-title="响应速度"]/text()')[0],
                'updated_at': u
            }

    def update(self):
        pass


if __name__ == '__main__':
    print(list(KuaiDaiLiComFree().parse()))
