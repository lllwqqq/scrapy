# -*- coding: utf-8 -*-
import scrapy


class HtwSpider(scrapy.Spider):
    name = 'htw'
    allowed_domains = ['haitou.cc']
    start_urls = ['http://haitou.cc/']

    def parse(self, response):
        pass
