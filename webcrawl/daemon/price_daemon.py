# -*- coding: utf-8 -*-
from daemon import Daemon
from webcrawl import settings

class PriceDaemon(Daemon):
    '''生成价格通知'''

    def run(self):
        self.mysql = MYSQL(host=settings['DATABASE']['host'],
                           user=settings['DATABASE']['user'],
                           pwd=settings['DATABASE']['password'],
                           db=settings['DATABASE']['db'],
                           char=settings['DATABASE']['charset'])

        while True:
            rows = self.mysql.getAll("SELECT spec_id,price FROM b_price ORDER BY update_time DESC LIMIT 100")
            for row in rows:
                notifys = self.mysql.getAll("SELECT pid,uid,spec_id,note FROM b_price_notify WHERE "
                                            "(price<%s AND op=0 ) OR (price>%s AND op=1) AND spec_id=%s)"
                                            %(row['price'], row['spec_id']))
                for  n in notifys:
                    data = {'pid': n['pid'], 'msg': $n['note'] }
                    self.mysql.execInsert('b_queue', data)
        pass


    pass