# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']
    # start_urls = ['http://blog.jobbole.com/']

    def parse(self, response):
        # title = response.xpath('//*[@id="post-113681"]/div[1]/h1/text()')
        # create_time = response.xpath('//*[@id="post-113592"]/div[2]/p/text()').extract()[0].strip().replace('·', '')
        # praise_number = response.xpath('//*[@id="113592votetot al"]/text()').extract()[0]

        post_urls = response.css("#archive .floated-thumb .post-thumb a::attr(href)").extract()
        for post_url in post_urls:
            # yield Request("http://blog.jobbole.com/113684/", callback=self.parse_details)
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_details)

        next_urls = response.css(".next.page-numbers::attr(href)").extract_first("")
        yield Request(url=parse.urljoin(response.url, next_urls), callback=self.parse)
        pass

    # 提取文章详情
    def parse_details(self, response):
        title = response.xpath('//div[@class="entry-header"]/h1/text()')    # 标题
        create_time = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace('·', '')    # 创建时间
        praise_nums = response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()").extract()[0]    # 点赞数
        fav_nums = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract()[0]   # 分享数
        match_re = re.match(".*(\d+).*", fav_nums)
        if match_re:
            fav_nums = int(match_re.group(1))
        else:
            fav_nums = 0

        comment_nums = response.xpath("//a[@href='#article-comment']/span").extract()[0]    # 评论条数
        match_re = re.match(".*(\d+).*", comment_nums)
        if match_re:
            comment_nums = int(match_re.group(1))
        else:
            comment_nums = 0

        cotent = response.xpath("//div[@class='entry']").extract()[0]   # 文章内容
        tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()    # 文章tag
        tag_list = [element for element in tag_list if not element.strip().endswith('评论')]
        pass
