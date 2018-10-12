# -*- coding: utf-8 -*-
import scrapy


class A51jobSpider(scrapy.Spider):
    name = '51job'
    allowed_domains = ['51job.com']


    def start_requests(self):
        start_urls = ('https://www.51job.com/')
        yield scrapy.Request(start_urls,callback=self.parse)

    def parse(self, response):
        categorys = response.xpath("//*[@class='cn hlist']//*[@class='e']/a/@href")
        for category in categorys:
            print (category.extract())
            print ('-'*10+'>')

