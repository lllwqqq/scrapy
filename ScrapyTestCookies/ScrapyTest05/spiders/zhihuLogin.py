# -*- coding: utf-8 -*-
import scrapy


class ZhihuloginSpider(scrapy.Spider):
    name = 'zhihuLogin'
    allowed_domains = ['zhihu.com']
    start_urls = ['https://www.zhihu.com/inbox']

    cookies = {
        '_xsrf': 'dbdcbec4-5fbc-4562-a0db-c39eb9c55fba',
        '_zap': 'a3ca7687-2b34-4159-b859-53c29289859a',
        'cap_id': '"OTVkNGIxZDg0Y2E5NDA5N2E0MGQwMGU5NjYwZjhjOWQ=|1541569640|9fc5247a4cc00e9c2de0c1ade5a6d839febd7c09"',
        'capsion_ticket': '"2|1:0|10:1541569649|14:capsion_ticket|44:YTUyY2U0NWJiNjRmNGZkMmJmMmRiMzkwYzc0YmFlMTI=|2833c458e470cbc0bb217037fb8a48ecd2b038a92c0a521defa9dd7fd2d72b3b"',
        'd_c0': '"AJCovZohew6PTn2cgdHfucO5igwZtwLKZXU=|1541561368"',
        'l_cap_id': '"NGQzZGNhNmI0MzZiNDQ4MGE1MzVlNmNlN2I1MTA1MzY=|1541569640|3bb5e734bcb086029b1fe785a28a414433ea58c1"',
        'l_n_c': '1',
        'n_c': '1',
        'q_c1': 'df56947ffd05465ca443f193fd4898bf|1541569616000|1541569616000',
        'r_cap_id': '"YTRjZTgwMGVjYmY0NDJhZmE1NjBiNTJmMTZkODEzM2U=|1541569640|6d391587c027238145092f8f20e3723f18446359"',
        'tgw_l7_route': '200d77f3369d188920b797ddf09ec8d1',
        'z_c0': '"2|1:0|10:1541569659|4:z_c0|92:Mi4xSWRRLUJRQUFBQUFBa0tpOW1pRjdEaVlBQUFCZ0FsVk5lOHJQWEFDQmFTWlI2NTA0NlppeUlhNFRKaTdSWmNLcHNR|ab01d9007936bc08fb4586573978b55ddec924c35cc2670117ed2f934000dbaa"'
    }

    # 重写Spider类的start_requests方法，附带Cookie值，发送POST请求
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.FormRequest(url, cookies=self.cookies, callback=self.parse_page)

    # 处理响应内容
    def parse_page(self, response):
        with open('zhihu.html', 'wb') as filename:
            filename.write(response.body)
