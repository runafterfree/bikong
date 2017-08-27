#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import scrapy
from webcrawl.items_price import PriceItem
import time
import json

class JubiPriceSpider(scrapy.Spider):
    name = 'JubiPriceSpider'
    allowed_domains = ["jubi.com"]

    custom_settings = {
        'ITEM_PIPELINES':{
             'webcrawl.pipelines.PriceDbPipeLine': 300,
        },
    }

    #定义币种
    spec_used = {
        'act':'120',
        'xnc':'121',
        'eth':'122',
        'tic':'123',
        'qtum':'124',
        'bcc':'125',
        'xrp':'126',
        'ugt':'127',
        'ans':'128',
        'vtc':'129',
        'ltc':'130',
        'btm':'131',
        'blk':'132',
        'rss':'133',
        'hcc':'134',
        'elc':'135',
        'pgc':'136',
        'lsk':'137',
        'btc':'138',
        'btk':'139',
        'ico':'140',
        'etc':'141',
        'xas':'142',
        'bts':'143',
        'jbc':'144',
        'eos':'145',
        'zet':'146',
        'nxt':'147',
        'fz':'148',
        'doge':'149',
        'peb':'150',
        'xpm':'151',
        'mryc':'152',
        'dnc':'153',
        'max':'154',
        'vrc':'155',
        'qec':'156',
        'game':'157',
        'met':'158',
        'rio':'159',
        'zcc':'160',
        'ifc':'161',
        'mcc':'162',
        'tfc':'163',
        'plc':'164',
        'skt':'165',
        'ppc':'166',
        'lkc':'167',
        'ytc':'168',
        'xsgs':'169',
        'wdc':'170',
        'gooc':'171',
        'hlb':'172',
        'mtc':'173',
        'eac':'174',
        'ktc':'175',
    }

    site_id = '1'

    def __init__(self):
        pass

    def start_requests(self):
        url = 'https://www.jubi.com/coin/allcoin?t=%s' %(str(time.time()))
        return [scrapy.FormRequest(url)]

    def parse(self, response):
        try:
            data = json.loads(response.body)
            for d in data:
                if d in self.spec_used:
                    item = PriceItem()
                    item['spec_id'] = self.spec_used[d]
                    item['price'] = data[d][1]
                    item['volumn'] = data[d][6]
                    item['sales'] = data[d][7]
                    item['update_time'] = int(time.time())
                    item['site_id'] = self.site_id
                    #print(item)
                    yield item
        except:
            raise Exception('get json data failed : %s' %(response.body))
        time.sleep(5)
        url = 'https://www.jubi.com/coin/allcoin?t=%s' %(str(time.time()))
        yield scrapy.Request(url, callback=self.parse)