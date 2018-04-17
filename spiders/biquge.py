# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from scrapy.loader import ItemLoader
from urllib import parse
from ArticleSpider.items import BiQuGeListItem
from ArticleSpider.items import BiQuGeItem
from ArticleSpider.utils.common import get_md5
from ArticleSpider.items import ArticleItemLoader


class BiqugeSpider(scrapy.Spider):
    name = 'biquge'
    allowed_domains = ['www.biquge.com.tw']
    start_urls = ['http://www.biquge.com.tw/modules/article/soshu.php?searchkey=+%B6%B7%C2%DE%B4%F3%C2%BD']     # 关键字 斗 6页
    # start_urls = ['http://www.biquge.com.tw/']
    # 自定义
    custom_settings = {
        'ITEM_PIPELINES': {
            'ArticleSpider.pipelines.ArticleImagePipeline': 1,  # 获取图片
            'ArticleSpider.pipelines.MysqlTwistedPipeline': 2,  # mysql异步插入文章列表信息
            'ArticleSpider.pipelines.BiqugeMongoPipeline': 3,   # MongoDB 存入文章内容
        },
    }

    def parse(self, response):
        # 获取列表
        list_urls = response.xpath('//*[@id="nr"]/td[1]/a/@href').extract()
        if list_urls:
            # 循环爬取列表页
            for list_url in list_urls:
                yield Request(url=parse.urljoin(response.url, list_url), callback=self.parse_list)

        # 获取下一页
        next_url = response.css('.next::attr(href)').extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)
        pass

    def parse_list(self, response):
        # 实例化项目
        post_url = response.xpath('//*[@id="fmimg"]/img/@src').extract_first("")    # 图片
        front_image_url = parse.urljoin(response.url, post_url)
        list = response.xpath('//*[@id="list"]/dl/dd/a/@href').extract()   # 列表

        #   通过自定义ArticleItemLoader加载item
        item_loader = ArticleItemLoader(item=BiQuGeListItem(), response=response)
        # xpath 获取方式
        item_loader.add_value("url_object_id", get_md5(response.url))   # MD5ID
        item_loader.add_xpath("title", '//*[@id="info"]/h1/text()')     # 文章标题
        item_loader.add_xpath("author", '//*[@id="info"]/p[1]/text()')  # 作者
        item_loader.add_xpath("last_update_time", '//*[@id="info"]/p[3]/text()')    # 最后更新时间
        item_loader.add_value("front_image_url", [front_image_url])     # 图片下载链接

        article_item = item_loader.load_item()

        yield article_item

        # 循环爬取详情页
        if list:
            post_urls = []
            for each in list:
                # post_urls.append(parse.urljoin(response.url, each))
                yield Request(url=parse.urljoin(response.url, each), meta={"url_object_id": article_item['url_object_id']}, callback=self.parse_details)

        pass

    def parse_details(self, response):
        # 实例化项目
        url_object_id = response.meta.get("url_object_id", '')  # 文章封面图

        # 通过默认的ItemLoader加载item
        item_loader = ItemLoader(item=BiQuGeItem(), response=response)
        # xpath 获取方式
        item_loader.add_value('url_object_id', url_object_id)
        item_loader.add_css('title', '.bookname h1::text')
        # item_loader.add_xpath('title', '//*[@id="wrapper"]/div[4]/div/div[2]/h1/text()')
        item_loader.add_xpath('content', '//*[@id="content"]')

        article_item = item_loader.load_item()

        yield article_item


        # pass
