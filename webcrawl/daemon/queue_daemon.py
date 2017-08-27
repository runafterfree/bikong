# -*- coding: utf-8 -*-
from daemon import Daemon
from MYSQL import MYSQL
import time, sys
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from yunpian_python_sdk.model import constant as YC
from yunpian_python_sdk.ypclient import YunpianClient


class QueueDaemon(Daemon):
    '''处理消息队列'''

    def run(self):
        #mysql = MYSQL(host="127.0.0.1", user="root", pwd="123456", db="bikong")
        mysql = self.mysql
        self.clnt = YunpianClient('304ab9c0aa24a69869052441f9afbe08')

        while True:
            try:
                rows = mysql.getAll("SELECT queue_id,msg, uid, tel, email FROM b_queue LIMIT 10")
                for row in rows:
                    queue_id, msg, uid, tel, email = row
                    r = self.sendtel_yunpian(tel, msg)
                    if r:
                        data = {'uid':uid, 'message': msg, 'send_time': int(time.time())}
                        mysql.insert('b_price_notify_log', data)
                        mysql.executeNonQuery("DELETE FROM b_queue WHERE queue_id=%s" % queue_id)
            except Exception as e:
                sys.stderr.write(str(e))
            time.sleep(5)
        pass

    def sendemail(self, email, msg):
        # 第三方 SMTP 服务
        mail_host = "smtp.163.com"  # 设置服务器
        mail_user = "cy_024@163.com"  # 用户名
        mail_pass = "cy110120"  # 口令

        sender = 'cy_024@163.com'
        receivers = ['createday@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

        message = MIMEText(msg, 'html', 'utf-8')
        message['From'] = sender
        message['To'] = ",".join(receivers)

        subject = '价格变动通知'
        message['Subject'] = subject

        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(sender, receivers, message.as_string())
            smtpObj.close()
            return True
        except Exception as e:
            sys.stderr.write(str(e))
            return False

    def sendtel_yunpian(self, tel, msg):
        '''使用yunpian.com的短信接口发送短信'''

        param = {YC.MOBILE: tel, YC.TEXT: '【币控网】'+msg+'来自bikongwang.com！'}
        r = self.clnt.sms().single_send(param)
        if r.code():
            sys.stderr.write(str(r.code())+':'+r.msg())
            return False
        return True


    pass

if __name__ == '__main__':
    daemon = QueueDaemon('/tmp/queue_process.pid', stdout='/tmp/queue_stdout.log')
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