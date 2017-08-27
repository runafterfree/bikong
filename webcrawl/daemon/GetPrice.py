# -*- coding: utf-8 -*-
#from daemon import Daemon
import sys, time
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class GetPriceDaemon():
    '''获得价格'''

    def run(self):
        while True:
            process = CrawlerProcess(get_project_settings())

            # 'followall' is the name of one of the spiders of the project.
            to_crawl = ['YunbiPriceSpider', 'JubiPriceSpider']

            for spider in to_crawl:
                process.crawl(spider)
            process.start()  # the script will block here until the crawling is finished
            time.sleep(5)
        pass
    pass


if __name__ == '__main__':
    daemon = GetPriceDaemon()
    daemon.run()