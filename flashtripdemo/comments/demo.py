import requests

url = "https://www.tripadvisor.cn/Hotels-g294265-Singapore-Hotels.html"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    # 'Cookie': 'TART=%1%enc%3A7GskRNQPyBJa6Pb3gLQ%2B%2FP0SYzIvXw9JKp5tIjGvW1WgNbFhr8K%2BuVSR7pS2hmocNox8JbUSTxk%3D; TAUnique=%1%enc%3ADppjTohHWhmUxQHg3frr9S6FhopQyGZEbrskVrljX8o%3D; TASSK=enc%3AALus3yTDwV%2BdMNU%2BNb3%2FNtTcissei9IMOXA7aP9g%2BNHCM%2BHnmGUp2C8xs5mWN4Fr%2FQjM485miz7K43J0dEVWIct1tbfXmSptpGeCFqfazsV8%2FzcV80w%2BeO6KiT5UHLrbVQ%3D%3D; ServerPool=C; _gcl_au=1.1.1928727886.1557384961; _ga=GA1.2.165149689.1557384961; _gid=GA1.2.1309262413.1557384961; _smt_uid=5cd3cf05.1db4e906; __gads=ID=5195ea6c0a5efae2:T=1557384967:S=ALNI_MYq1knnUzzUHrJAn_JIo89dqijSQw; CM=%1%PremiumMobSess%2C%2C-1%7Ct4b-pc%2C%2C-1%7CRestAds%2FRPers%2C%2C-1%7CRCPers%2C%2C-1%7CWShadeSeen%2C%2C-1%7CTheForkMCCPers%2C%2C-1%7CHomeASess%2C2%2C-1%7CPremiumSURPers%2C%2C-1%7CPremiumMCSess%2C%2C-1%7CRestPartSess%2C%2C-1%7CRestPremRSess%2C%2C-1%7CCCSess%2C%2C-1%7CCYLSess%2C%2C-1%7CPremRetPers%2C%2C-1%7CViatorMCPers%2C%2C-1%7Csesssticker%2C%2C-1%7CPremiumORSess%2C%2C-1%7Ct4b-sc%2C%2C-1%7CRestAdsPers%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS2%2C%2C-1%7Cb2bmcpers%2C%2C-1%7CPremMCBtmSess%2C%2C-1%7CPremiumSURSess%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS%2C%2C-1%7CLaFourchette+Banners%2C%2C-1%7Csess_rev%2C%2C-1%7Csessamex%2C%2C-1%7CPremiumRRSess%2C%2C-1%7CTADORSess%2C%2C-1%7CAdsRetPers%2C%2C-1%7CTARSWBPers%2C%2C-1%7CSPMCSess%2C%2C-1%7CTheForkORSess%2C%2C-1%7CTheForkRRSess%2C%2C-1%7Cpers_rev%2C%2C-1%7CSPMCWBPers%2C%2C-1%7CRBAPers%2C%2C-1%7CRestAds%2FRSess%2C%2C-1%7CHomeAPers%2C%2C-1%7CPremiumMobPers%2C%2C-1%7CRCSess%2C%2C-1%7CLaFourchette+MC+Banners%2C%2C-1%7CRestAdsCCSess%2C%2C-1%7CRestPartPers%2C%2C-1%7CRestPremRPers%2C%2C-1%7Csh%2C%2C-1%7Cpssamex%2C%2C-1%7CTheForkMCCSess%2C%2C-1%7CCYLPers%2C%2C-1%7CCCPers%2C%2C-1%7Cb2bmcsess%2C%2C-1%7CSPMCPers%2C%2C-1%7CPremRetSess%2C%2C-1%7CViatorMCSess%2C%2C-1%7CPremiumMCPers%2C%2C-1%7CAdsRetSess%2C%2C-1%7CPremiumRRPers%2C%2C-1%7CRestAdsCCPers%2C%2C-1%7CTADORPers%2C%2C-1%7CTheForkORPers%2C%2C-1%7CPremMCBtmPers%2C%2C-1%7CTheForkRRPers%2C%2C-1%7CTARSWBSess%2C%2C-1%7CPremiumORPers%2C%2C-1%7CRestAdsSess%2C%2C-1%7CRBASess%2C%2C-1%7CSPORPers%2C%2C-1%7Cperssticker%2C%2C-1%7CSPMCWBSess%2C%2C-1%7C; BEPIN=%1%16a9b6cdc61%3Bweb08c.daodao.com%3A10023%3B; TATravelInfo=V2*AY.2019*AM.5*AD.19*DY.2019*DM.5*DD.20*A.2*MG.-1*HP.2*FL.3*DSM.1557385763157*RS.1; TAReturnTo=%1%%2FHotels-g294265-Singapore-Hotels.html; TASession=%1%V2ID.E3B149A334922FAE516783F383190DAF*SQ.17*LP.%2F*LS.OverlayWidgetAjax*PD1.2*GR.90*TCPAR.62*TBR.1*EXEX.74*ABTR.49*PHTB.16*FS.35*CPU.30*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*FA.1*DF.0*TRA.true*LD.294265; TAUD=LA-1557384960071-1*RDD-1-2019_05_09*HDD-803032-2019_05_19.2019_05_20*LD-1068583-2019.5.19.2019.5.20*LG-1068585-2.1.F.; roybatty=TNI1625!AMDsyCSeC%2F%2FI%2Fx7%2FurOX2b4demDuF6qmcuBuhrXiR0%2BHil0MH1WBxO7ubl%2BPnKnx3WFQjgqyMd9Cororb91v9D2%2BIh%2Fxn%2BIjDpqDNqsa23vfQHAIhy4qFsM2GIrS%2BOndbANWVZk29zLSHeKVtMr04zSarArhArMPG2A1Aj%2FC5iJz%2C1; SRT=%1%enc%3A7GskRNQPyBJa6Pb3gLQ%2B%2FP0SYzIvXw9JKp5tIjGvW1WgNbFhr8K%2BuVSR7pS2hmocNox8JbUSTxk%3D',
    'X-Requested-With': 'XMLHttpRequest',

}

post_data = {
    'sl_opp_json': {},
    'plSeed': '304484723',
    'reqNum': '2',
    'isLastPoll': 'false',
    'paramSeqId': '0',
    'waitTime': '1001',
    'changeSet': '',
    # 'puid': 'XNPTLMCoAS0ABGs1YQQAAADB',

}

response = requests.request("POST", url, data=post_data, headers=headers, verify=False)
print(response.text)
