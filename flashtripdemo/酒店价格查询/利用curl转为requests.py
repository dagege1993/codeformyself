import requests

cookies = {
    # '$CommercePopunder': 'SuppressAll*1557803321223',
    # 'TASSK': 'enc%3AAJ2vx2yuK89hh0vB4ZRH5xZ58rsk%2F6xiA6O6haONvloaNKe%2BAPvNrjesyprLFvWIHUOn%2B1RZpUr0KFhFX5T534z0GMR2IrrYcMISChZxXhq3hG%2FPkxtVddcDGbolQFI%2BUw%3D%3D',
    # 'BEPIN': '%1%16ab45049ff%3Bweb08c.daodao.com%3A10023%3B',
    # 'ServerPool': 'C',
    # 'TART': '%1%enc%3AQZpLz%2BcEhM6H%2Bw2oezto5iymIzCMNuPP%2BGqsfk0hkcqQe3bS7YQnAe2mZw%2FOK0EWAJJVOu6GcoE%3D',
    # 'TAUnique': '%1%enc%3AvkH%2FTMQPxHUNSJTzw8g7nz%2BY75sxo05EY2mpsyNZzXh9i1%2B2aew%2BBQ%3D%3D',
    # '_gcl_au': '1.1.723677213.1557808777',
    # '_ga': 'GA1.2.53421744.1557808777',
    # '_gid': 'GA1.2.1654778507.1557808777',
    # 'CM': '%1%PremiumMobSess%2C%2C-1%7Ct4b-pc%2C%2C-1%7CRestAds%2FRPers%2C%2C-1%7CRCPers%2C%2C-1%7CWShadeSeen%2C%2C-1%7CTheForkMCCPers%2C%2C-1%7CHomeASess%2C1%2C-1%7CPremiumSURPers%2C%2C-1%7CPremiumMCSess%2C%2C-1%7CRestPartSess%2C%2C-1%7CRestPremRSess%2C%2C-1%7CCCSess%2C%2C-1%7CCYLSess%2C%2C-1%7CPremRetPers%2C%2C-1%7CViatorMCPers%2C%2C-1%7Csesssticker%2C%2C-1%7CPremiumORSess%2C%2C-1%7Ct4b-sc%2C%2C-1%7CRestAdsPers%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS2%2C%2C-1%7Cb2bmcpers%2C%2C-1%7CPremMCBtmSess%2C%2C-1%7CPremiumSURSess%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS%2C%2C-1%7CLaFourchette+Banners%2C%2C-1%7Csess_rev%2C%2C-1%7Csessamex%2C%2C-1%7CPremiumRRSess%2C%2C-1%7CTADORSess%2C%2C-1%7CAdsRetPers%2C%2C-1%7CTARSWBPers%2C%2C-1%7CSPMCSess%2C%2C-1%7CTheForkORSess%2C%2C-1%7CTheForkRRSess%2C%2C-1%7Cpers_rev%2C%2C-1%7CSPMCWBPers%2C%2C-1%7CRBAPers%2C%2C-1%7CRestAds%2FRSess%2C%2C-1%7CHomeAPers%2C%2C-1%7CPremiumMobPers%2C%2C-1%7CRCSess%2C%2C-1%7CLaFourchette+MC+Banners%2C%2C-1%7CRestAdsCCSess%2C%2C-1%7CRestPartPers%2C%2C-1%7CRestPremRPers%2C%2C-1%7Csh%2C%2C-1%7Cpssamex%2C%2C-1%7CTheForkMCCSess%2C%2C-1%7CCYLPers%2C%2C-1%7CCCPers%2C%2C-1%7Cb2bmcsess%2C%2C-1%7CSPMCPers%2C%2C-1%7CPremRetSess%2C%2C-1%7CViatorMCSess%2C%2C-1%7CPremiumMCPers%2C%2C-1%7CAdsRetSess%2C%2C-1%7CPremiumRRPers%2C%2C-1%7CRestAdsCCPers%2C%2C-1%7CTADORPers%2C%2C-1%7CTheForkORPers%2C%2C-1%7CPremMCBtmPers%2C%2C-1%7CTheForkRRPers%2C%2C-1%7CTARSWBSess%2C%2C-1%7CPremiumORPers%2C%2C-1%7CRestAdsSess%2C%2C-1%7CRBASess%2C%2C-1%7CSPORPers%2C%2C-1%7Cperssticker%2C%2C-1%7CSPMCWBSess%2C%2C-1%7C',
    # '_smt_uid': '5cda8416.7159805',
    # 'TATravelInfo': 'V2*AY.2019*AM.5*AD.26*DY.2019*DM.5*DD.27*A.2*MG.-1*HP.2*FL.3*DSM.1557825023207*RS.1',
    # 'roybatty': 'TNI1625\\u21ACm0xM26kjXVDYXDn8X1q7%2BdaUKO2pdoCLb1I%2BlqHhv1Xn1Z6HFV9p8sb4U31M1D3hD6aChDgDyiT7KuMrh5F70Nu7XLroSwJy%2BDmSLX09XQeosfi9MGfSQXS%2BQBfXe3noPa68gE30WJEXFTpZbaFVnaoKE7Oqu7nIwZu0iv7ewi%2C1',
    # 'SRT': '%1%enc%3AQZpLz%2BcEhM6H%2Bw2oezto5iymIzCMNuPP%2BGqsfk0hkcqQe3bS7YQnAe2mZw%2FOK0EWAJJVOu6GcoE%3D',
    # 'TASession': '%1%V2ID.555561FC987761FB9AC4FAD4E6742F75*SQ.98*LR.https%3A%2F%2Fwww%5C.tripadvisor%5C.cn%2FHotels-g186338-London_England-Hotels%5C.html*LP.%2FHotels%3Fg%3D186338%26reqNum%3D1%26puid%3DXNolXcCoASwAAmjvUsAAAABE%26isLastPoll%3Dfalse%26plSeed%3D1967882847%26sl_opp_json%3D%7B%7D%26waitTime%3D56%26paramSeqId%3D0%26changeSet%3DMAIN_META*LS.DemandLoadAjax*GR.78*TCPAR.58*TBR.37*EXEX.12*ABTR.46*PHTB.75*FS.24*CPU.29*HS.popularity*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*FA.1*DF.0*TRA.true*LD.298484',
    # 'TAUD': 'LA-1557803322751-1*RDD-1-2019_05_14*HC-21696419*HDD-21700420-2019_05_26.2019_05_27*LD-22543260-2019.5.26.2019.5.27*LG-22543262-2.1.F.',
    # 'TAReturnTo': '%1%%2FHotels%3Fdf%3D%26zfn%3D%26reqNum%3D1%26zfp%3D%26ns%3D%26isLastPoll%3Dfalse%26zft%3D%26g%3D298484%26bs%3D%26puid%3DXNqF-8CoATQAA0-cgzsAAAF6%26distFrom%3D%26sl_opp_json%3D%7B%7D%26paramSeqId%3D8%26distFromPnt%3D%26offset%3D0%26cat_tag%3D9189%26changeSet%3DFILTERS%2CMAIN_META%26zfc%3D9566%26zfb%3D%26amen%3D%26trating%3D4%2C5%26zfd%3D%26plSeed%3D1730470459%26zff%3D%26pRange%3D605%2C-1%2CRMB%2CALL_IN_WITH_EXCLUSIONS%26waitTime%3D29',
}

headers = {
    'X-Puid': 'XNqF-8CoATQAA0-cgzsAAAF6',
    'Origin': 'https://www.tripadvisor.cn',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': 'text/html, */*',
    'Referer': 'https://www.tripadvisor.cn/Hotels-g298484-Moscow_Central_Russia-Hotels.html',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}

data = {
    'sl_opp_json': '{}',
    'plSeed': '1730470459',
    'offset': '0',
    'zfp': '',
    'zff': '',
    'trating': '4,5',
    'zft': '',
    'bs': '',
    # 'zfc': '9566,9573',
    'cat_tag': '9189',
    'amen': '',
    'df': '',
    'zfd': '',
    'distFrom': '',
    'zfb': '',
    'zfn': '',
    'ns': '',
    'pRange': '605,-1,RMB,ALL_IN_WITH_EXCLUSIONS',
    'distFromPnt': '',
    'reqNum': '1',
    'isLastPoll': 'false',
    'paramSeqId': '9',
    'waitTime': '254',
    'changeSet': 'FILTERS,MAIN_META',
    'staydates': '2019_05_20_2019_05_26',
    # 'staydates': '2018_05_20_2018_05_25',
    'puid': 'XNqF-8CoATQAA0-cgzsAAAF6'
}

url = 'https://www.tripadvisor.cn/Hotels-g186338-London_England-Hotels.html'
# url = 'https://www.tripadvisor.cn/Hotels-g298484-Moscow_Central_Russia-Hotels.html'
response = requests.post(url, headers=headers,
                         cookies=cookies, data=data)
print(response.text)
