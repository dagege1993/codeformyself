# coding: utf8

from w3lib.html import remove_tags
from html.parser import HTMLParser


class HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = HTMLStripper()

    if isinstance(html, (list, tuple)):
        return list(map(strip_tags, html))
    if isinstance(html, (str, bytes)):
        s.feed(html)
        return s.get_data()


def take_first(selector, xp: str):
    """choice first element
    """
    return selector.xpath(xp).extract_first()


def take_all(selector, xp: str):
    """return all elements
    """
    return selector.xpath(xp).extract()


def service_to_dict(selector, hotels_xp):
    """transform services to dict
    """
    services = []
    for select in selector:
        values = map(
            remove_tags,
            select.xpath('.' + hotels_xp.SERVICE_FACT_CELL).extract()
        )
        key = select.xpath('.' + hotels_xp.SERVICE_FACT_TITLE).extract_first()
        services.append({key: list(values)})

    return services
