# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RsfdspiderItem(scrapy.Item):
    url = scrapy.Field()
    job = scrapy.Field()
    company = scrapy.Field()
    company_info = scrapy.Field()
    example_time = scrapy.Field()
    job_cycle = scrapy.Field()
    job_team = scrapy.Field()
    job_salary = scrapy.Field()
    job_addr = scrapy.Field()
    job_industry = scrapy.Field()
    job_num = scrapy.Field()
    hr_name = scrapy.Field()
