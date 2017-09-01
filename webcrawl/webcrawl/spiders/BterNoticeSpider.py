#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import scrapy
from webcrawl.items_notice import NoticeItem
import time,sys

class BterNoticeSpider(scrapy.Spider):
    name = 'BterNoticeSpider'
    allowed_domains = ["bter.com"]
    start_urls = [
        'https://bter.com/lang/cn'
    ]
    custom_settings = {
        'ITEM_PIPELINES':{
            'webcrawl.pipelines.NoticeDbPipeLine': 300,
        },
    }
    site_id = '3'

    def __init__(self):
        pass

    def parse(self, response):
        #print(response.body)
        for sel in response.xpath('//div[@class="right_con clearfix"]/div[1]/div[@class="right_content bul"]/ul/li'):
            try:
                item = NoticeItem()
                item['title'] = sel.xpath('a/text()')[0].extract()
                item['link'] = 'https://bter.com' + sel.xpath('a/@href')[0].extract()
                if '上线' in item['title']:
                    item['is_online'] = '1'
                    item['step'] = '0'
                else:
                    item['is_online'] = '0'
                    item['step'] = '3'
                item['site_id'] = self.site_id
                yield scrapy.Request(item['link'], callback=self.parse_article, meta={'item':item})
                #print(item['title'],item['link'])
            except Exception as e:
                print(e)

    def parse_article(self, response):
        item = response.meta['item']
        update_time = response.xpath('//div[@class="new-dtl-info"]/span[1]/text()')[0].extract()
        item['update_time'] = int(time.mktime(time.strptime(update_time, '%Y-%m-%d %H:%M:%S')))
        yield item