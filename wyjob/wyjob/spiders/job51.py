# -*- coding: utf-8 -*-
import scrapy


class A51jobSpider(scrapy.Spider):
    name = '51job'
    allowed_domains = ['51job.com']
    # start_urls = ['https://www.51job.com/']

    def get_urls(self):
        start_urls = ['https://www.51job.com/']
        return scrapy.Request(start_urls,callback=self.get_categorys)

    def get_categorys(self,response):
        categorys = response.xpath("//*[@class='cn hlist']//*[@class='e']/a/@href")
        for category in categorys:
            print (category.extract())

    # def parse(self, response):
    #     categorys = response.xpath("//*[@class='cn hlist']//*[@class='e']/a/@href")
    #     for category in categorys:
    #         categoryUrl = category


    # def getJobs(self,response):