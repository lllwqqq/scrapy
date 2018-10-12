#!/usr/bin/python
# -*- coding: utf8 -*-
import json
import psycopg2
from HTXJ.utils import define
from psycopg2.extras import RealDictCursor

if __name__ == '__main__':
    conn = psycopg2.connect(database=define.g_db_database, user=define.g_db_user, password=define.g_db_password, host=define.g_db_host, port=define.g_db_port)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(""" select slug, name from xspy_schools """)
    lst = cur.fetchall()
    store_item = dict()
    for item in lst:
        store_item[item['name']] = item['slug']
    with open('school.json', 'w') as json_file:
        json_file.write(json.dumps(store_item, ensure_ascii=False))
    cur.close()
    conn.close()
