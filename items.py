# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field()  # 标题
    create_time = scrapy.Field()    # 文章创建时间
    url = scrapy.Field()    # 访问的url
    url_object_id = scrapy.Field()    # MD5url
    front_image_url = scrapy.Field()    # 封面图
    front_image_path = scrapy.Field()    # 路径
    praise_nums = scrapy.Field()    # 点赞数
    fav_nums = scrapy.Field()    # 分享数
    comment_nums = scrapy.Field()    # 评论数
    tags = scrapy.Field()    # tag
    content = scrapy.Field()    # 内容


class BiQuGeListItem(scrapy.Item):
    title = scrapy.Field()  # 标题
    author = scrapy.Field()  # 作者
    last_update_time = scrapy.Field()  # 最后更新时间
    front_image_url = scrapy.Field()  # 封面图
    front_image_path = scrapy.Field()  # 路径
