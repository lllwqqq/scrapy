# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2
from rsfdSpider.items import RsfdspiderItem

class RsfdspiderPipeline(object):
    def __init__(self):


        self.conn = psycopg2.connect(database="xbdb", user="dbuser", password="123kkk", host='127.0.0.1', port=5433)
        self.cur = self.conn.cursor()
    def process_item(self, item, spider):
        if isinstance(item, RsfdspiderItem):
            url = item['url']
            job = item['job']
            company = item['company']
            company_info = item['company_info']
            example_time = item['example_time']
            job_cycle = item['job_cycle']
            job_team = item['job_team']
            job_salary = item['job_salary']
            job_addr = item['job_addr']
            job_industry = item['job_industry']
            job_num = item['job_num']
            hr_name = item['hr_name']
            sqlstr = """insert into risfond (url,job,company,example_time,job_cycle,job_team,job_salary,job_addr,job_industry,job_num,hr_name,company_info) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
            self.cur.execute(sqlstr, (url,job,company,example_time,job_cycle,job_team,job_salary,job_addr,job_industry,job_num,hr_name,company_info))
            self.conn.commit()
            self.cur.close
            self.conn.close