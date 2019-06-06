import re
import sys
import enum
import json
import time
import atexit
import random
import logging
import urllib3

import requests
import pychrome
import coloredlogs

from urllib.parse import unquote
from datetime import datetime, timedelta

from tasks.utils.database import databases


logger = logging.getLogger(__name__)
level_style = {
    'debug': {'color': 'blue'},
    'info': {'color': 'white'},
    'warning': {'color': 'yellow'},
    'error': {'color': 'red'},
    'critical': {'bold': True, 'color': 'red'}
}
coloredlogs.install(
    level='DEBUG', isatty=True, level_styles=level_style,
    fmt='%(asctime)s %(name)s %(levelname)s %(message)s'
)

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
        "Referer": "https://hotels.ctrip.com/international/",
        "Accept-Charset": "gb2312,gbk;q=0.7,utf-8;q=0.7,*;q=0.7",
    },  # 网上找的浏览器
    {
        "Proxy-Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0",
        "Accept": "image/gif,image/x-xbitmap,image/jpeg,application/x-shockwave-flash,application/vnd.ms-excel,application/vnd.ms-powerpoint,application/msword,*/*",
        "DNT": "1",
        "Referer": "https://hotels.ctrip.com/international/",
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
        "Referer": "https://hotels.ctrip.com/international/",
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
        "Referer": "https://hotels.ctrip.com/international/",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.7,en;q=0.6",
    },  # Win10 系统 firefox 浏览器
    {
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64;) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Referer": "https://hotels.ctrip.com/international/",
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
        "Referer": "https://hotels.ctrip.com/international/",
        "Accept-Charset": "gb2312,gbk;q=0.7,utf-8;q=0.7,*;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0",
    }
]


def _cookies():
    # tab.start()
    page = tab.call_method("Page.navigate",
                           url="https://hotels.ctrip.com/international/",
                           _timeout=5)
    cookies = tab.call_method('Network.getAllCookies', url='ctrip.com')
    # tab.stop()
    logger.debug('cookies: %s', cookies)
    return {
        cookie['name']: cookie['value']
        for cookie in cookies['cookies']
    }


def _proxy():
    proxies = DB.cm_proxies.find({
        'updated_at': {
            '$gte': datetime() - timedelta(minutes=13)
        }
    })
    proxy = random.choice(proxies)
    return 'http://{ip}:{port}'.format(ip=proxy['ip'], port=proxy['port'])


class MustExit(Exception):
    pass


class Providers(enum.Enum):
    bonotel = 'bonotel'
    roomsxml = 'roomsxml'
    hotelbeds = 'hotelbeds'
    hotelspro = 'hotelspro'
    jactravel = 'jactravel'


def supplier_table(supplier):
    return DB.get_collection(
        f'statics.hotels.{supplier.value}'
    )


def word_for_compare(word):
    word = word.lower().replace('hotel', '').replace('.', ' ')\
        .replace('&', ' ').replace(',', ' ').replace('-', ' ')
    return re.sub('\s{2,}', ' ', word)


def query_name_chs(name, cookies, retring=0, is_international=True):
    if is_international:
        url = 'https://hotels.ctrip.com/international/Tool/cityFilter.ashx'
        params = {
            'charset': 'gb2312',
            'flagship': 1,
            'keyword': name
        }
    else:
        url = 'https://hotels.ctrip.com/Domestic/Tool/AjaxDestination.aspx'
        params = {
            'keyword': name,
            'from': 'public'
        }
    headers = random.choice(HEADERS)
    try:
        resp = requests.get(url, headers=headers, params=params,
                            allow_redirects=False,
                            cookies=cookies)
    except urllib3.exceptions.ProtocolError:
        if retring < 2:
            time.sleep(.5)
            return query_name_chs(name, cookies, retring=retring + 1)
        raise
    if resp.status_code >= 500:
        if retring == 0:
            logger.critical('Failed to request, will retry.')
            time.sleep(.5)
            return query_name_chs(name, cookies, retring=1)
        logger.critical('Failed to request %s, after %s times.',
                        name,
                        retring + 1)
    if resp.status_code == 302:
        raise MustExit()
    text = resp.text
    all_name = []
    try:
        resp = json.loads(unquote(text[21: -1], encoding='utf-8'))
    except IndexError:
        logger.critical('Bad response %s', text)
        return
    except json.decoder.JSONDecodeError:
        logger.critical('Bad response %s', text)
        return
    items = resp.get('data', '').split('@')
    for item in items:
        if not item:
            continue
        try:
            if is_international:
                name_en, name_zh, _type, *_ = item.split('|')
            else:
                try:
                    item = item.split('，')[1]
                except IndexError:
                    logger.error('Incomplete item %s', item)
                    continue
                city, _type, name_chs, *_ = item.split('|')
        except ValueError:
            logger.error('Unknown item %s', item)
            continue
        # hotel = fields[1]
        if _type.lower() != 'hotel':
            logger.warning(f'Item is not a hotel: {_type}')
            continue
        if is_international:
            hotel_detail = name_zh.split('，')
            name_chs = hotel_detail[0]
        if not re.findall('[\u4E00-\u9FA5]+', name_chs):
            logger.warning(f'Name is not in Chinese: {name_chs}')
            continue
        all_name.append(name_chs)
        if is_international and len(all_name) == 1:
            matched_name = word_for_compare(name_en)
            _name = word_for_compare(name)
            if matched_name == _name:
                break
            if matched_name in _name:
                break
            if _name in matched_name:
                break
    if not all_name:
        logger.error(f'[Empty] {name}: {resp}')
    return ';'.join(all_name)


def save_process(process):
    with open('/tmp/process', 'w') as p:
        p.write(str(process - 100))
        logger.info('Process saved, %s', process)
    return True


def load_process():
    with open('/tmp/process', 'r') as p:
        process = int(p.read())
        logger.info('Loaded process, %s', process)
    return process


def main():
    start = time.time()
    count = 0
    fetched = 0
    successful = 0
    atexit.register(lambda: save_process(count))
    can_skiped = load_process()
    cookies = _cookies()
    for provider in Providers:
        table = supplier_table(provider)
        for doc in table.find({}, no_cursor_timeout=True):
            count += 1
            if count <= can_skiped:
                continue
            if 'ctrip_name' in doc:
                continue
            if count % 10000 == 0:
                cookies = _cookies()
            fetched += 1
            logger.debug('-' * 100)
            logger.info('hotel num: %s', count)
            logger.debug('hotel name: %s', doc['name'])
            name_chs = query_name_chs(doc['name'], cookies)
            if not name_chs:
                name_chs = query_name_chs(
                    doc['name'],
                    cookies,
                    is_international=False
                )
            if name_chs:
                logger.debug('ctrip name: %s', name_chs)
                successful += 1
                table.update_one(
                    {'_id': doc['_id']},
                    {
                        "$set": {'ctrip_name': name_chs}
                    }
                )
            logger.info('time: %s', f'{(time.time() - start)}s')
            logger.info('success rate: %s', successful / fetched)
    return True


if __name__ == '__main__':

    browser = pychrome.Browser()
    tab = list(
        filter(
            lambda tab: tab.id == '(D3876BF786C0B494B01CC04FFE420A2B)',
            browser.list_tab()
        )
    )[0]
    if tab.status != 'started':
        tab.start()
    while True:
        try:
            if main():
                atexit._clear()
                break
            atexit._run_exitfuncs()
            atexit._clear()
        except (MustExit, KeyboardInterrupt):
            sys.exit(255)
            break
        except Exception:
            logger.warning('Restarting!')
        time.sleep(10)
