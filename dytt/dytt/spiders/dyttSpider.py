# -*- coding: utf-8 -*-
import scrapy
from dytt.items import DyttItem

class DyttspiderSpider(scrapy.Spider):
    name = 'dyttSpider'
    allowed_domains = ['haomagujia.com']

    def start_requests(self):
        for page in range(1,417):
            # print(type(page))
            start_urls = ('https://www.haomagujia.com/jiaoyi/?page=%s' %page)
            # print (start_urls)
            yield scrapy.Request(start_urls, callback=self.parse)






    def parse(self, response):
        item = DyttItem()
        tels = response.xpath("//*[@class='jg66_list']/a/text()")
        for tel in tels:

            item['phone'] = tel.extract()
            print (tel.extract())
            yield item

        # return item

