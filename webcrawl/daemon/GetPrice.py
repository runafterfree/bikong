# -*- coding: utf-8 -*-
#from daemon import Daemon
import sys, time
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class GetPriceDaemon():
    '''获得价格'''

    def run(self):
        process = CrawlerProcess(get_project_settings())
        to_crawl = ['YunbiPriceSpider', 'JubiPriceSpider']
        while True:
            for spider in to_crawl:
                process.crawl(spider)
            process.start()  # the script will block here until the crawling is finished
            process.stop()
            time.sleep(5)


if __name__ == '__main__':
    daemon = GetPriceDaemon()
    daemon.run()