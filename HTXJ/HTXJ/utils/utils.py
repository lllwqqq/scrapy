#!/usr/bin/python
# -*- coding: utf8 -*-

import urllib
import urllib2
import hashlib
import random
import string
import time
import re

# convert string to hex
import datetime
import base64
from lxml import etree


class WordCheck(object):
    addressRegex = re.compile(ur"[\u4e00-\u9fa5]+省|[\u4e00-\u9fa5]+市")
    fileMD5Regex = re.compile(r'^\b[A-F0-9]{32}\b$')
    uuidRegex = re.compile(r'^\w{3}_\w{12}$')
    checknumberRegex = re.compile(r'^\d{6}$')
    checkbirthYM = re.compile('^\d{4}-\d{2}$')
    searchBarRegex = re.compile(r'[\*;?_=&\(\)\[\]\<\>%{}\\]')
    usernameRegex = re.compile('[\*;?\\\+=&\(\)\[\]\<\>%{}]')
    emailRegex = re.compile('[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}')
    urlRegex = re.compile('(https?|ftp|file)://')
    telRegx = re.compile('^1[0-9]{10}$')

    @classmethod
    def CheckFileMD5(cls, text):
        rv = cls.fileMD5Regex.match(text)
        if not rv:
            return False
        return True

    @classmethod
    def GetAddress(cls, text):
        match = cls.addressRegex.search(text)
        if match:
            result = match.group()
        else:
            result = u"其他地区"

        return result

    @classmethod
    def CheckUUID(cls, text):
        match = cls.uuidRegex.match(str(text))
        if not match:
            return False
        return True

    @classmethod
    def CheckNubmer(cls, text):
        match = cls.checknumberRegex.match(str(text))
        if not match:
            return False
        return True

    @classmethod
    def CheckBirthYM(cls, text):
        match = cls.checkbirthYM.match(str(text))
        if not match:
            return False
        return True

    @classmethod
    def CheckSearchBar(cls, text):
        """
        返回True表示正常，False表示有非法字符
        """
        if isinstance(text, str) or isinstance(text, unicode):
            match = cls.searchBarRegex.search(text)
            if not match:
                return True
            return False

        return True

    @classmethod
    def CheckUsername(cls, text):
        """
        返回True表示正常，False表示有非法字符
        """
        if isinstance(text, str) or isinstance(text, unicode):
            match = cls.usernameRegex.search(text)
            if not match:
                return True
            return False

        return False

    @classmethod
    def CheckEmail(cls, text):
        """
        返回True表示正常，False表示有非法字符
        """
        if isinstance(text, str) or isinstance(text, unicode):
            # print '--------------->', text
            match = cls.emailRegex.match(text)
            if not match:
                return False
            return True

        return False

    @classmethod
    def CleanUrl(cls, text):
        """
        清晰URl，如果出现http://这种，就去掉，没有就不管,只保留网址部分
        """
        if isinstance(text, str) or isinstance(text, unicode):
            # print '--------------->', text
            outtext = cls.urlRegex.sub('', text)
            return outtext

        return text

    @classmethod
    def CheckTelphone(cls, text):
        """
        返回True表示正常，False表示有非法字符
        """
        if isinstance(text, str) or isinstance(text, unicode):
            # print '--------------->', text
            match = cls.telRegx.match(text)
            if not match:
                return False
            return True

        return False


class DateCheck(object):
    dateRegex = re.compile(r'\b(19|20)?[0-9]{2}[- /.](0?[1-9]|1[012])[- /.](0?[1-9]|[12][0-9]|3[01])\b')

    @classmethod
    def GetDateStr(cls, text):
        match = cls.dateRegex.search(text)
        if match:
            result = match.group()
        else:
            result = ''

        return result


def GetValidStr(orgstr):
    """
    如果参数是None返回'',否则返回字符串本身
    """
    if orgstr is None:
        return ''

    from define import zerotime

    if isinstance(orgstr, datetime.datetime):
        rvtime = orgstr.strftime('%Y-%m-%d %H:%M:%S')
        if rvtime == zerotime:
            return ''
        return orgstr.strftime('%Y-%m-%d')
    return orgstr


def GetValidNum(orgstr):
    """
    如果参数是None返回0,否则返回字数字本身
    """
    if not orgstr:
        return 0

    return orgstr


def toHex(s):
    lst = []
    for ch in s:
        hv = hex(ord(ch)).replace('0x', '')
        if len(hv) == 1:
            hv = '0' + hv
        lst.append(hv)

    return reduce(lambda x, y: x + y, lst)


# convert hex repr to string
def toStr(s):
    return s and chr(string.atoi(s[:2], base=16)) + toStr(s[2:]) or ''


# 把带有html的标签去掉，回车换行去掉，用于计算输入的文字
def CleanHtmlStr(srcstr):
    desstr = re.sub('<[^>]+>', '', srcstr)
    desstr = desstr.replace("\r\n", "")
    desstr = desstr.replace("\r", "")
    desstr = desstr.replace("\n", "")
    return desstr


def RawString(text):
    """
    对字符串进行特殊字符转义
    by whitney (2015.12.29)
    """
    _text = text.strip()
    _text = _text.replace('+', '\+')
    _text = _text.replace('#', '\#')
    return _text


# 可逆解密函数
def CYDecode(s):
    if not s:
        return ''
    htextlist = s.split('X')
    if not htextlist:
        return ''

    htextlist.reverse()
    textlist = []
    for word in htextlist:
        word = word[::-1]
        if word:
            textlist.append(chr(int(word)))
        else:
            textlist.append('')

    return ''.join(textlist)


# base64解密函数
def TYBaseDecode(strdata, skey='snhshf'):
    dic = {
        "O0O0O": "=",
        "o000o": "+",
        "oo00o": "/",
    }
    strArr = StrSplit(multiple_replace(dic, strdata), 2)
    strCount = len(strArr)
    for key, value in enumerate(skey):
        if key <= strCount and strArr[key][1] == value:
            strArr[key] = strArr[key][0]
    rv = base64.b64decode(''.join(strArr))
    return rv


def StrSplit(str, width):
    """
    按长度分隔字符串
    :param str: 字符串
    :param width: 分隔的长度
    :return:
    """
    return [str[x:x + width] for x in range(0, len(str), width)]


def multiple_replace(dic, text):
    """
    将字符串中的某些部分进行替换
    dic = {
     需要被替换的字符串：替换后的字符串
    }
    :param dic:
    :param text:
    :return:
    """
    pattern = "|".join(map(re.escape, dic.keys()))
    return re.sub(pattern, lambda m: dic[m.group()], text)


def PrintHEX(msg):
    for i in range(0, 16):
        print "%3s" % hex(i),
    print
    for i in range(0, 16):
        print "%3s" % "##",
    print
    index = 0
    for temp in msg:
        print "%3s" % temp.encode('hex'),
        index += 1
        if index == 16:
            index = 0
            print


# This class provides the functionality we want. You only need to look at
# this if you want to know how this works. It only needs to be defined
# once, no need to muck around with its internals.
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:  # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False


# 数据库填写当前datetime字段用的格式：YYYY-MM-DD HH:MM:SS
def GetDateTime(timestamp=None):
    if timestamp is None:
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    else:
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))


# 数据库填写当前datetime字段用的格式：YYYY-MM-DD HH:MM:SS
def TransDBDateTime(dbdatetime):
    if isinstance(dbdatetime, datetime.datetime):
        datestr = dbdatetime.strftime('%Y-%m-%d %H:%M:%S')
    else:
        datestr = dbdatetime
    return datestr


def TransDBdateTimeNoYear(dbdatetime):
    if isinstance(dbdatetime, datetime.datetime):
        datestr = dbdatetime.strftime('%m-%d %H:%M:%S')
    else:
        datestr = dbdatetime
    return datestr


def GetDate(timestamp=None):
    if timestamp is None:
        return time.strftime('%Y-%m-%d', time.localtime(time.time()))
    else:
        return time.strftime('%Y-%m-%d', time.localtime(timestamp))


def GetMonth(timestamp=None):
    if timestamp is None:
        return time.strftime('%Y-%m', time.localtime(time.time()))
    else:
        return time.strftime('%Y-%m', time.localtime(timestamp))


def GetElasticDate(timestamp=None, param=None):
    opt = '%Y-%m-%d %H:%M:%S' if not param else param
    if timestamp is None:
        return time.strftime(opt, time.localtime(time.time()))
    else:
        return time.strftime(opt, time.localtime(timestamp))


# 就是time.time()得到的时间，这个是从'%Y-%m-%d %H:%M:%S'格式转换为18289423.23这种格式，用于计算时间间隔
def GetTimpStamp(timestr):
    if timestr is None:
        return 0
    return time.mktime(time.strptime(str(timestr), '%Y-%m-%d %H:%M:%S'))


def isFloatEqual(f1, f2):
    if abs(abs(f1) - abs(f2)) < 0.000001:
        return True
    return False


# 根据单位得到这个单位的时间长度（秒单位）
def GetSecondByUnit(unit):
    second = 0
    for case in switch(unit):
        if case('hour'):
            second = 3600
            break

        if case('day'):
            second = 86400
            break

        if case('month'):
            second = 2592000
            break

        if case('year'):
            second = 31104000
            break

        if case():
            break

    return second


def GetFileMD5(fdfile):
    md5obj = hashlib.md5()
    md5obj.update(fdfile.read())
    hash = md5obj.hexdigest().upper()
    fdfile.seek(0)
    return hash


def GetMD5(orgstr, islower=False):
    m0 = hashlib.md5()
    m0.update(orgstr)
    if islower:
        return m0.hexdigest().lower()
    return m0.hexdigest().upper()


# 深度加密，避免库里直接复制密码就可以生效的漏洞
def DeepEncrypPassword(username, orgpassword, datetimestr):
    if isinstance(datetimestr, datetime.datetime):
        datetimestr = datetimestr.strftime('%Y-%m-%d %H:%M:%S')
    return EncrypPassword(username + orgpassword + datetimestr)


def EncrypPassword(orgStr):
    magic = '@godLoveU$'
    orgStr = magic + orgStr
    orgStr += str(len(orgStr) * 23)
    return GetMD5(orgStr)


def GenerateRandomIntNum(min, max):
    return int(random.randint(min, max))


def CreateGUID(prefix=None, guidlen=12, withpunctuation=False, islower=True):
    gen = GenerateRandomString(guidlen, withpunctuation)
    if prefix is None:
        outstr = gen
    else:
        outstr = '%s_%s' % (prefix, gen)

    if islower:
        return outstr.lower()

    return outstr.upper()


def CreateOPENAPI(prefix=None, guidlen=11, withpunctuation=False):
    gen = GenerateRandomString(guidlen, withpunctuation)
    if prefix is None:
        outstr = gen
    else:
        if prefix == 'id':
            outstr = 's%s' % (gen,)
        elif prefix == 'secret':
            outstr = 'x%s' % (gen,)
        else:
            outstr = gen
    return outstr


def GenerateRandCode(length=6):
    """
    随机产生一个手机校验码字符串，6位全数字
    """
    rdcode = []
    first = True
    while len(rdcode) < length:
        if first is True:
            rnum = str(random.randint(0, 9))
            first = False
        else:
            rnum = random.choice(string.digits)

        rdcode.append(rnum)

    return ''.join(rdcode)


# withpunctuation是否带标点符号
def GenerateRandomString(length, withpunctuation=True, withdigit=True):
    """
    Linux正则命名参考：http://vbird.dic.ksu.edu.tw/linux_basic/0330regularex.php#lang
    [:alnum:]	代表英文大小写字节及数字，亦即 0-9, A-Z, a-z
    [:alpha:]	代表任何英文大小写字节，亦即 A-Z, a-z
    [:blank:]	代表空白键与 [Tab] 按键两者
    [:cntrl:]	代表键盘上面的控制按键，亦即包括 CR, LF, Tab, Del.. 等等
    [:digit:]	代表数字而已，亦即 0-9
    [:graph:]	除了空白字节 (空白键与 [Tab] 按键) 外的其他所有按键
    [:lower:]	代表小写字节，亦即 a-z
    [:print:]	代表任何可以被列印出来的字节
    [:punct:]	代表标点符号 (punctuation symbol)，亦即：" ' ? ! ; : # $...
    [:upper:]	代表大写字节，亦即 A-Z
    [:space:]	任何会产生空白的字节，包括空白键, [Tab], CR 等等
    [:xdigit:]	代表 16 进位的数字类型，因此包括： 0-9, A-F, a-f 的数字与字节

    Python自带常量(本例中改用这个，不用手工定义了)
    string.digits		  #十进制数字：0123456789
    string.octdigits	   #八进制数字：01234567
    string.hexdigits	   #十六进制数字：0123456789abcdefABCDEF
    string.ascii_lowercase #小写字母(ASCII)：abcdefghijklmnopqrstuvwxyz
    string.ascii_uppercase #大写字母(ASCII)：ABCDEFGHIJKLMNOPQRSTUVWXYZ
    string.ascii_letters   #字母：(ASCII)abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
    string.punctuation	 #标点符号：!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~

    以下的不用，有locale问题
    string.lowercase	   #abcdefghijklmnopqrstuvwxyz
    string.uppercase	   #ABCDEFGHIJKLMNOPQRSTUVWXYZ
    string.letters		 #ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz

    以下的不能用
    string.whitespace	  #On most systems this includes the characters space, tab, linefeed, return, formfeed,
    and vertical tab.
    string.printable	   #digits, letters, punctuation, and whitespace
    """
    punctuation = '!$%^&*'

    rdw_seed = string.ascii_letters

    if withdigit:
        rdw_seed += string.digits

    if withpunctuation:
        rdw_seed += punctuation

    rdw = []
    while len(rdw) < length:
        rdw.append(random.choice(rdw_seed))
    return ''.join(rdw)


# --exeTime
# 测试函数执行时间，使用方法，在函数的上一行写@TestExeTime即可
def TestExeTime(func):
    def newFunc(*args, **args2):
        t0 = time.time()
        # print "@%s, {%s} start" % (time.strftime("%X", time.localtime()), func.__name__)
        back = func(*args, **args2)
        # print "@%s, {%s} end" % (time.strftime("%X", time.localtime()), func.__name__)
        print "@%.3fms taken for {%s}" % ((time.time() - t0) * 1000, func.__name__)
        return back

    return newFunc


# --end of exeTime



# 获取模版使用次数显示
def GetDurationStr(duration):
    if duration < 0:
        return '无限次'

    return '%d次' % duration
    #
    # import bisect
    # d = [(0,'小时'), (24-1,'天'), (24*30-1,'月'), (24*30*365-1,'年')]
    # s = [x[0] for x in d]
    # index = bisect.bisect_left(s, hourlen) - 1
    # if index == -1:
    #     return str(hourlen)
    # else:
    #     b, u = d[index]
    # return str(hourlen / (b+1)) + u


def PostToServer(url, parmdict, timeout=30):
    # headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    if not isinstance(parmdict, dict):
        print 'parmdict is not dict'
        return None

    try:
        postData = urllib.urlencode(parmdict)
        req = urllib2.Request(url)
        # print self.urlstr, postData
        req.add_header('Content-Type', "application/x-www-form-urlencoded");
        req.get_method = lambda: 'POST'  # or 'GET','PUT','DELETE'
        response = urllib2.urlopen(req, postData, timeout)
        recvmsg = response.read()
        return recvmsg


    except Exception, e:
        print 'PostToServer: %s' % repr(e)
        return None


def PostXML(url, xml, timeout=30):
    # headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    try:
        req = urllib2.Request(url)
        req.get_method = lambda: 'POST'  # or 'GET','PUT','DELETE'
        response = urllib2.urlopen(req, xml, timeout)
        recvmsg = response.read()
        return recvmsg

    except Exception, e:
        print 'PostXML: %s' % repr(e)
        return None


def PrintSqlStr(sqlstr, parm):
    # pass
    _parm = []
    for p in parm:
        _parm.append("'%s'" % p)
    outstr = sqlstr % tuple(_parm)
    print outstr.decode('utf-8')


def GetRawSqlStr(sqlstr, parm):
    # print('**'+sqlstr)
    if sqlstr == 'Cache':
        r = 'Cache ' + str(parm)
        return r
    # pass
    _parm = []
    for p in parm:
        _parm.append("'%s'" % p)
    outstr = sqlstr % tuple(_parm)
    return outstr.decode('utf-8')


def GetPureStr(rawstr, target_code='utf-8', source_code=None):
    """
    无论进入的字符串是unicode编码中文还是str，都解码成utf-8编码的str返回
    :param rawstr:原始字串
    target_code:目标字串编码
    :return:
    """
    if not rawstr:
        return None

    if isinstance(rawstr, unicode):
        checkstr = rawstr.encode('utf-8')
    else:
        checkstr = rawstr

    if source_code:
        rc = source_code
    else:
        # 没有指定，就自动判断
        import chardet
        # 这个必须要是str才能判断编码
        crv = chardet.detect(checkstr)
        rc = crv['encoding']

    try:
        dstr = checkstr.decode(rc)
    except Exception as e:
        dstr = checkstr.decode('utf-8')
    # 先按照本身编码转换为unicode，然后再最终用utf-8编码成str返回
    try:
        outstr = dstr.encode(target_code)
    except Exception as e:
        outstr = dstr.encode('utf-8')
    return outstr


def FixedEmailAddress(email_str):
    """
    对email地址整形，中间有空格的，前后有空格的都去掉，让发送邮件有点鲁棒性
    :param email_str:
    :return:
    """
    if not email_str:
        return ''
    _estr = email_str.strip()
    _estr = _estr.replace(' ', '')
    _estr = _estr.replace(',', '.')
    _estr = _estr.replace('，', '.')
    _estr = _estr.replace('。', '.')
    return _estr


def FixedEmailList(email_str):
    """
    处理多个email组成的字符串，把分隔符号替换为标准的 ";"
    :param email_str:
    :return:
    """
    _estr = email_str.strip()
    _estr = _estr.replace(' ', ';')
    _estr = _estr.replace('；', ';')
    _estr = _estr.replace('，', ';')
    _estr = _estr.replace('。', ';')
    _estr = _estr.replace(',', ';')
    return _estr


def GetWXRealFee(fee_yuan):
    """
    微信采用分计费的方式，比如1就是0.01元，这里切换真实的显示单位和微信单位
    :param fee: 元单位的值
    :return:分单位的值字符串！
    """
    return str(int(round(float(fee_yuan) * 100.0)))


def Todate(date):
    """
    处理将日期提取出来
    :param data:
    :return:
    """
    t = re.findall(r"\d+\.?\d*", date)
    print "处理日期:", t
    if len(t) == 3:
        y, m, d = t
        return ''.join([y, '-', m, '-', d, ' ', '00', ':', '00', ':00'])
    elif len(t) == 4:
        y, m, d, h = t[0:4]
        return ''.join([y, '-', m, '-', d, ' ', h, ':', ':00', ':00'])
    elif len(t) > 4:
        y, m, d, h, mm = t[0:5]
        return ''.join([y, '-', m, '-', d, ' ', h, ':', mm, ':00'])
    else:
        pass


def get_url(context):
    url = []
    pattren = '[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?'
    for i in re.findall(pattren, context):
        url.append(i)
    return url


def Get_WangShen(context, org_url):
    page = etree.HTML(context.decode('utf-8'))
    wang = page.xpath(u"//*[contains(text(),'网申')]")
    a = '.'.join(org_url.split('.')[:2])
    apply_context = ''
    c = []
    if wang:
        for i in wang:
            apply_context += i.xpath('string(.)')
        url = page.xpath(u"//a[@href]")
        if url:
            for ll in url:
                print a, ll, a not in ll, '-------------------->'
                if len(ll.attrib['href'].split('http')) > 1 and len(ll.attrib['href'].split('weibo')) <= 1 and len(ll.attrib['href'].split('baike')) <= 1 and a not in ll.attrib['href'].encode('utf-8'):
                    c.append(ll.attrib['href'].encode('utf-8'))
        else:
            c = get_url(page.xpath('string(.)'))

    if c:
        return {'url': list(set(c)),
                'apply_context': apply_context.encode('utf-8')}

    return None
