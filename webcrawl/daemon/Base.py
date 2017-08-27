# -*- coding: utf-8 -*-
from webcrawl.MYSQL import MYSQL
from scrapy.utils.project import get_project_settings

class Base():
    def __init__(self):
        settings = get_project_settings()
        self.mysql = MYSQL(host=settings['DATABASE']['host'],
                           user=settings['DATABASE']['user'],
                           pwd=settings['DATABASE']['password'],
                           db=settings['DATABASE']['db'],
                           char=settings['DATABASE']['charset'])