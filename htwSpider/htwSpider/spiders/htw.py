# -*- coding: utf-8 -*-
import scrapy
from ..items import HtwXjhItem, HtwXyzpIterm, HtwXyzpJobIterm, HtwXyzpXjhIterm
import re, hashlib, redis


class HtwSpider(scrapy.Spider):
    name = 'htw'
    allowed_domains = ['haitou.cc']


    def __init__(self):
        self.pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
        self.rediscli = redis.Redis(connection_pool=self.pool)

    def start_requests(self):
        start_urls = ['https://xyzp.haitou.cc', 'https://xjh.haitou.cc/']
        for start_url in start_urls:
            if 'xyzp' in start_url:
                tag = 'xyzp'
                yield scrapy.Request(start_url, callback=self.crawlXyzpLists, meta={'start_url': start_url,'tag':tag})
            # elif 'xjh' in start_url:
            #     tag = 'xjh'
            #     yield scrapy.Request(start_url, callback=self.crawlXjhLists, meta={'start_url': start_url,'tag':tag})
            else:
                pass

    # 获取城市简称
    def crawlXjhLists(self, response):
        if response:
            citys = response.xpath('//div[contains(@class, "dropdown-city")]/a')
            for city in citys:
                start_url = response.meta['start_url']
                yield scrapy.Request(start_url + '{}'.format(city.xpath('./@data-value').extract_first()), callback=self.crawlNextPage, meta={'start_url': start_url,'tag':response.meta['tag']})


    def crawlXyzpLists(self, response):
        nextPage = response.xpath("//*[@class='grid-view']/ul/li[@class='next']/a/@href").extract_first()
        tag = response.meta['tag']
        if nextPage:
            comInfos = response.xpath("//table[@class='table cxxt-table']/tbody/tr")
            for comInfo in comInfos:
                start_url = response.meta['start_url']
                nextPageHref = comInfo.xpath("./td[@class='cxxt-title']/a/@href").extract_first()
                company = comInfo.xpath("./td[@class='cxxt-title']/a/div[@class='text-success company']/text()").extract_first()
                nextPageUrl = start_url + nextPageHref
                yield scrapy.Request(nextPageUrl, callback=self.parseXYZP, meta={'start_url': start_url, 'company': company,'tag':tag})
            yield scrapy.Request(start_url + nextPage, callback=self.crawlXyzpLists, dont_filter=True, meta={'start_url': start_url,'tag':tag})

    # 爬取公司校园招聘详情页面函数
    def parseXYZP(self, response):
        tag = response.meta['tag']
        # 获取校园招聘页面所有内容
        pageLeft = response.xpath("//*[@class='page-left']")
        # 匹配标题span(简章正文、职位列表、宣讲会列表、公司相册等)
        companyTitles = response.xpath("//div[@class='panel xjh-article-panel panel-content']/div[@class='panel-heading']/div[@class='panel-title']/span/text()").extract()
        sourceUrl = response.url
        company = response.meta['company']
        xjhList = response.xpath("//*[@class='page-left']//div[@class='panel-body xjhlist']//tbody/tr")
        datakeys = xjhList.xpath("./td[@class='cxxt-title']/a/@href").extract()
        # 获取标题名字，判断是否关联宣讲会系统里面的宣讲会
        for title in companyTitles:
            if '宣讲会列表' in title:
                itermXyzpXjh = HtwXyzpXjhIterm()
                for data in datakeys:
                    datakey = data.split('=')[-1]
                    if self.rediscli.get(datakey):
                        pass
                    else:
                        xjhArticleUrl = 'https://xjh.haitou.cc/article/{}.html'.format(datakey)
                        itermXyzpXjh['datakey'] = datakey
                        itermXyzpXjh['company'] = company
                        itermXyzpXjh['sourceUrl'] = sourceUrl
                        yield itermXyzpXjh
                        # 获取到公司对应的宣讲会datakey后，返给解析宣讲会页面函数处理
                        datakeyuuid = hashlib.md5(datakey.encode(encoding='UTF-8')).hexdigest()
                        self.rediscli.set(datakey, datakeyuuid)
                        yield scrapy.Request(xjhArticleUrl, callback=self.parseXjhPage, meta={'company': company, 'datakey': datakey,'tag':tag})
            elif '职位列表' in title:
                # 获取校园招聘页面职位列表
                pattern = re.compile(r'[^\d]+(\d+)[^\d]+')
                redatakey = re.findall(pattern, response.url)
                datakey = redatakey[0]
                if self.rediscli.get(datakey):
                    pass
                else:
                    datakeyuuid = hashlib.md5(datakey.encode(encoding='UTF-8')).hexdigest()
                    self.rediscli.set(datakey, datakeyuuid)
                    itermXyzp = HtwXyzpIterm()
                    itermXyzpJob = HtwXyzpJobIterm()
                    jobList = pageLeft.xpath(".//div[@class='panel-body']//span/text()").extract()
                    pushTime = pageLeft.xpath(".//div[@class='info-item post-time text-ellipsis']//p[@class='text-ellipsis']/span[2]/text()").extract_first()
                    ucitys = pageLeft.xpath(".//div[@class='info-item cities text-ellipsis']/p[@class='text-ellipsis']/span[@class='item-content']/text()").extract()
                    logo_url = response.xpath("//div[@class='article-logo']/img/@src").extract_first()
                    content = response.xpath("//div[@class='panel xjh-article-panel panel-content']/div[@class='panel-body article-content']").extract_first()
                    citys = repr(ucitys).replace("'", '"')
                    itermXyzp['company'] = response.meta['company']
                    itermXyzp['pushTime'] = pushTime
                    itermXyzp['citys'] = citys
                    itermXyzp['sourceUrl'] = sourceUrl
                    itermXyzp['logo_url'] = logo_url
                    itermXyzp['datakey'] = datakey
                    itermXyzp['content'] = content
                    source = response.meta['tag']
                    yield itermXyzp
                    for job in jobList:
                        itermXyzpJob['company'] = company
                        itermXyzpJob['job'] = job
                        itermXyzpJob['source'] = source
                        itermXyzpJob['sourceUrl'] = sourceUrl
                        yield itermXyzpJob
            else:
                pass

    # 开始爬取宣讲会内容

    def crawlNextPage(self, response):
        nextPage = response.xpath("//*[@class='next']//@href").extract_first()
        xjhLists = response.xpath("//div[@class='grid-view']//*[@class='table cxxt-table']/tbody/tr")
        start_url = response.meta['start_url']

        for xjhList in xjhLists:
            xjhTag = xjhList.xpath("./td[@class='cxxt-title']/span[@class='badge badge-warning badge-yellow']/text()").extract_first()
            xjhArticleHUrl = xjhList.xpath("./td[@class='cxxt-title']/a/@href").extract_first()
            xjhArticleUrl = start_url + xjhArticleHUrl.strip('/')
            company = xjhList.xpath("./td[@class='cxxt-title']/a/div[@class='text-success company pull-left']/text()").extract_first()

            if '云宣讲' == xjhTag:
                pass
            else:
                pattern = re.compile(r'[^\d]+(\d+)[^\d]+')
                redatakey = re.findall(pattern, xjhArticleHUrl)
                datakey = redatakey[0]
                if self.rediscli.get(datakey):
                    pass
                else:
                    datakeyuuid = hashlib.md5(datakey.encode(encoding='UTF-8')).hexdigest()
                    self.rediscli.set(datakey,datakeyuuid)
                    yield scrapy.Request(xjhArticleUrl, callback=self.parseXjhPage, meta={'company': company, 'datakey': datakey,'tag':response.meta['tag']})
        if nextPage:
            nextPage = nextPage.strip('/')
            nextPageUrl = start_url + nextPage
            yield scrapy.Request(nextPageUrl, callback=self.crawlNextPage, dont_filter=True, meta={'start_url': start_url,'tag':response.meta['tag']})
        else:
            print('这是最后一页啦!!')

    def parseXjhPage(self, response):
        iterm = HtwXjhItem()
        xjhContent = response.xpath("//*[@class='page-left']")
        company = response.meta['company']
        school = xjhContent.xpath(".//div[@class='main-info']/div[@class='main-info-item col-xs-6'][1]/p[@class='text-ellipsis'][1]/span[2]/text()").extract_first()
        address = xjhContent.xpath(".//div[@class='main-info']/div[@class='main-info-item col-xs-6'][2]/p[@class='text-ellipsis'][1]/span[2]/text()").extract_first()
        pushTime = xjhContent.xpath(".//div[@class='main-info']/div[@class='main-info-item col-xs-6'][1]/p[@class='text-ellipsis'][2]/span[2]/span[1]/text()").extract_first()
        holdTime = xjhContent.xpath(".//div[@class='main-info']/div[@class='main-info-item col-xs-6'][2]/p[@class='text-ellipsis'][2]/span[2]/text()").extract_first()
        logo_url = response.xpath("//div[@class='article-logo']/img/@src").extract_first()
        xjContent = response.xpath("//div[@class='panel-body article-content']").extract_first()
        if address:
            iterm['address'] = address
        else:
            iterm['address'] = "待定"
        iterm['sourceUrl'] = response.url
        iterm['source'] = response.meta['tag']
        iterm['datakey'] = response.meta['datakey']
        iterm['company'] = company
        if school:
            iterm['school'] = school
        else:
            iterm['school'] = "待定"
        if pushTime:
            iterm['pushTime'] = pushTime
        else:
            iterm['pushTime'] = "待定"
        if holdTime:
            iterm['holdTime'] = holdTime
        else:
            iterm['holdTime'] = "待定"
        if xjContent:
            iterm['xjContent'] = xjContent
        else:
            iterm['xjContent'] = "暂无"
        if logo_url:
            iterm['logo_url'] = logo_url
        else:
            iterm['logo_url'] = "无"
        yield iterm
