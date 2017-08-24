#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import scrapy
from webcrawl.items_price import PriceItem
import time
import json

class JubiPriceSpider(scrapy.Spider):
    name = 'jubi_price'
    allowed_domains = ["jubi.com"]

    custom_settings = {
        'ITEM_PIPELINES':{
             'webcrawl.pipelines.JsonWriterPipeline': 300,
        },
    }

    def __init__(self):
        pass

    def start_requests(self):
        url = 'https://www.jubi.com/coin/allcoin?t=%s' %(str(time.time()))
        return [scrapy.FormRequest(url)]

    def parse(self, response):
        try:
            data = json.loads(response.body)
            for d in data:
                item = PriceItem()
                item['price'] = data[d][1]
                item['spec'] = d
                item['volumn'] = data[d][6]
                item['sales'] = data[d][7]
                item['update_time'] = int(time.time())
                item['site_id'] = '1'
                yield item
        except:
            raise Exception('get json data failed : %s' %(response.body))