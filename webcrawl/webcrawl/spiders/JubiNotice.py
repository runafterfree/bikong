#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import scrapy
from webcrawl.items import NoticeItem
import time

class JubiNoticeSpider(scrapy.Spider):
    name = 'jubi_notice'
    allowed_domains = ["jubi.com"]
    start_urls = [
        'https://www.jubi.com/'
    ]

    def __init__(self):
        pass

    def parse(self, response):
        for sel in response.xpath('//span[@class="jubi_news"]/ul/li'):
            title = sel.xpath('a/text()')[0].extract()
            if '上线' in title:
                url = sel.xpath('a/@href')[0].extract()
                link = 'https://www.jubi.com'+url
                # item = NoticeItem()
                # item['title'] = title
                #item['link'] = link
                #item['site'] = "jubi"
                #update_time = sel.xpath('a/span/text()')[0].extract()
                #item['update_time'] = update_time[1:-1]
                #item['update_time'] = time.mktime(update_time)
                #print(item['title'],item['link'],item['update_time'])
                #yield item

                yield scrapy.Request(link, callback=self.parse_article)

    def parse_article(self, response):
        item = NoticeItem()
        item['link'] = response.url
        item['title'] = response.xpath('//h1/text()')[0].extract()
        item['site'] = 'jubi'
        item['update_time'] = int(time.time())
        item['body'] = "1"
        #for p in response.xpath('//div[@class="about_text"]/p'):
        #    body = body+p.xpath('text()')[0].extract()
        #item['body'] = body
        #print(item['title'], item['link'], item['update_time'])
        yield item
