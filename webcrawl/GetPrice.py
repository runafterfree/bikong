# -*- coding: utf-8 -*-
from scrapy.utils.project import get_project_settings
from webcrawl.spiders.JubiPriceSpider import JubiPriceSpider
from webcrawl.spiders.YunBiPriceSpider import YunbiPriceSpider
import scrapydo
import time

scrapydo.setup()
scrapydo.default_settings.update(get_project_settings())
def runcrawl():
    """
    Run a spider within Twisted. Once it completes,
    wait 5 seconds and run another spider.
    """
    try:
        scrapydo.run_spider(JubiPriceSpider)
        scrapydo.run_spider(YunbiPriceSpider)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    while True:
        runcrawl()
        time.sleep(5)