# -*- coding: utf-8 -*-
#from daemon import Daemon
from MYSQL import MYSQL
import sys, time
from daemon import Daemon

class PriceDaemon(Daemon):
    '''生成价格通知'''

    def _run(self):
        #mysql = MYSQL(host="127.0.0.1", user="root", pwd="123456", db="bikong")
        mysql = self.mysql

        while True:
            try:
                rows = mysql.getAll("SELECT n.pid,n.note,n.uid,n.tel,n.email FROM b_spec s,b_price_notify n WHERE s.active=1 AND n.spec_id=s.spec_id"
                                    + " AND ((n.op=0 AND s.price>n.price) OR (n.op=1 AND s.price<n.price)) AND n.step=0")
                for row in rows:
                    pid, msg, uid, tel, email = row
                    data = {'pid': pid, 'msg': msg, 'uid': uid, 'tel': tel, 'email': email}
                    mysql.insert('b_queue', data)
                    mysql.executeNonQuery("UPDATE b_price_notify SET step=2 WHERE pid='%s'" %(pid) )
            except Exception as e:
                sys.stderr.write(str(e))
            time.sleep(5)
        pass
    pass


if __name__ == '__main__':
    daemon = PriceDaemon('/tmp/price_process.pid', stdout='/tmp/price_stdout.log')
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