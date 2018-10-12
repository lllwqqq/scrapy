# -*- coding: utf-8 -*-
import os
import json
import math
import scrapy
import logging
import psycopg2
from HTXJ.utils import define
from psycopg2.extras import RealDictCursor
from HTXJ.utils.utils import CreateGUID, GetMD5, Todate
from HTXJ.items import HtxjItem, HtxjCancelItem, HtxjUpdateItem


class XjhSpider(scrapy.Spider):
    name = 'xjh'

    def __init__(self, **kwargs):
        super(XjhSpider, self).__init__(**kwargs)
        self.school_dict = dict()
        with open(os.path.join(os.getcwd(), 'school.json')) as f_obj:
            self.school_dict = json.load(f_obj)
        self.item_per_page = 20.0
        self.conn = psycopg2.connect(database=define.g_db_database, user=define.g_db_user, password=define.g_db_password, host=define.g_db_host, port=define.g_db_port)
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)

    def start_requests(self):
        yield scrapy.Request('https://xjh.haitou.cc', callback=self.parse, errback=self.errback, meta={'callback': 'parse'})

    def parse(self, response):
        if response:
            data_value_lst = response.xpath(u'//div[contains(@class, "dropdown-city")]/a')
            for data_value in data_value_lst:
                name = data_value.xpath(u'./text()').extract_first()
                yield scrapy.Request('https://xjh.haitou.cc/{}'.format(data_value.xpath(u'./@data-value').extract_first()), callback=self.crawlSchool, errback=self.errback, meta={'name': name, 'callback': 'crawlSchool'})

    def crawlSchool(self, response):
        if response:
            total_item_sel = response.xpath(u'//span[@class="text-success"]/text()')
            if total_item_sel:
                total_item = int(total_item_sel.extract_first())
            else:
                return
            total_page = int(math.ceil(total_item / self.item_per_page))
            yield self.parsePage(response)
            for index in xrange(2, total_page + 1):
                yield scrapy.Request(response.url + '/page-{}'.format(index), callback=self.parsePage, errback=self.errback, meta={'name': response.meta['name'], 'callback': 'parsePage'})

    def parsePage(self, response):
        if response:
            url_lst = response.xpath(u'//tr[@data-source="xjh"]/td[@class="cxxt-title"]/a')
            city = response.xpath(u'//a[contains(@class, "switch-city")]/text()').extract_first().encode('utf8')
            for url in url_lst:
                new_url = 'https://xjh.haitou.cc{}'.format(url.xpath(u'./@href').extract_first())
                murl = GetMD5('_haitou_' + new_url)
                company_name = url.xpath(u'./div/text()').extract_first().strip().encode('utf8')
                begin_time = url.xpath('./../..//span[@class="hold-ymd"]/text()').extract_first().strip().encode('utf8')
                begin_time = Todate(begin_time)
                info = url.root.attrib['title']
                school_name = info[info.index(u'学校：') + 3:]
                school_name = school_name[:school_name.index('\n')].strip().encode('utf8')
                place = url.xpath(u'./../../td[@class="text-ellipsis"]/span/@title').extract_first().strip().encode('utf8')
                publish_time = url.xpath(u'./../../td[@class="cxxt-time"]/text()').extract_first().strip().encode('utf8')
                cancel = url.xpath('string(.)').extract_first()[:2]
                sqlcrt = """SELECT uuid FROM xwa_preach_flow  WHERE status='haitouup' AND murl=%s
                            UNION ALL
                            SELECT uuid FROM xwa_preach_flow  WHERE status='haitou_check' AND murl=%s """
                self.cur.execute(sqlcrt, (murl, murl))
                rv = self.cur.fetchall()
                if rv and (u'取消' in info or cancel == u'取消'):
                    item = HtxjCancelItem()
                    item['place'] = place
                    item['org_url'] = '_haitou_' + new_url
                    yield item
                    continue
                elif rv and (u'变动' in info or u'更改' or u'待定'):
                    item = HtxjUpdateItem()
                    item['company_name'] = company_name
                    item['place'] = place
                    item['begin_time'] = begin_time
                    item['repeat_md5'] = GetMD5(begin_time + place + school_name)
                    item['org_url'] = '_haitou_' + new_url
                    yield item
                    continue
                if not rv:
                    span_lst = url.xpath(u'./../span/text()')
                    if span_lst:
                        span_lst = span_lst.extract()
                        if u'云宣讲' in span_lst:
                            # yield scrapy.Request(new_url, callback=self.parseDetailCloud, meta={'city': city})
                            pass
                        else:
                            yield scrapy.Request(new_url, callback=self.parseDetailNormal, errback=self.errback, meta={'city': city, 'begin_time': begin_time, 'place': place, 'school_name': school_name, 'company_name': company_name, 'publish_time': publish_time, 'callback': 'parseDetailNormal'})
                    else:
                        yield scrapy.Request(new_url, callback=self.parseDetailNormal, errback=self.errback, meta={'city': city, 'begin_time': begin_time, 'place': place, 'school_name': school_name, 'company_name': company_name, 'publish_time': publish_time, 'callback': 'parseDetailNormal'})

    def parseDetailNormal(self, response):
        logging.warning('parse {}'.format(response.url))
        if response:
            item = HtxjItem()
            item['uuid'] = CreateGUID('xpy')
            item['city'] = response.meta['city']
            item['place'] = response.meta['place']
            item['preach_context'] = response.xpath(u'//div[@class="panel-body article-content"]').extract_first()
            item['school_name'] = response.meta['school_name']
            item['org_url'] = '_haitou_' + response.url
            item['begin_time'] = response.meta['begin_time']
            item['publish_time'] = response.xpath(u'string(//*[contains(text(),"发布时间")]/following-sibling::*)').extract_first()
            item['org_name'] = response.xpath(u'//div[contains(text(),"来源：")]/*/text()').extract_first()
            item['preach_context'] = item['preach_context'].replace('\n', '').replace('\r', '').replace('\t', '').replace('height: 25px;', '').encode('utf8') if item['preach_context'] else ''
            item['murl'] = GetMD5(item['org_url'])
            item['status'] = 'haitou'
            item['school_type'] = self.school_dict.get(item['school_name'].decode('utf8'), '').encode('utf8')
            if not item['school_type']:
                return
            title = response.xpath(u'//div[@class="article-title text-ellipsis"]/h1/text()').extract_first()
            if not title:
                title = response.xpath(u'//h1[@class="article-title text-ellipsis"]/text()').extract_first()
            item['title'] = title.strip().encode('utf8') if title else ''
            item['company_name'] = response.meta['company_name']
            if not item['org_name'] or not item['place'] or not item['begin_time'] or not item['company_name'] or not item['school_name']:
                item['status'] = 'uncheck'
            yield item

    def errback(self, failure):
        spider_url = failure.request.url
        callable_func = failure.request.meta['callback']
        if callable_func == 'parse':
            yield scrapy.Request(url=spider_url, callback=self.parse, meta={'callback': 'parse'}, errback=self.errback, dont_filter=True)
        elif callable_func == 'crawlSchool':
            yield scrapy.Request(url=spider_url, callback=self.crawlSchool, meta={'callback': 'crawlSchool'}, errback=self.errback, dont_filter=True)
        elif callable_func == 'parsePage':
            yield scrapy.Request(url=spider_url, callback=self.parsePage, meta={'name': failure.request.meta.get("name"), 'callback': 'parsePage'}, errback=self.errback, dont_filter=True)
        elif callable_func == 'parseDetailNormal':
            yield scrapy.Request(url=spider_url, callback=self.parseDetailNormal, meta={'city': failure.request.meta.get("city"), 'begin_time': failure.request.meta.get("begin_time"), 'place': failure.request.meta.get("place"), 'school_name': failure.request.meta.get("school_name"), 'company_name': failure.request.meta.get("company_name"), 'publish_time': failure.request.meta.get("publish_time"), 'callback': 'parseDetailNormal'}, errback=self.errback, dont_filter=True)
