# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from scrapy.http import HtmlResponse

class XsmSpider(scrapy.Spider):
    name = 'xsm'
    allowed_domains = ['xinshangmeng.com']
    start_urls = ['http://www.xinshangmeng.com/xsm2/']

    # def __init__(self):
    #     self.broswer = None
    #     super(XsmSpider, self).__init__()
    def parse(self, response):
        username = response.xpath(" //div[@id='custDetail']/div/div[2]/div[@class='duiqi1  mt10']/span[2]/text()").extract_first()
        shortname = response.xpath(" //div[@id='custDetail']/div/div[2]/div[@class='duiqi1 mt10']/span[2]/text()").extract_first()
        usercode = response.xpath(" //div[@id='custDetail']/div/div[4]/div[@class='duiqi1 ']/span[2]/text()").extract_first()
        httpUrl = 'http://sc.xinshangmeng.com/eciop/orderForCC/myCoForCC.htm?xsm_user=510106100856&zone=11510101&v=1540966487638'
        yield scrapy.Request(httpUrl,callback=self.testDingDan)

        # print("客户名称：", username)
        # print("客户经理：", usercode)

    def testDingDan(self,response):
        print(response.url,"<<<<<<<<<<<<<<<<<<<<-----------------------")
        print(response.body.decode("utf8"),"---------------->>>>>>>>>>")