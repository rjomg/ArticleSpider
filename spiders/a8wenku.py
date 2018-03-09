# # -*- coding: utf-8 -*-
# import scrapy
# import sys
# import os
# from scrapy.cmdline import execute
#
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#
#
# class A8wenkuSpider(scrapy.Spider):
#     name = '8wenku'
#     allowed_domains = ['www.8wenku.com']
#     start_urls = ['http://www.8wenku.com/chapter/view?id=1498&chapter_no=57']
#     # start_urls = ['http://www.8wenku.com/']
#
#     def parse(self, response):
#         title = response.xpath('//*[@id="xtopjsinfo"]/div[2]/div[2]/div/div[1]/h1')
#         connent = response.xpath('//*[@id="xtopjsinfo"]/div[2]/div[2]/div/div[2]/p/text()').extract()
#         print(connent)
#         pass
#
#
# execute(["scrapy", "crawl", "8wenku"])
