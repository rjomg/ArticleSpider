# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from scrapy.http import Request
from urllib import parse
from scrapy.loader import ItemLoader

from ArticleSpider.items import JobBoleArticleItem
from ArticleSpider.items import ArticleItemLoader
from ArticleSpider.utils.common import get_md5

import codecs
import json


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']     # 首页地址
    # start_urls = ['http://blog.jobbole.com/']
    #  设置管道
    custom_settings = {
         'ITEM_PIPELINES': {
             'ArticleSpider.pipelines.ArticleImagePipeline': 1,  # 获取图片
             'ArticleSpider.pipelines.MysqlTwistedPipeline': 2,
         },
    }

    def parse(self, response):
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url}, callback=self.parse_details)

        next_urls = response.css(".next.page-numbers::attr(href)").extract_first("")
        yield Request(url=parse.urljoin(response.url, next_urls), callback=self.parse)
        pass


    #   提取文章详情
    def parse_details(self, response):
        front_image_url = response.meta.get("front_image_url", '')  # 文章封面图

        #   通过ItemLoader加载item
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        # xpath 获取方式
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_xpath("title", './/div[@class="entry-header"]/h1/text()')
        item_loader.add_xpath("create_time", "//p[@class='entry-meta-hide-on-mobile']/text()")
        item_loader.add_value("url", response.url)
        item_loader.add_value("front_image_url", [front_image_url])
        item_loader.add_xpath("praise_nums", "//span[contains(@class, 'vote-post-up')]/h10/text()")
        item_loader.add_xpath("fav_nums", "//span[contains(@class, 'bookmark-btn')]/text()")
        item_loader.add_xpath("comment_nums", "//a[@href='#article-comment']/span")
        item_loader.add_xpath("tags", "//p[@class='entry-meta-hide-on-mobile']/a/text()")
        item_loader.add_xpath("content", "//div[@class='entry']")

        article_item = item_loader.load_item()

        yield article_item
