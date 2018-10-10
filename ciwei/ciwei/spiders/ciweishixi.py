# coding=utf-8

import scrapy
from ciwei.items import CiweiItem


class CiweiSpider(scrapy.Spider):
    # 爬虫的识别名称，必须是唯一的，在不同的爬虫必须定义不同的名字
    name = 'ciweishixi'
    # 爬虫的域名范围，也就是爬虫的约束区域，规定爬虫只爬取这个域名下的网页，不存在的Url会被忽略
    allowd_domains = ['ciweishixi.com']
    # 爬虫的起始Url
    start_urls = ('http://www.ciweishixi.com/search?s_c=1')
    #
    def parse(self, response):
        job_list = response.xpath('//section[@classs="widget item"]')

