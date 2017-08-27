# -*- coding: utf-8 -*-

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

# 'followall' is the name of one of the spiders of the project.
to_crawl = ['YunbiPriceSpider','JubiPriceSpider']

for spider in to_crawl:
    process.crawl(spider)
process.start() # the script will block here until the crawling is finished