# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings
from webcrawl.MYSQL import MYSQL
import json


class NoticeDbPipeLine(object):
    """将上线通知保存到数据库"""
    def __init__(self):
        settings = get_project_settings()
        self.mysql = MYSQL(host=settings['DATABASE']['host'],
                           user=settings['DATABASE']['user'],
                           pwd=settings['DATABASE']['password'],
                           db=settings['DATABASE']['db'],
                           char=settings['DATABASE']['charset'])

    def process_item(self, item, spider):
        data = dict(item)
        sql = "SELECT COUNT(*) FROM b_notice WHERE site_id=%s AND title=%s"
        row = self.mysql.getRow(sql, (data['site_id'], data['title']))
        if not row[0]:
            self.mysql.insert('b_notice',data)
        #print(data['title'], data['site_id'], data['update_time'], data['link'], item['is_online'])
        pass



class PriceDbPipeLine(object):
    """保存最新价格到数据库"""
    def __init__(self):
        settings = get_project_settings()
        self.mysql = MYSQL(host=settings['DATABASE']['host'],
                           user=settings['DATABASE']['user'],
                           pwd=settings['DATABASE']['password'],
                           db=settings['DATABASE']['db'],
                           char=settings['DATABASE']['charset'])

    def process_item(self, item, spider):
        data = dict(item)
        #self.mysql.insert('b_price', data)
        self.mysql.executeNonQuery("UPDATE b_spec SET price='%s' WHERE spec_id=%s" %(data['price'], data['spec_id']))
        pass