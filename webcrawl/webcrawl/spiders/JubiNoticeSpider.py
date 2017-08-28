#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import scrapy
from webcrawl.items_notice import NoticeItem
import time

class JubiNoticeSpider(scrapy.Spider):
    name = 'JubiNoticeSpider'
    allowed_domains = ["jubi.com"]
    start_urls = [
        'https://www.jubi.com/'
    ]
    custom_settings = {
        'ITEM_PIPELINES':{
            'webcrawl.pipelines.NoticeDbPipeLine': 300,
        },
    }
    site_id = '1'

    def __init__(self):
        pass

    def parse(self, response):
        for sel in response.xpath('//span[@class="jubi_news"]/ul/li'):
            try:
                item = NoticeItem()
                item['title'] = sel.xpath('a/text()')[0].extract()
                item['title'] = item['title'].replace('\xa0', '')
                if '查看更多' in item['title']:
                    continue
                if '上线' in item['title']:
                    item['is_online'] = '1'
                    item['step'] = '0'
                else:
                    item['is_online'] = '0'
                    item['step'] = '3'
                update_time = sel.xpath('a/span/text()')[0].extract()
                update_time = time.strftime('%Y', time.localtime(time.time()))+'-'+update_time[1:-1]
                item['update_time'] = int(time.mktime(time.strptime(update_time, '%Y-%m-%d')))
                item['site_id'] = self.site_id
                url = sel.xpath('a/@href')[0].extract()
                item['link'] = 'https://www.jubi.com'+url
                yield item
            except Exception as e:
                print(e)
            #yield scrapy.Request(link, callback=self.parse_article)

    def parse_article(self, response):
        item = NoticeItem()
        item['link'] = response.url
        item['title'] = response.xpath('//h1/text()')[0].extract()
        if '上线' in item['title']:
            item['is_online'] = '1'
        else:
            item['is_online'] = '0'
        item['site_id'] = self.site_id
        update_time = response.xpath('//span[@class="pub_date"]/text()')[0].extract()
        update_time = int(time.mktime(time.strptime(update_time, '%Y-%m-%d')))
        item['update_time'] = int(time.time())
        body = ''
        for sel in response.xpath('//div[@class="about_text"]/p/span'):
            body += sel.xpath('string(.)')[0].extract()+'<br />'
        item['body'] = body
        yield item
