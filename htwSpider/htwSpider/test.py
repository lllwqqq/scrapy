# coding=utf-8

import re,hashlib,redis
# str1 = '/article/1298398.html'
# pattern = re.compile("[1-9]\d*")
# res = re.findall(pattern, str1)
# print (res)


# pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
# rediscli = redis.Redis(connection_pool=pool)
#
#
# a = '成都新大瀚人力资源管理有限公司'
# b = '成都新大瀚人力资源管理有限公司'
# e = '成都新大瀚人力资源管理有限公司1'
# company_uuida = hashlib.md5(a.encode(encoding='UTF-8')).hexdigest()
# company_uuidb = hashlib.md5(b.encode(encoding='UTF-8')).hexdigest()
# company_uuide = hashlib.md5(e.encode(encoding='UTF-8')).hexdigest()
# dd = company_uuida
# print(type(dd))
# print(rediscli.set(dd,company_uuida))
# print(rediscli.get(dd))
# rediscli.set('COMPANY_UUIDB',company_uuidb)
# rediscli.set('COMPANY_UUIDA',company_uuide)

# c = rediscli.get('COMPANY_UUIDA')
# d = rediscli.get('COMPANY_UUIDB')
# e = rediscli.get('COMPANY_UUIDA')
# print(c,d,e)

# if c == d :
#     print('相等')
# else:
#     print('不等')


abc= "['广州', '深圳', '珠海']"

pattern = ".'"
aa = re.findall(".\'",abc)
print(repr(abc).replace("'",'"'))

