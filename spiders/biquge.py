# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse


class BiqugeSpider(scrapy.Spider):
    name = 'biquge'
    allowed_domains = ['www.biquge.com.tw']
    # start_urls = ['http://www.biquge.com.tw/0_32/']
    start_urls = ['http://www.biquge.com.tw/modules/article/soshu.php?searchkey=+%B6%B7']    # 关键字 斗 6页
    # start_urls = ['http://www.biquge.com.tw/modules/article/soshu.php?searchkey=+%C8%AB%D6%B0%B8%DF%CA%D6']    # 全职 1页
    # start_urls = ['http://www.biquge.com.tw/']

    def parse(self, response):
        # 获取列表
        list_urls = response.xpath('//*[@id="nr"]/td[1]/a/@href').extract()
        if list_urls:
            for list_url in list_urls:
                yield Request(url=parse.urljoin(response.url, list_url), callback=self.parse_list)

        # 获取下一页
        next_url = response.css('.next::attr(href)').extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)
        pass

    def parse_list(self, response):
        title = response.xpath('//*[@id="info"]/h1/text()')    # 小说标题
        author = response.xpath('//*[@id="info"]/p[1]/text()').extract()[0].strip()     # 作者
        last_update_time = response.xpath('//*[@id="info"]/p[3]/text()')    # 最后更新时间
        list = response.xpath('//*[@id="list"]/dl/dd/a/@href').extract()   # 列表

        if list:
            post_urls = []
            for each in list:
                # post_urls.append(parse.urljoin(response.url, each))
                yield Request(url=parse.urljoin(response.url, each), callback=self.parse_details)

        pass

    def parse_details(self, response):
        title = response.css('.bookname h1::text')
        content = response.xpath('//*[@id="content"]').extract()

        pass
