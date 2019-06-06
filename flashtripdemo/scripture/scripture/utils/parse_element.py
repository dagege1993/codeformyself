# -*- coding: utf-8 -*-
import json
import re
import logging
from w3lib.html import remove_tags

from yarl import URL
from scripture.xpath import bookings_v2 as bk
from scripture.xpath import hotels as hotels_xp
from scripture.utils.processors import dupefilter
from scripture.utils.html import take_first, take_all

logger = logging.getLogger(__name__)


def _pictures(selectors):
    _pics = []
    for select in selectors:
        url = take_first(select, './@data-desktop')
        if not url:
            url = take_first(select, './@data-src')
        sizes = take_first(select, './@data-sizes')
        sizes = sizes and list(sizes) or list('zwybndeglst')
        name = take_first(select, './p/span[@class="room-name"]/text()')
        tag = take_first(select, './p/span[@class="second-level"]/text()')
        if not name:
            name = take_first(select, './p/text()')

        u = URL(url)
        if u.host != 'exp.cdn-hotels.com':
            *_, uri = u.path.split('/', 6)
            url = str(
                URL.build(
                    scheme='https',
                    host='exp.cdn-hotels.com',
                    path=uri
                )
            )
        else:
            url = url.format(size=sizes[0])
        _pics.append({
            'url': url,
            'name': name,
            'classification': tag,
            'sizes': sizes
        })

    return _pics


def _address(resp):
    address_info = resp.xpath(hotels_xp.ADDRESS_INFO).extract_first()
    address_info = json.loads(address_info)["address"]
    return {
        'street': address_info.get("streetAddress"),
        'locality': address_info.get("addressLocality"),
        'region': address_info.get("addressRegion"),
        'postal_code': address_info.get("postalCode"),
        'country': address_info.get("addressCountry")
    }


def _notice(resp, prefix):
    keys = {
        'CN': {
            'term': '政策',
            'alias': '其它名称',
            'mandatory': '强制消费',
            'optional': '其它费用'
        },
        'EN': {
            'term': 'term',
            'alias': 'alias',
            'mandatory': 'mandatory fees',
            'optional': 'optional fees'
        }
    }
    key = keys[prefix]
    term_xp = getattr(hotels_xp, prefix + '_TERM')
    alias_xp = getattr(hotels_xp, prefix + '_ALIAS')
    mandatory_xp = getattr(hotels_xp, prefix + '_MANDATORY_FEES')
    optional_xp = getattr(hotels_xp, prefix + '_OPTIONAL_FEES')
    mandatory = dupefilter(_clean(take_all(resp, mandatory_xp)))
    optional = dupefilter(_clean(take_all(resp, optional_xp)))
    return {
        key['term']: dupefilter(_clean(take_all(resp, term_xp))),
        key['alias']: dupefilter(_clean(take_all(resp, alias_xp))),
        key['mandatory']: mandatory,
        key['optional']: optional
    }


def _clean(_list):
    if not _list:
        return None
    return list(map(lambda v: remove_tags(v), _list))


def _summary(resp):
    xp = (hotels_xp)
    return {
        'key_facts': _clean(take_all(resp, xp.SUMMARY_KEY_FACTS)),
        'travellings': _clean(take_all(resp, xp.SUMMARY_TRAVELLING)),
        'transport': _clean(take_all(resp, xp.SUMMARY_TRANSPORT))
    }


def remove_line_break(s):
    if isinstance(s, list):
        s = "\n".join(s)
    return re.sub("\s{2,}", "\n", s).strip()


def find_polices(res):
    policy_base_node = res.xpath(bk.POLICES)
    if not policy_base_node:
        return []
    else:
        policy_base_node = policy_base_node[0]
    polices = []
    checkin_out_policy = ""
    for e in policy_base_node.xpath('./div'):
        ori_policy = (
            remove_line_break(e.xpath("string(.)").extract())
                .replace("预订取消/\n预付政策", "预订取消/预付政策")
                .replace("&amp;", "&")
        )
        if not ori_policy:
            continue
        ori_policy = ori_policy.split("\n")
        if ori_policy[0] == "入住时间":
            checkin_out_policy += f"入住时间: {ori_policy[1]}\n"
            continue
        if ori_policy[0] == "退房时间":
            checkin_out_policy += f"退房时间: {ori_policy[1]}\n"
            continue
        _policy = {
            "type": ori_policy[0],
            "content": "\n".join(set(ori_policy[1:])),
        }
        if _policy["content"].strip() == "":
            continue
        polices.append(_policy)
    polices.append({"type": "入住政策", "content": checkin_out_policy.strip()})
    if res.xpath('//*[@id="hp_important_info_box"]/div[1]/div/text()'):
        polices.append(
            {
                "type": "预定须知",
                "content": remove_line_break(
                    res.xpath(
                        bk.CONTENT
                    ).extract()
                ),
            }
        )
    remove_policy = []
    for i, policy in enumerate(polices):
        if "直至另行通知" in policy["content"]:
            remove_policy.append(i)
            continue
        if "接受上述银行卡" in policy["content"]:
            cards = "、".join(
                res.xpath(bk.CARDS).extract()
            )
            policy["content"] = f"{cards}\n{policy['content']}"

    return polices


def find_price(url, price):
    try:
        return int(float(re.search(r'\d*,?\d+\.?\d{0,2}元', price).group().replace(',', '').replace('元', '')))
    except Exception:
        return False


def get_policies(policies):
    policies = [v.strip() for v in policies if v.strip()]
    return '-'.join(policies).replace('\n', '').replace('\r', '')
