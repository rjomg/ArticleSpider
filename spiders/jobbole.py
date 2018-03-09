# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import JobBoleArticleItem
from ArticleSpider.utils.common import get_md5

import codecs
import json



class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']
    # start_urls = ['http://blog.jobbole.com/']

    def parse(self, response):
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url}, callback=self.parse_details)

        next_urls = response.css(".next.page-numbers::attr(href)").extract_first("")
        yield Request(url=parse.urljoin(response.url, next_urls), callback=self.parse)
        pass

    # 提取文章详情
    def parse_details(self, response):
        article_item = JobBoleArticleItem()

        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first("")    # 标题
        create_time = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace('·', '')    # 创建时间
        praise_nums = response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()").extract()[0]    # 点赞数
        fav_nums = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract()[0]   # 分享数
        front_image_url = response.meta.get("front_image_url", '')  # 文章封面图
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

        content = response.xpath("//div[@class='entry']").extract()[0]   # 文章内容
        tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()    # 文章tag
        tag_list = [element for element in tag_list if not element.strip().endswith('评论')]
        tags = ",".join(tag_list)

        article_item['url_object_id'] = get_md5(response.url)
        article_item['title'] = title
        article_item['url'] = response.url
        article_item['create_time'] = create_time
        article_item['front_image_url'] = [front_image_url]
        article_item['praise_nums'] = praise_nums
        article_item['fav_nums'] = fav_nums
        article_item['comment_nums'] = comment_nums
        article_item['tags'] = tags
        article_item['content'] = content

        yield article_item
