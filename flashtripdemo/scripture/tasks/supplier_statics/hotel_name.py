import random
import requests
import json
import logging
import re

from urllib.parse import unquote

from tasks.utils.database import databases


logger = logging.getLogger(__name__)
DB = databases('scripture')
HEADERS = [
    {
        "Proxy-Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "DNT": "1",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
        "Referer": "https://www.baidu.com/s?wd=%BC%96%E7%A0%81&rsv_spt=1&rsv_iqid=0x9fcbc99a0000b5d7&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&rqlang=cn&tn=baiduhome_pg&rsv_enter=0&oq=If-None-Match&inputT=7282&rsv_t",
        "Accept-Charset": "gb2312,gbk;q=0.7,utf-8;q=0.7,*;q=0.7",
    },  # 网上找的浏览器
    {
        "Proxy-Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0",
        "Accept": "image/gif,image/x-xbitmap,image/jpeg,application/x-shockwave-flash,application/vnd.ms-excel,application/vnd.ms-powerpoint,application/msword,*/*",
        "DNT": "1",
        "Referer": "https://www.baidu.com/link?url=c-FMHf06-ZPhoRM4tWduhraKXhnSm_RzjXZ-ZTFnPAvZN",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
    },  # window 7 系统浏览器
    {
        "Proxy-Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
        "Accept": "image/x-xbitmap,image/jpeg,application/x-shockwave-flash,application/vnd.ms-excel,application/vnd.ms-powerpoint,application/msword,*/*",
        "DNT": "1",
        "Referer": "https://www.baidu.com/s?wd=http%B4%20Pragma&rsf=1&rsp=4&f=1&oq=Pragma&tn=baiduhome_pg&ie=utf-8&usm=3&rsv_idx=2&rsv_pq=e9bd5e5000010",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.7,en;q=0.6",
    },  # Linux 系统 firefox 浏览器
    {
        "Proxy-Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0",
        "Accept": "*/*",
        "DNT": "1",
        "Referer": "https://www.baidu.com/link?url=c-FMHf06-ZPhoRM4tWduhraKXhnSm_RzjXZ-ZTFnP",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.7,en;q=0.6",
    },  # Win10 系统 firefox 浏览器
    {
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64;) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Referer": "https://www.baidu.com/link?url=c-FMHf06-ZPhoRM4tWduhraKXhnSm_RzjXZ-",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.7,en;q=0.6",
        "Accept-Charset": "gb2312,gbk;q=0.7,utf-8;q=0.7,*;q=0.7",
    },  # Win10 系统 Chrome 浏览器
    {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "DNT": "1",
        "Referer": "https://www.baidu.com/s?wd=If-None-Match&rsv_spt=1&rsv_iqid=0x9fcbc99a0000b5d7&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&rq",
        "Accept-Charset": "gb2312,gbk;q=0.7,utf-8;q=0.7,*;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0",
    }
]


def word_for_compare(word: str) -> str:
    word = word.lower().replace('hotel', '').replace('.', ' ')\
        .replace('&', ' ').replace(',', ' ').replace('-', ' ')
    return re.sub('\s{2,}', ' ', word)


def fetch_ctrip_name(name: str) -> str:
    url = 'http://hotels.ctrip.com/international/Tool/cityFilter.ashx'
    params = {
        'charset': 'gb2312',
        'flagship': 1,
        'keyword': name
    }
    resp = unquote(requests.get(url, headers=random.choice(HEADERS), params=params).text,
                   encoding='utf-8', errors='replace')
    all_name = []
    try:
        resp = json.loads(resp[21: -1])
    except json.decoder.JSONDecodeError:
        logger.critical('Bad Request: %s', resp)
        return ''
    items = resp.get('data', '').split('@')
    for item in items:
        if not item:
            continue
        name_en, name_zh, _type, *_ = item.split('|')
        if _type != 'hotel':
            logger.warning(f'Item is not a hotel: {_type}')
            continue
        hotel_detail = name_zh.split('，')
        name_chs = hotel_detail[0]
        if not re.search('[\u4E00-\u9FA5]+', name_chs):
            logger.warning(f'Name is not in Chinese: {name_chs}')
            continue
        all_name.append(name_chs)
        # 以下代码判断如果第一条与搜索的name相符，立即结束循环
        if len(all_name) == 1:
            matched_name = word_for_compare(name_en)
            _name = word_for_compare(name)
            if matched_name == _name:
                break
            if matched_name in _name:
                break
            if _name in matched_name:
                break
    return ';'.join(all_name)

