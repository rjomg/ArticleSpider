# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import datetime
import scrapy
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.loader.processors import TakeFirst
from scrapy.loader.processors import Join


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def add_jobbole(value):
    return value+"-123"


#   获取时间
def create_convert(value):
    try:
        create_time = datetime.datetime.strptime(value, "%Y/%m/%d")
    except Exception as e:
        create_time = datetime.datetime.now()

    return create_time


#   获取数值
def get_nums(value):
    match_re = re.match(".*(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums


#   去掉tag中提取的评论
def remove_comment_tags(value):
    #   去掉tag中提取的评论
    if "评论" in value:
        return ""
    else:
        return value


def return_value(value):
    return value


class ArticleItemLoader(ItemLoader):
    # 自定义ItemLoader
    default_output_processor = TakeFirst()


#   伯乐在线
class JobBoleArticleItem(scrapy.Item):
    # MD5url
    url_object_id = scrapy.Field()
    title = scrapy.Field()  # 标题
    create_time = scrapy.Field(
        input_processor=MapCompose(create_convert),
    )    # 文章创建时间
    url = scrapy.Field()    # 访问的url
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value),
    )    # 封面图
    front_image_path = scrapy.Field()    # 路径
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums),
    )    # 点赞数
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums),
    )    # 分享数
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums),
    )    # 评论数
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(','),
    )    # tag
    content = scrapy.Field()    # 内容


# 笔趣阁列表
class BiQuGeListItem(scrapy.Item):
    url_object_id = scrapy.Field()  # MD5url
    title = scrapy.Field()  # 标题
    author = scrapy.Field()  # 作者
    last_update_time = scrapy.Field()  # 最后更新时间
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value),
    )  # 封面图
    front_image_path = scrapy.Field()  # 路径


# 笔趣阁详情
class BiQuGeItem(scrapy.Item):
    url_object_id = scrapy.Field()  # MD5url
    title = scrapy.Field()  # 标题
    content = scrapy.Field()  # 内容
