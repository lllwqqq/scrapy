# -*- coding: utf-8 -*-
import scrapy
from ..items import RsfdspiderItem


class RisfondSpider(scrapy.Spider):
    name = 'risfond'
    allowed_domains = ['risfond.com']
    start_urls = ['http://www.risfond.com/case/all']

    def start_requests(self):
        start_urls = ('http://www.risfond.com/case/all')
        yield scrapy.Request(start_urls,callback=self.parseCaseLists)

    def parseCaseLists(self,response):
        baseUrl = 'http://www.risfond.com'
        caseLists = response.xpath("//div[@class='content-container']/div[@class='case-list']/ul[@class='it-list']/li/span/a/@href").extract()
        nextPage = response.xpath("//div[@class='content-container']/div[@class='case-list']/div[@id='body_pagerBottom']/li[@class='prevnext'][2]/a/@href").extract_first()
        print("+"*50)
        print(baseUrl+nextPage)
        print("+"*50)
        for case in caseLists:
            yield scrapy.Request(baseUrl+case,callback=self.parseJob,dont_filter=True)
        if nextPage:
            yield scrapy.Request(baseUrl+nextPage,callback=self.parseCaseLists,dont_filter=True)

    def parseJob(self,response):
        rsfdspiderItem = RsfdspiderItem()
        company_title = response.xpath("//div[@class='sc_b']/div[@class='sc_js']/h3[@class='sc_js_title']/text()").extract_first()
        if company_title:
            rsfdspiderItem['company_info'] = response.xpath("//div[@class='sc_b']/div[@class='sc_js']/div[@class='sc_js_con']/text()").extract_first()
        else:
            rsfdspiderItem['company_info'] = ""
        exampleDesc = response.xpath("//div[@class='body cgal titleM']/div[@class='sc_box']/div[@class='sc_b']/div[@class='sc_d_b']")
        job = exampleDesc.xpath("./div[@class='sc_d_l cf']/div[@class='sc_d_i'][1]/span[@class='sc_d_con']/text()").extract_first()
        if job:
            rsfdspiderItem['job'] = job
        else:
            rsfdspiderItem['job'] = ""
        job_salary = exampleDesc.xpath("./div[@class='sc_d_l cf']/div[@class='sc_d_i'][2]/span[@class='sc_d_con']/text()").extract_first()
        company = exampleDesc.xpath("./div[@class='sc_d_l cf']/div[@class='sc_d_i'][3]/span[@class='sc_d_con']/text()").extract_first()
        job_addr = exampleDesc.xpath("./div[@class='sc_d_l cf']/div[@class='sc_d_i'][4]/span[@class='sc_d_con']/text()").extract_first()
        example_time = exampleDesc.xpath("./div[@class='sc_d_l cf']/div[@class='sc_d_i'][5]/span[@class='sc_d_con']/text()").extract_first()
        job_industry = exampleDesc.xpath("./div[@class='sc_d_l cf']/div[@class='sc_d_i'][6]/span[@class='sc_d_con']/text()").extract_first()
        job_cycle = exampleDesc.xpath("./div[@class='sc_d_l cf']/div[@class='sc_d_i'][7]/span[@class='sc_d_con']/text()").extract_first()
        job_num = exampleDesc.xpath("./div[@class='sc_d_l cf']/div[@class='sc_d_i'][8]/span[@class='sc_d_con']/text()").extract_first()
        job_team = exampleDesc.xpath("./div[@class='sc_d_l cf']/div[@class='sc_d_i'][9]/span[@class='sc_d_con']/text()").extract_first()
        hr_name = exampleDesc.xpath("./div[@class='sc_user_b']/a/text()").extract_first()
        if hr_name:
            rsfdspiderItem['hr_name'] = hr_name
        else:
            rsfdspiderItem['hr_name'] = ""
        rsfdspiderItem['job_salary'] = job_salary
        rsfdspiderItem['company'] = company
        rsfdspiderItem['job_addr'] = job_addr
        rsfdspiderItem['example_time'] = example_time
        rsfdspiderItem['job_industry'] = job_industry
        rsfdspiderItem['job_cycle'] = job_cycle
        rsfdspiderItem['job_num'] = job_num
        rsfdspiderItem['job_team'] = job_team
        rsfdspiderItem['url'] = response.url
        yield rsfdspiderItem
