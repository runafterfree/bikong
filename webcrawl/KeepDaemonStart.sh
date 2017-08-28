#/bin/sh
#保证通知进程一直激活状态
while true  
do  
  count=`ps -ef | grep "GetPrice.py" | grep -v "grep"`
  if [ "$?" != "0" ]; then  
     cd /var/www/html/bikong/webcrawl && python GetPrice.py 
  fi
  count=`ps -ef | grep "PriceNotify.py" | grep -v "grep"`
  if [ "$?" != "0" ]; then  
     cd /var/www/html/bikong/webcrawl/daemon && python PriceNotify.py 
  fi
  count=`ps -ef | grep "Queue.py" | grep -v "grep"`
  if [ "$?" != "0" ]; then  
     cd /var/www/html/bikong/webcrawl/daemon && python Queue.py
  fi
  sleep 5
done