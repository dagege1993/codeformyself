# -*- coding: utf-8 -*-
import spidermodule
import scrapy
from scrapy_splash import SplashRequest


class HttpbinSpider(scrapy.Spider):
	name = 'httpbin'
	allowed_domains = ['httpbin.org']
	
	def start_requests(self):
		url = 'http://httpbin.org/get'
		for i in range(4):
			# yield scrapy.Request(url=url, callback=self.parse, dont_filter=True, )
			yield SplashRequest(url=url, callback=self.parse, dont_filter=True, )
	
	def parse(self, response):
		print('这是httpbin 返回结果')
		self.logger.debug(response.text)
		self.logger.debug('Status Code: ' + str(response.status))


class Spider(scrapy.Spider):
	name = 'ip'
	allowed_domains = ["ip.chinaz.com"]
	
	def start_requests(self):
		url = 'http://ip.chinaz.com/getip.aspx'
		
		for i in range(4):
			# yield scrapy.Request(url=url, callback=self.parse, dont_filter=True, )
			yield SplashRequest(url=url, callback=self.parse, args={'wait': 1},
			                    dont_filter=True)  # dont_filter=True，则可以重复请求
	
	#
	def parse(self, response):
		print(response.text)



