import json
import pandas as pd

import requests


def xueqiu_first():
    url = "https://xueqiu.com/service/v5/stock/screener/quote/list"
    querystring = {"page": "1", "size": "90", "order": "desc", "orderby": "percent", "order_by": "percent",
                   "market": "US",
                   "type": "us", "_": "1555049852046"}
    payload = ""
    headers = {
        'Host': "xueqiu.com",
        'Connection': "keep-alive",
        'Accept': "*/*",
        'cache-control': "no-cache,no-cache",
        'X-Requested-With': "XMLHttpRequest",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
        'Referer': "https://xueqiu.com/hq",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
        'Cookie': "aliyungf_tc=AQAAABU2vw/KoAcA9N2VPRzo4ZUjI7dl; s=el197y2zfv; xq_a_token=3450822dc3b6c0b631c3ba4768fcddac23c054d7; xq_r_token=0de8d3b6155ce156310ff6d4e214d4532198ccec; __utma=1.797518204.1555049795.1555049795.1555049795.1; __utmc=1; __utmz=1.1555049795.1.1.utmcsr=github.com|utmccn=(referral)|utmcmd=referral|utmcct=/tdzhang/pre_interview/blob/master/questions/%E7%88%AC%E8%99%AB%EF%BC%88%E9%AB%98%E7%BA%A7%EF%BC%89.md; __utmt=1; u=391555049794641; device_id=060abf70c354a932b89e6ec87781ee54; __utmb=1.2.10.1555049795; Hm_lvt_1db88642e346389874251b5a1eded6e3=1555049794,1555049852; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1555049852",
        'Postman-Token': "b57eaa82-96aa-43c1-870f-3338d85594bb"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    return response.text


def stotage(response_text):
    response_text = json.loads(response_text)
    data_list = response_text.get("data").get("list")
    stock_list = []
    for data in data_list:
        symbol = data.get("symbol")  # 股票代码
        name = data.get("name")  # 股票名字
        current = data.get("current")  # 当前价格
        percent = data.get("percent")  # 涨跌幅
        market_capital = data.get("market_capital")  # 市值
        pe_ttm = data.get("pe_ttm")  # 市盈率
        stock_tuple = [symbol, name, current, percent, market_capital, pe_ttm]
        stock_list.append(stock_tuple)

    # 转为CSV文件
    name = ["股票代码", "股票名称", "当前价", "涨跌幅", "市值", "市盈率"]
    test = pd.DataFrame(columns=name, data=stock_list)
    test.to_csv('stock.csv', encoding='gbk', index=False)


if __name__ == '__main__':
    # 通过接口获取数据
    response_text = xueqiu_first()
    # 清洗并储存数据
    stotage(response_text)
