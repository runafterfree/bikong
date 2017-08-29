# -*- coding: utf-8 -*-
from scrapy.utils.project import get_project_settings
from webcrawl.spiders.JubiNoticeSpider import JubiNoticeSpider
from webcrawl.spiders.YunBiNoticeSpider import YunBiNoticeSpider
import scrapydo
scrapydo.setup()
scrapydo.default_settings.update(get_project_settings())

def runcrawl():
    """
    Run a spider within Twisted. Once it completes,
    wait 5 seconds and run another spider.
    """
    try:
        scrapydo.run_spider(JubiNoticeSpider)
        scrapydo.run_spider(YunBiNoticeSpider)
    except Exception as e:
        print(e)

if __name__ == '__main__':
        runcrawl()
