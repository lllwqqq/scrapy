# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import os.path

class DyttPipeline(object):
    fileName = 'phone.txt'
    def process_item(self, item, spider):
        with open('phone.txt', 'a', encoding='utf-8') as f:
            phone = item['phone']
            f.write(phone+'\n')
        return item
