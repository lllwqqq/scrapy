# coding=utf-8


import scrapy
from mySpider.items import MyspiderItem

class ItcastSpider(scrapy.Spider):
    # 爬虫的识别名称，必须是唯一的，在不同的爬虫必须定义不同的名字
    name="itcast"
    # 爬虫的域名范围，也就是爬虫的约束区域，规定爬虫只爬取这个域名下的网页，不存在的URL会被忽略
    allowd_domains=["itcast.cn"]
    # 爬虫起始的url
    start_urls=("http://www.itcast.cn/channel/teacher.shtml#",)

    # 解析的方法，每个初始url完成下载将被用
    def parse(self,response):
        teacher_list=response.xpath('//div[@class="li_txt"]')
        # 保存信息的集合
        teacherItem=[]
        for each in teacher_list:
            teacher_name=each.xpath('./h3/text()').extract()[0]
            teacher_title=each.xpath('./h4/text()').extract()[0]
            teacher_info=each.xpath('./p/text()').extract()[0]

            item=MyspiderItem()
            item['name']=teacher_name
            item['title']=teacher_title
            item['info']=teacher_info

            teacherItem.append(item)

        return teacherItem