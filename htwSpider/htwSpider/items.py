# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HtwXjhItem(scrapy.Item):
    datakey = scrapy.Field()
    company = scrapy.Field()
    school = scrapy.Field()
    address = scrapy.Field()
    pushTime = scrapy.Field()
    holdTime = scrapy.Field()
    xjContent = scrapy.Field()
    sourceUrl = scrapy.Field()
    source = scrapy.Field()
    logo_url = scrapy.Field()


class HtwXyzpIterm(scrapy.Item):
    company = scrapy.Field()
    pushTime = scrapy.Field()
    citys = scrapy.Field()
    sourceUrl = scrapy.Field()
    logo_url = scrapy.Field()

class HtwXyzpXjhIterm(scrapy.Item):
    company = scrapy.Field()
    datakey = scrapy.Field()
    sourceUrl = scrapy.Field()

class HtwXyzpJobIterm(scrapy.Item):
    company = scrapy.Field()
    job = scrapy.Field()
    sourceUrl = scrapy.Field()
    source = scrapy.Field()


    