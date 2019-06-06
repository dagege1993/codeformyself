staydates: 2019_05_29_2019_05_30
import requests

cookies = {
    '$CommercePopunder': 'SuppressAll*1557803321223',
    'TASSK': 'enc%3AAJ2vx2yuK89hh0vB4ZRH5xZ58rsk%2F6xiA6O6haONvloaNKe%2BAPvNrjesyprLFvWIHUOn%2B1RZpUr0KFhFX5T534z0GMR2IrrYcMISChZxXhq3hG%2FPkxtVddcDGbolQFI%2BUw%3D%3D',
    'BEPIN': '%1%16ab45049ff%3Bweb08c.daodao.com%3A10023%3B',
    'ServerPool': 'C',
    'TART': '%1%enc%3AQZpLz%2BcEhM6H%2Bw2oezto5iymIzCMNuPP%2BGqsfk0hkcqQe3bS7YQnAe2mZw%2FOK0EWAJJVOu6GcoE%3D',
    'TAUnique': '%1%enc%3AvkH%2FTMQPxHUNSJTzw8g7nz%2BY75sxo05EY2mpsyNZzXh9i1%2B2aew%2BBQ%3D%3D',
    '_gcl_au': '1.1.723677213.1557808777',
    '_ga': 'GA1.2.53421744.1557808777',
    '_gid': 'GA1.2.1654778507.1557808777',
    '_smt_uid': '5cda8416.7159805',
    'roybatty': 'TNI1625\\u21ADHHNzEl%2FB7Rv7dxAiTbfcyfC%2F4lRZmMSJo6IQkQsd2pe90cA7YldQBVFpmL58Rj6KvReMjJScsESo%2BSeQarVCK4FjZp0xhVJmcNMKvF88Qpr8avbgrx69aIRAikG%2BqkHuCFQULwmAYWA2XwSCovQJV1asaglyDZDT1Kvlxdyqtw%2C1',
    'SRT': '%1%enc%3AQZpLz%2BcEhM6H%2Bw2oezto5iymIzCMNuPP%2BGqsfk0hkcqQe3bS7YQnAe2mZw%2FOK0EWAJJVOu6GcoE%3D',
    'TATravelInfo': 'V2*AY.2019*AM.5*AD.29*DY.2019*DM.5*DD.30*A.2*MG.-1*HP.2*FL.3*DSM.1557827903780*AZ.1*RS.1',
    'CM': '%1%PremiumMobSess%2C%2C-1%7Ct4b-pc%2C%2C-1%7CRestAds%2FRPers%2C%2C-1%7CRCPers%2C%2C-1%7CWShadeSeen%2C%2C-1%7CTheForkMCCPers%2C%2C-1%7CHomeASess%2C2%2C-1%7CPremiumSURPers%2C%2C-1%7CPremiumMCSess%2C%2C-1%7CRestPartSess%2C%2C-1%7CUVOwnersSess%2C%2C-1%7CRestPremRSess%2C%2C-1%7CCCSess%2C%2C-1%7CCYLSess%2C%2C-1%7CPremRetPers%2C%2C-1%7CViatorMCPers%2C%2C-1%7Csesssticker%2C%2C-1%7CPremiumORSess%2C%2C-1%7Ct4b-sc%2C%2C-1%7CRestAdsPers%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS2%2C%2C-1%7Cb2bmcpers%2C%2C-1%7CPremMCBtmSess%2C%2C-1%7CPremiumSURSess%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS%2C%2C-1%7CLaFourchette+Banners%2C%2C-1%7Csess_rev%2C%2C-1%7Csessamex%2C%2C-1%7CPremiumRRSess%2C%2C-1%7CTADORSess%2C%2C-1%7CAdsRetPers%2C%2C-1%7CTARSWBPers%2C%2C-1%7CSPMCSess%2C%2C-1%7CTheForkORSess%2C%2C-1%7CTheForkRRSess%2C%2C-1%7Cpers_rev%2C%2C-1%7Cmds%2C1557827903677%2C1557914303%7CSPMCWBPers%2C%2C-1%7CRBAPers%2C%2C-1%7CRestAds%2FRSess%2C%2C-1%7CHomeAPers%2C%2C-1%7CPremiumMobPers%2C%2C-1%7CRCSess%2C%2C-1%7CLaFourchette+MC+Banners%2C%2C-1%7CRestAdsCCSess%2C%2C-1%7CRestPartPers%2C%2C-1%7CRestPremRPers%2C%2C-1%7CUVOwnersPers%2C%2C-1%7Csh%2C%2C-1%7Cpssamex%2C%2C-1%7CTheForkMCCSess%2C%2C-1%7CCYLPers%2C%2C-1%7CCCPers%2C%2C-1%7Cb2bmcsess%2C%2C-1%7CSPMCPers%2C%2C-1%7CPremRetSess%2C%2C-1%7CViatorMCSess%2C%2C-1%7CPremiumMCPers%2C%2C-1%7CAdsRetSess%2C%2C-1%7CPremiumRRPers%2C%2C-1%7CRestAdsCCPers%2C%2C-1%7CTADORPers%2C%2C-1%7CTheForkORPers%2C%2C-1%7CPremMCBtmPers%2C%2C-1%7CTheForkRRPers%2C%2C-1%7CTARSWBSess%2C%2C-1%7CPremiumORPers%2C%2C-1%7CRestAdsSess%2C%2C-1%7CRBASess%2C%2C-1%7CSPORPers%2C%2C-1%7Cperssticker%2C%2C-1%7CSPMCWBSess%2C%2C-1%7C',
    'TASession': '%1%V2ID.555561FC987761FB9AC4FAD4E6742F75*SQ.135*LR.https%3A%2F%2Fwww%5C.tripadvisor%5C.cn%2FHotels-g186338-London_England-Hotels%5C.html*LP.%2FHotels%3Fg%3D186338%26reqNum%3D1%26puid%3DXNolXcCoASwAAmjvUsAAAABE%26isLastPoll%3Dfalse%26plSeed%3D1967882847%26sl_opp_json%3D%7B%7D%26waitTime%3D56%26paramSeqId%3D0%26changeSet%3DMAIN_META*LS.DemandLoadAjax*GR.78*TCPAR.58*TBR.37*EXEX.12*ABTR.46*PHTB.75*FS.24*CPU.29*HS.popularity*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*FA.1*DF.0*TRA.true*LD.186338',
    'TAUD': 'LA-1557803322751-1*RDD-1-2019_05_14*HC-23011118*HDD-23018176-2019_05_26.2019_05_27*HD-24580934-2019_05_29.2019_05_30.186338*G-24580935-2.1.186338.*LD-24583423-2019.5.29.2019.5.30*LG-24583426-2.1.T.*ARDD-24583427-2019_05_292019_05_30',
    'TAReturnTo': '%1%%2FHotels%3Fg%3D186338%26offset%3D0%26reqNum%3D2%26puid%3DXNqLJMCoASwAA9RjQ84AAAA7%26zfp%3D%26isLastPoll%3Dfalse%26plSeed%3D409644502%26sl_opp_json%3D%7B%7D%26zff%3D%26waitTime%3D2496%26paramSeqId%3D14%26changeSet%3D',
}

headers = {
    'X-Puid': 'XNqLJMCoASwAA9RjQ84AAAA7',
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
    'plSeed': '409644502',
    'offset': '0',
    'zfp': '',
    'zff': '',
    'reqNum': '3',
    'isLastPoll': 'false',
    'paramSeqId': '14',
    'waitTime': '5852',
    'changeSet': '',
    'puid': 'XNqLJMCoASwAA9RjQ84AAAA7',
    # 'staydates': '2019_05_29_2019_05_30'
}

response = requests.post('https://www.tripadvisor.cn/Hotels-g186338-London_England-Hotels.html', headers=headers,
                         # cookies=cookies,
                         data=data)
print(response.text)
