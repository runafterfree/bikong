# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from scrapy.conf import settings
from webcrawl.MYSQL import MYSQL
import json


class NoticeDbPipeLine(object):
    """将上线通知保存到数据库"""
    def __init__(self):
        self.mysql = MYSQL(host=settings['DATABASE']['host'],
                           user=settings['DATABASE']['user'],
                           pwd=settings['DATABASE']['password'],
                           db=settings['DATABASE']['db'],
                           char=settings['DATABASE']['charset'])

    def process_item(self, item, spider):
        data ={}
        data['title'] = item['title']
        data['site'] = item['site']
        data['link'] = item['link']
        data['update_time'] = item['update_time']
        print(data['title'], data['site'], data['update_time'], data['link'], item['body'])
        pass



class PriceDbPipeLine(object):
    """保存最新价格到数据库"""
    def __init__(self):
        self.mysql = MYSQL(host="127.0.0.1", user="root", pwd="123456", db="bikong")

    def process_item(self, item, spider):
        data ={}
        data['spec'] = item['spec']
        data['price'] = item['price']
        data['site_id'] = item['site_id']
        data['volumn'] = item['volumn']
        data['sales']  = item['sales']
        data['update_time'] = item['update_time']
        print(data['price'], data['volumn'], data['sales'], data['site'], data['update_time'])
        pass

class JsonWriterPipeline(object):
    """保存最新价格到文件中"""
    def open_spider(self, spider):
        self.file = open('jubi_price.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = item['spec']+',' + item['site_id']+','+str(item['price'])+"\n"
        self.file.write(line)
        return item