# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PriceItem(scrapy.Item):
    price = scrapy.Field()
    update_time = scrapy.Field()
    volumn = scrapy.Field()
    sales = scrapy.Field()
    site_id = scrapy.Field()
    spec = scrapy.Field()
