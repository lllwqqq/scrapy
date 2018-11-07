# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from htwSpider.items import HtwXyzpXjhIterm,HtwXyzpJobIterm,HtwXyzpIterm,HtwXjhItem
import hashlib,redis,psycopg2

class HtwspiderPipeline(object):
    def __init__(self):
        self.pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
        self.rediscli = redis.Redis(connection_pool=self.pool)

        self.conn = psycopg2.connect(database="xbdb", user="dbuser", password="123kkk", host='127.0.0.1', port=5433)
        self.cur = self.conn.cursor()
    # def process_item(self, item, spider):
    #     print(self.rediscli.get('test'))
    #     if isinstance(item,HtwXjhItem):
    #         with open('xjh.txt', 'a', encoding='utf-8') as f:
    #             f.write(item['datakey'] + '--')
    #             f.write(item['company'] + '--')
    #             f.write(item['school'] + '--')
    #             f.write(item['address'] + '--')
    #             f.write(item['pushTime'] + '--')
    #             f.write(item['sourceUrl'] + '--')
    #             f.write(item['holdTime'] + '\n')
    #     elif isinstance(item,HtwXyzpIterm):
    #         with open('xyzp.txt', 'a', encoding='utf-8') as f:
    #             f.write(item['company'] + '--')
    #             f.write(item['pushTime'] + '--')
    #             # f.write(item['citys'] + '--')
    #             f.write(item['sourceUrl'] + '\n')
    #     elif isinstance(item, HtwXyzpJobIterm):
    #         with open('xyzpjob.txt', 'a', encoding='utf-8') as f:
    #             f.write(item['job'] + '--')
    #             f.write(item['sourceUrl'] + '\n')
    #     elif isinstance(item, HtwXyzpXjhIterm):
    #         with open('xyzpxjh.txt', 'a', encoding='utf-8') as f:
    #             f.write(item['datakey'] + '--')
    #             f.write(item['sourceUrl'] + '\n')
    def process_item(self, item, spider):
        if isinstance(item,HtwXjhItem):
            company = item['company']
            school = item['school']
            address = item['address']
            pushTime = item['pushTime']
            holdTime = item['holdTime']
            source = item['source']
            sourceurl = item['sourceUrl']
            logo_url = item['logo_url']
            datakey = item['datakey']
            content = item['xjContent']
            sqlstr = """insert into xjh (company,school,address,pushtime,holdtime,sourceurl,datakey,logo_url,source,content) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
            self.cur.execute(sqlstr,(company,school,address,pushTime,holdTime,sourceurl,datakey,logo_url,source,content))
            self.conn.commit()
            self.cur.close
            self.conn.close
        elif isinstance(item,HtwXyzpIterm):
            company = item['company']
            pushTime = item['pushTime']
            citys = item['citys']
            sourceurl = item['sourceUrl']
            logo_url = item['logo_url']
            datakey = item['datakey']
            content = item['content']
            sqlstr = """insert into xyzp (company,citys,pushtime,sourceurl,logo_url,datakey,content) VALUES (%s,%s,%s,%s,%s,%s,%s) """
            self.cur.execute(sqlstr, (company,citys, pushTime, sourceurl,logo_url,datakey,content))
            self.conn.commit()
            self.cur.close
            self.conn.close
        elif isinstance(item, HtwXyzpJobIterm):
            job = item['job']
            company = item['company']
            sourceurl = item['sourceUrl']
            source = item['source']
            sqlstr = """insert into xyzp_job (job,sourceurl,company,source) VALUES (%s,%s,%s,%s) """
            self.cur.execute(sqlstr, (job, sourceurl,company,source))
            self.conn.commit()
            self.cur.close
            self.conn.close
        elif isinstance(item, HtwXyzpXjhIterm):
            datakey = item['datakey']
            sourceurl = item['sourceUrl']
            company = item['company']
            sqlstr = """insert into xyzp_xjh (datakey,sourceurl,company) VALUES (%s,%s,%s) """
            self.cur.execute(sqlstr, (datakey , sourceurl,company))
            self.conn.commit()
            self.cur.close
            self.conn.close
