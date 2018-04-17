# -*- coding: utf-8 -*-
import scrapy
import sys
import os
import re
from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class A8wenkuSpider(scrapy.Spider):
    name = 'biquke'
    allowed_domains = ['www.biquke.com']
    start_urls = ['http://www.biquke.com/bq/44/44385/2713107.html']
    # start_urls = ['http://www.8wenku.com/']

    def parse(self, response):
        title = response.xpath('//*[@id="wrapper"]/div[4]/div/div[2]/h1')
        connent = response.xpath('//*[@id="content"]').extract()
        # dr = re.compile(r'<[^>]+>', re.S)
        # connent = dr.sub('', html)
        print(connent)
        pass


execute(["scrapy", "crawl", "biquke"])
