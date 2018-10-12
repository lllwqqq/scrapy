# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import json
import logging
import psycopg2
from HTXJ.utils import define, utils
from psycopg2.extras import RealDictCursor
from HTXJ.items import HtxjItem, HtxjUpdateItem, HtxjCancelItem


class HtxjPipeline(object):
    def __init__(self):
        self.conn = psycopg2.connect(database=define.g_db_database, user=define.g_db_user, password=define.g_db_password, host=define.g_db_host, port=define.g_db_port)
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
        self.conn.autocommit = True

    def process_item(self, item, spider):
        if isinstance(item, HtxjItem):
            pattern = '(<div class="for-absolute">.*?</div> |<div class="panel-heading">.*?</div>|<div class="article-affix affix-bottom" style="position: relative;">.*?</div>|<div class="article-toolbox">.*?</div>|<script>.*?</script>|<div class="page-rigth">.*?</div>)'
            context = item['preach_context']
            for i in re.findall(pattern, context):
                context = context.replace(i, '')
            context = (context.decode('utf8').split(u'<!-- 加职位 -->')[0] + '</div>').encode('utf8')
            wang = utils.Get_WangShen(context, item['org_url'][8:])
            if wang:
                apply_urls = wang['url']
                apply_context = context  # wang['apply_context']
                apply_url = apply_urls[0]

                city = [item['city']]
                city = json.dumps(city)

                check = """SELECT uuid,city FROM xwa_recruit_info WHERE company_name = '%s';""" % item['company_name']
                self.cur.execute(check)
                cc = self.cur.fetchall()
                if cc and item['company_name'].strip() != '':
                    pass
                else:
                    if item['company_name'] and item['begin_time']:
                        title = item['company_name'] + str(int(str(item['begin_time']).split('-')[0]) + 1) + '年校招开启'
                    else:
                        title = item['title']
                    ruuid = utils.CreateGUID('xri')
                    repeat_md5 = utils.GetMD5(title)
                    sqlcrl = """ select id from "public"."xwa_recruit_info" WHERE repeat_md5='%s' """ % repeat_md5
                    self.cur.execute(sqlcrl)
                    if not self.cur.fetchall():
                        sqlcrl = """INSERT INTO "public"."xwa_recruit_info" ("uuid","title","city","company_name","status","org_url","begin_time","apply_context","apply_url","apply_url_ext","repeat_md5")
                                                                      VALUES (%s,%s,%s,%s,'uncheck',%s,%s,%s,%s,%s,%s); """
                        self.cur.execute(sqlcrl, (ruuid, title, city, item['company_name'], item['org_url'], item['begin_time'], apply_context, apply_url, json.dumps(apply_urls), repeat_md5))
                    else:
                        logging.warning('url %s duplicate in recruit' % item['org_url'])

                    xpfuuid = utils.CreateGUID('xpy')
                    repeat_md5 = utils.GetMD5(str(item['begin_time']) + item['place'] + item['school_name'])
                    sqlcrl = """ select id from "public"."xwa_preach_flow" WHERE repeat_md5='%s' """ % repeat_md5
                    self.cur.execute(sqlcrl)
                    if not self.cur.fetchall():
                        sqlcrl = """ INSERT INTO "public"."xwa_preach_flow" ("uuid","recruit_uuid","city", "place", "preach_context", "school_name", "school_type", "org_url", "begin_time", "publish_time", "build_time", "status","company_name","title","repeat_md5","org_name","murl")
                                                                  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),%s,%s,%s,%s,%s,%s);"""
                        self.cur.execute(sqlcrl, (xpfuuid, ruuid, item['city'], item['place'], context, item['school_name'], item['school_type'], item['org_url'], item['begin_time'], item['publish_time'], item['status'], item['company_name'], title, repeat_md5, item['org_name'], item['murl']))
                    else:
                        logging.warning('url %s duplicate' % item['org_url'])
                        # Spider.SendMessage('xingzeng', '新增成功', ' ,'.join([school['name'], company, place, start_time]))
            else:
                xpfuuid = utils.CreateGUID('xpy')
                repeat_md5 = utils.GetMD5(str(item['begin_time']) + item['place'] + item['school_name'])
                sqlcrl = """ select id from "public"."xwa_preach_flow" WHERE repeat_md5='%s' """ % repeat_md5
                self.cur.execute(sqlcrl)
                if not self.cur.fetchall():
                    sqlcrl = """ INSERT INTO "public"."xwa_preach_flow" ("uuid","city", "place", "preach_context", "school_name", "school_type", "org_url", "begin_time", "publish_time", "build_time", "status","company_name","title","repeat_md5","org_name","murl")
                                                              VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),%s,%s,%s,%s,%s,%s);"""
                    self.cur.execute(sqlcrl, (xpfuuid, item['city'], item['place'], context, item['school_name'], item['school_type'], item['org_url'], item['begin_time'], item['publish_time'], item['status'], item['company_name'], item['title'], repeat_md5, item['org_name'], item['murl']))
                else:
                    logging.warning('url %s duplicate' % item['org_url'])
                    # Spider.SendMessage('xingzeng','新增成功',' ,'.join([school['name'],company,place,start_time]))
        elif isinstance(item, HtxjUpdateItem):
            sqlcrt = """UPDATE xwa_preach_flow SET company_name = %s,place = %s,begin_time=%s,status='haitouup',repeat_md5 = %s WHERE org_url=%s """
            self.cur.execute(sqlcrt, (item['company_name'], item['place'], item['begin_time'], item['repeat_md5'], item['org_url']))
        elif isinstance(item, HtxjCancelItem):
            sqlcrt = """ UPDATE xwa_preach_flow SET place = %s ,status='haitouup' WHERE org_url=%s  """
            self.cur.execute(sqlcrt, '(暂时取消)' + item['place'], item['org_url'])
