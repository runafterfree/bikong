# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import scrapy.settings
from webcrawl.MYSQL import MYSQL

class NoticeDbPipeLine(object):
    """将上线通知保存到数据库"""
    def __init__(self):
        self.mysql = MYSQL(host="127.0.0.1", user="root", pwd="123456", db="bikong")

    def process_item(self, item, spider):
        data ={}
        data['title'] = item['title']
        data['site'] = item['site']
        data['link'] = item['link']
        data['update_time'] = item['update_time']
        print(data['title'],data['site'],data['update_time'],data['link'],item['body'])
        pass



class WebcrawlPipeline(object):
    def process_item(self, item, spider):
        return item
