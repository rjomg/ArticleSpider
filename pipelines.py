# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import MySQLdb
import MySQLdb.cursors
import pymongo

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi  # mysql异步


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    # 自定义文件导出
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding="utf8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


class MysqlPipeline(object):
    # mysql 爬虫同步执行 容易造成mysql 堵塞
    def __init__(self):
        self.conn = MySQLdb.connect('120.78.208.86', 'root', 'root', 'article-spider', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into jobbole_article(title, create_time, url, fav_nums)
            VALUE (%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql, (item["title"], item["create_time"], item["url"], item["fav_nums"]))
        self.conn.commit()

# mysql异步执行
class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        #  使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item, spider)
        query.addErrback(self.handler_error, item, spider) # 处理异常
        return item

    def handler_error(self, failure, item, spider):
        #   处理异步插入的异常
        print(failure)


    def do_insert(self, cursor, item, spider):
        if spider.name == 'jobbole':
            #   执行具体的插入
            insert_sql = """
                        insert into jobbole_article(url_object_id, title, url, front_image_url, front_image_path, comment_nums, fav_nums, praise_nums, tags, content, create_time)
                        VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """
            cursor.execute(insert_sql, (item["url_object_id"], item["title"], item["url"], item["front_image_url"], item["front_image_path"], item["comment_nums"], item["fav_nums"], item["praise_nums"], item["tags"], item["content"], item["create_time"]))

        if spider.name == 'biquge':
                #   执行具体的插入
                insert_sql = """
                            insert into biquge_novel(url_object_id, title, author, front_image_url, front_image_path, last_update_time)
                            VALUE (%s,%s,%s,%s,%s,%s)
                            """
                cursor.execute(insert_sql, (item["url_object_id"], item["title"], item["author"], item["front_image_url"], item["front_image_path"], item["last_update_time"]))

class MongoPipeline(object):
    def __init__(self):
        self.conn = pymongo.MongoClient('120.78.208.86', 27017)
        self.db = self.conn.article_spider  # 连接mydb数据库，没有则自动创建


    def process_item(self, item, spider):
        if spider.name == 'jobbole':
            self.jobbole_article = self.db.jobbole_article  # 使用jobbole_article集合，没有则自动创建
            self.jobbole_article.insert({"name": item['title'], "create_time": item['create_time'], "url": item['url'],
                                         "fav_nums": item['fav_nums']})
        if spider.name == 'biquge':
            self.biquge_article = self.db.biquge_article  # 使用biquge_article集合，没有则自动创建
            self.biquge_article.insert({"name": item['title'], "author": item['author']})


class BiqugeMongoPipeline(object):
    def __init__(self):
        self.conn = pymongo.MongoClient('120.78.208.86', 27017)
        self.db = self.conn.article_spider  # 连接mydb数据库，没有则自动创建

    def process_item(self, item, spider):
        if spider.name == 'biquge':
            if item['content'] != '':
                self.biquge_article = self.db.biquge_article  # 使用biquge_article集合，没有则自动创建
                self.biquge_article.insert({"url_object_id": item['url_object_id'], "name": item['title'], "content": item['content']})



class JsonExporterPipeline(object):
    # 调用
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            for ok, value in results:
                image_file_path = value["path"]
            item['front_image_path'] = image_file_path

        return item
