# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CiweiItem(scrapy.Item):

    jobName = scrapy.Field()
    jobCreateTime = scrapy.Field()
    jobSalary = scrapy.Field()
    jobBase = scrapy.Field()
    jobCompany = scrapy.Field()
    jobCompanyDesc = scrapy.Field()
    jobCompanyLogo = scrapy.Field()
    jobDegree = scrapy.Field()
    jobTags = scrapy.Field()

