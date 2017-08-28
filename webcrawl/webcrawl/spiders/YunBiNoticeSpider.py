#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import scrapy
from webcrawl.items_notice import NoticeItem
import time

class YunBiNoticeSpider(scrapy.Spider):
    name = 'YunbiNoticeSpider'
    allowed_domains = ["yunbi.com"]
    start_urls = [
        'https://yunbi.com/?warning=false&lang=zh-CN'
    ]
    custom_settings = {
        'ITEM_PIPELINES':{
            'webcrawl.pipelines.NoticeDbPipeLine': 300,
        },
    }
    site_id = '2'

    def __init__(self):
        pass

    def parse(self, response):
        for sel in response.xpath('//div[@class="ui relaxed aligned link list"]/div[@class="item "]'):
            try:
                title = sel.xpath('a').xpath('string(.)')[0].extract()
                title = title.replace('\x0a', '')
                title = title.replace(' ', '')
                item = NoticeItem()
                item['title'] = title
                if '上线' in title:
                    item['is_online'] = '1'
                    item['step'] = '0'
                else:
                    item['is_online'] = '0'
                    item['step'] = '3'
                url = sel.xpath('a/@href')[0].extract()
                item['link'] = url
                item['site_id'] = self.site_id
                update_time = sel.xpath('div/i/text()')[0].extract()
                update_time = time.strftime('%Y', time.localtime(time.time())) + '-' + update_time
                item['update_time'] = int(time.mktime(time.strptime(update_time, '%Y-%m-%d %H:%M')))
                yield item
            except Exception as e:
                print(e)

            #yield scrapy.Request(url, callback=self.parse_article)

    def parse_article(self, response):
        item = NoticeItem()
        item['link'] = response.url
        item['title'] = response.xpath('//h1/text()')[0].extract()
        item['site'] = 'jubi'
        item['update_time'] = int(time.time())
        body = ''
        for sel in response.xpath('//div[@class="about_text"]/p/span'):
            body += sel.xpath('string(.)')[0].extract()+'<br />'
        item['body'] = body
        yield item
