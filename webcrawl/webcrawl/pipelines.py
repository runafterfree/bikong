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
        #self.mysql = MYSQL(host="127.0.0.1", user="root", pwd="123456", db="bikong")
        self.mysql = MYSQL(host=settings['DATABASE']['host'],
                           user=settings['DATABASE']['user'],
                           pwd=settings['DATABASE']['password'],
                           db=settings['DATABASE']['db'],
                           char=settings['DATABASE']['charset'])

    def process_item(self, item, spider):
        data = dict(item)
        self.mysql.insert('b_price', data)
        self.mysql.executeNonQuery("UPDATE b_spec SET price='%s' WHERE spec_id=%s" %(data['price'], data['spec_id']))
        pass