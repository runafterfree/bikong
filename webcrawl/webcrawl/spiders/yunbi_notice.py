#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import scrapy
from webcrawl.items_notice import NoticeItem
import time

class JubiNoticeSpider(scrapy.Spider):
    name = 'yunbi_notice'
    allowed_domains = ["yunbi.com"]
    start_urls = [
        'https://yunbi.com/?warning=false&lang=zh-CN'
    ]
    custom_settings = {
        'ITEM_PIPELINES':{
            'webcrawl.pipelines.NoticeDbPipeLine': 300,
        },
    }

    def __init__(self):
        pass

    def parse(self, response):
        #print(response.body)
        for sel in response.xpath('//div[@class="ui relaxed aligned link list"]/div[@class="item "]'):
            title = sel.xpath('a').xpath('string(.)')[0].extract()
            if '上线' in title:
                url = sel.xpath('a/@href')[0].extract()
                update_time = sel.xpath('div[class="right floated content"]').xpath('string(.)')[0].extract()
                #update_time = time.strftime('%Y',time.localtime(time.time())) + update_time
                print(update_time)
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
