# -*- coding: utf-8 -*-
#from daemon import Daemon
import sys, time
from daemon import Daemon
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class GetPriceDaemon(Daemon):
    '''获得价格'''

    def _run(self):
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
    daemon = GetPriceDaemon('/tmp/getprice_process.pid', stdout='/tmp/getprice_stdout.log')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print
            'unknown command'
            sys.exit(2)
        sys.exit(0)
    else:
        print
        'usage: %s start|stop|restart' % sys.argv[0]
        sys.exit(2)