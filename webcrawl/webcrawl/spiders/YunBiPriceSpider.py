#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import scrapy
from webcrawl.items_price import PriceItem
import json

class YunbiPriceSpider(scrapy.Spider):
    name = 'YunbiPriceSpider'
    allowed_domains = ["yunbi.com"]
    start_urls = [
        'https://yunbi.com/api/v2/tickers.json'
    ]
    custom_settings = {
        'ITEM_PIPELINES':{
             'webcrawl.pipelines.PriceDbPipeLine': 300,
        },
    }

    #定义币种
    spec_used = {
        'btc': '176',
        'etc': '177',
        'pay': '178',
        'gnt': '179',
        'zmc': '180',
        'snt': '181',
        'omg': '182',
        'ans': '183',
        'lun': '184',
        'zec': '185',
        'ven': '186',
        '1st': '187',
        'bts': '188',
        'eos': '189',
        'eth': '190',
        'sc': '191',
        'rep': '192',
        'qtum': '193',
        'gxs': '194',
        'bcc': '195',
        'dgd': '196',
    }

    site_id = '2'

    '''
    def start_requests(self):
        url = 'https://yunbi.com/api/v2/tickers.json?t=%s' %(str(time.time()))
        return [scrapy.FormRequest(url)]
    '''
    def parse(self, response):
        try:
            data = json.loads(response.body)
            for d in data:
                v = d.replace('cny','')
                if v in self.spec_used:
                    item = PriceItem()
                    item['spec_id'] = self.spec_used[v]
                    item['price'] = data[d]['ticker']['last']
                    item['volumn'] = data[d]['ticker']['vol']
                    item['sales'] = 0
                    item['update_time'] = data[d]['at']
                    item['site_id'] = self.site_id
                    #print(item)
                    yield item
        except Exception as e:
            raise Exception(e)