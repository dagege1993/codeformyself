import requests

cookies = {
    '$TASSK': 'enc%3AAGxvq%2B3SkNLP9qDJsW3JzwUA6JTfOT72fsvFOJgZwl1jnAo911ESSDKuJRzPojKMzXcKvHVJMVrA6uIT9qZYBhc7WF5CFHEWKnMJyT1SYs9QZRPeIm8vfSq7xNTg4%2FDk5w%3D%3D',
    'BEPIN': '%1%16ab626cdad%3Bbak09c.daodao.com%3A10023%3B',
    'ServerPool': 'A',
    'TART': '%1%enc%3AQZpLz%2BcEhM4gGeGC1etDTDZSqNLePS172aOfQJeyPlDhqPh9pPBewE8FmqnCHGOgXOsDGAaIMEA%3D',
    'TAUnique': '%1%enc%3AmnrKVKxoZ%2FUNSJTzw8g7nz%2BY75sxo05EeXhMV6c%2F3S5irck%2BOLs3gg%3D%3D',
    'roybatty': 'TNI1625\\u21ADMqaY65nwCnxnz%2FP8fPylJthl0IcqgPtOj6FZeZT%2BH%2FCMLNEt27vP%2B%2FXIvJtJMnsR3jCvZhkylQVroW0%2BNkG0nEy1BBrpUbm8mBYYuvS6qFfsTRSLhTltkR4mBMCGErnp%2FEzfE41WM1CtgFsom5PeD4cfy%2BQ2i9EuScea%2FRUeyF%2C1',
    '_gcl_au': '1.1.329702117.1557834159',
    '_ga': 'GA1.2.270059779.1557834160',
    '_gid': 'GA1.2.584281208.1557834160',
    '_gat_UA-79743238-4': '1',
    'SRT': '%1%enc%3AQZpLz%2BcEhM4gGeGC1etDTDZSqNLePS172aOfQJeyPlDhqPh9pPBewE8FmqnCHGOgXOsDGAaIMEA%3D',
    '__gads': 'ID=af9bffc08d87f3e8:T=1557834161:S=ALNI_MbUTHx9yyMniRWZ3N-hGZHgv6f6OA',
    'TATravelInfo': 'V2*AY.2019*AM.5*AD.20*DY.2019*DM.5*DD.25*A.2*MG.-1*HP.2*FL.3*DSM.1557834164911*AZ.1*RS.1',
    'CM': '%1%mds%2C1557834164813%2C1557920564%7C',
    'TASession': '%1%V2ID.9709BEE3DFADC55EF9211AD97215D112*SQ.14*LP.%2FHotels-g186338-oa30-London_England-Hotels%5C.html*LS.DemandLoadAjax*GR.24*TCPAR.36*TBR.81*EXEX.36*ABTR.75*PHTB.82*FS.37*CPU.96*HS.popularity*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*FA.1*DF.0*TRA.true*LD.186338',
    'TAUD': 'LA-1557834160319-1*HDD-1-2019_05_26.2019_05_27*RDD-1-2019_05_14*HD-4502-2019_05_20.2019_05_25.186338*G-4503-2.1.186338.*LD-28573-2019.5.20.2019.5.25*LG-28576-2.1.T.*ARDD-28577-2019_05_202019_05_25',
    'TAReturnTo': '%1%%2FHotels%3Fdf%3D%26zfn%3D%26reqNum%3D1%26ns%3D%26isLastPoll%3Dfalse%26zft%3D%26g%3D186338%26bs%3D%26puid%3DXNqprMCoATIAA9PU1NEAAAAd%26distFrom%3D%26sl_opp_json%3D%7B%7D%26blender_tag%3D%26paramSeqId%3D9%26distFromPnt%3D%26offset%3D0%26cat_tag%3D9189%26changeSet%3DFILTERS%2CMAIN_META%26zfc%3D9572%26zfb%3D%26amen%3D%26trating%3D4%2C5%26zfd%3D%26plSeed%3D1840104352%26zff%3D%26pRange%3D595%2C-1%2CRMB%2CALL_IN_WITH_EXCLUSIONS%26waitTime%3D20',
}

headers = {
    'X-Puid': 'XNqprMCoATIAA9PU1NEAAAAd',
    'Origin': 'https://www.tripadvisor.cn',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': 'text/html, */*',
    'Referer': 'https://www.tripadvisor.cn/Hotels-g186338-London_England-Hotels.html',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}

data = {
  'sl_opp_json': '{}',
  'plSeed': '1840104352',
  'offset': '0',
  'zff': '',
  'trating': '4,5',
  'bs': '',
  'blender_tag': '',
  'zfn': '',
  'df': '',
  'zfc': '9566,9572',
  'zfd': '',
  'distFrom': '',
  'cat_tag': '9189',
  'zfb': '',
  'ns': '',
  'distFromPnt': '',
  'zft': '',
  'amen': '',
  'pRange': '595,-1,RMB,ALL_IN_WITH_EXCLUSIONS',
  'reqNum': '1',
  'isLastPoll': 'false',
  'paramSeqId': '10',
  'waitTime': '35',
  'changeSet': 'FILTERS,MAIN_META',
  'puid': 'XNqprMCoATIAA9PU1NEAAAAd'
}

response = requests.post('https://www.tripadvisor.cn/Hotels-g186338-London_England-Hotels.html', headers=headers, cookies=cookies, data=data)
print(response.text)