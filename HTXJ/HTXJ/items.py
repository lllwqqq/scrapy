# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HtxjItem(scrapy.Item):
    id = scrapy.Field()
    uuid = scrapy.Field()
    recruit_uuid = scrapy.Field()
    city = scrapy.Field()
    place = scrapy.Field()
    preach_context = scrapy.Field()
    school_name = scrapy.Field()
    school_type = scrapy.Field()
    org_url = scrapy.Field()
    begin_time = scrapy.Field()
    end_time = scrapy.Field()
    publish_time = scrapy.Field()
    build_time = scrapy.Field()
    status = scrapy.Field()
    org_name = scrapy.Field()
    company_name = scrapy.Field()
    title = scrapy.Field()
    murl = scrapy.Field()


class HtxjCancelItem(scrapy.Item):
    place = scrapy.Field()
    org_url = scrapy.Field()


class HtxjUpdateItem(scrapy.Item):
    company_name = scrapy.Field()
    place = scrapy.Field()
    begin_time = scrapy.Field()
    org_url = scrapy.Field()
