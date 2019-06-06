#coding:utf-8

import re
import scrapy
from lxml import etree
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scripture.models import booking
from scripture.xpath import bookings as bk


class BookingSpider(scrapy.spiders.Spider):
    name = 'booking'
    headers = {
        'Host': 'www.booking.com',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1'
    }
    allXpath = [x for x in dir(bk) if x[0] != '_']

    nameList = []

    def start_requests(self):
        for e in self.nameList:
            yield Request(
                f"https://www.booking.com/searchresults.zh-cn.html?ss={e['name']}",
                callback=self.parse,
                headers=self.headers,
                meta={
                    'hotelName': e['name'],
                    'hotelAddr': e['addr']
                    }
            )

    def parse(self,response):
        et = etree.HTML(response.text)
        if et.xpath('//*[@id="hotellist_inner"]/div[1]/div[2]/div[1]/div[1]/h3/a/@href'):
            bookingInfoUrl = 'https://www.booking.com' + \
                             et.xpath('//*[@id="hotellist_inner"]/div[1]/div[2]/div[1]/div[1]/h3/a/@href')[0].replace(
                                 '\n', '').split('?')[0]
            yield Request(bookingInfoUrl, callback=self.getInfo, headers=self.headers, meta=response.meta)

    def getInfo(self, res):
        if not mch(res):
            return
        response = etree.HTML(res.text)
        loader = ItemLoader(item=booking.Booking(), response=res)
        supplier_obj_id = res.meta.get('statics.hotels.id')
        supplier_name = res.meta.get('statics.hotels.supplier')
        if supplier_obj_id:
            loader.add_value('statics_hotels_id', supplier_obj_id)
            loader.add_value('statics_hotels_supplier', supplier_name)
        pic = []
        for e in self.allXpath:
            Xpath = eval('bk.'+e)
            fielName , lable = '_'.join(e.split('_')[:-1]) , e.split('_')[-1]
            tempResult = ''
            if lable == 'non':
                if response.xpath(Xpath):
                    tempResult = response.xpath(Xpath)[0].strip()
            elif lable == 'ren':
                if re.findall(Xpath,res.text):
                    tempResult = re.findall(Xpath,res.text)[0].strip()
            elif lable == 'rea':
                if re.findall(Xpath,res.text):
                    for each in re.findall(Xpath,res.text):
                        tempResult += each.strip()
            elif lable == 'sub':
                if response.xpath(Xpath):
                    tempResult = re.sub('\\n+','\\n',response.xpath(Xpath)[0].xpath('string(.)')).strip()
            elif lable == 'sua':
                selects,subSelcets,y = Xpath.split('weego')[0] , Xpath.split('weego')[1] ,Xpath.split('weego')[2:]
                for each in response.xpath(selects):
                    temp = each.xpath(subSelcets)
                    if isinstance(temp,list):
                        tempResult += temp[0]
                    elif isinstance(temp,str):
                        tempResult += temp
                tempResult = re.sub('\\n+','\\n',tempResult).strip()
            elif lable == 'pic':
                selects, subSelcets, y = Xpath.split('weego')[0], Xpath.split('weego')[1], Xpath.split('weego')[2:]
                for each in response.xpath(selects):
                    temp = each.xpath(subSelcets)
                    pic.append(
                        temp[0]
                    )
                tempResult = pic
            elif lable == 'pir':
                for each in re.findall(Xpath,res.text):
                    pic.append(
                        each
                    )
                tempResult = pic
            elif lable == 'xpl':
                selects, subSelcets, y = Xpath.split('weego')[0], Xpath.split('weego')[1], Xpath.split('weego')[2:]
                tl = []
                for each in response.xpath(selects):
                    temp = re.sub('\\n+', ' - ', each.xpath(subSelcets).strip())
                    tl.append(temp)
                loader.add_value(fielName.lower(),tl)
            if lable != 'xpl':
                if loader.get_collected_values(fielName.lower()):
                    if loader.get_collected_values(fielName.lower())[0] == '':
                        loader.replace_value(fielName.lower(),tempResult)
                else:
                    loader.add_value(fielName.lower(),tempResult)
        yield loader.load_item()

def mch(response):
    res = etree.HTML(response.text)
    if res.xpath(bk.name_non):
        hName = res.xpath(bk.name_non)[0].strip()
    elif re.findall('"name" : "(.*?)",',response.text):
        hName = re.findall('"name" : "(.*?)",',response.text)[0]
    else:
        hName = res.xpath('//title/text()')[0].strip().split('_')[0]
    hCountry = re.findall('b_countrycode" : \'(.*?)\',',response.text)[0].upper()
    hAddr = res.xpath(bk.ADDRESS_non)[0].strip()
    if hCountry != response.meta['country_code'].strip().upper():
        return False
    name = response.meta['name']
    addr = response.meta['address']
    if name == hName:
        return True
    if (caculate(name,hName) + caculate(addr,hAddr))/2 > 0.8:
        return True
    else:
        return False

def caculate(s1,s2):
    s1 = re.sub('[\.\,&]', '', re.sub('\s+', ' ', s1.strip()).lower())
    s2 = re.sub('[\.\,&]', '', re.sub('\s+', ' ', s2.strip()).lower())
    s1l = [w for w in s1.split(' ') if w != '']
    s2l = [w for w in s2.split(' ') if w != '']
    s1Match = 0.0
    s2Match = 0.0
    for e in s1l:
        if e in s2:
            s1Match += 1.0
    for e in s2l:
        if e in s1:
            s2Match += 1.0
    return max(s1Match/len(s1l),s2Match/len(s2l))
