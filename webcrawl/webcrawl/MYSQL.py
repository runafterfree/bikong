#coding=utf-8
#!/usr/bin/python
import pymysql

def addslashes(v):
    return v

class MYSQL:
    """
    对pymysql的简单封装
    """
    def __init__(self,host,user,pwd,db,char="utf8"):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.char=char

    def __GetConnect(self):
        """
        得到连接信息
        返回: conn.cursor()
        """
        if not self.db:
            raise Exception("没有设置数据库信息")
        try:
            conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.pwd,
                database=self.db,
                charset=self.char
            )
        except:
            raise Exception("数据库连接失败")
        if not conn:
            return None
        return conn

    def GetRow(self,sql,param=None):
        """
        获得单条记录
        """
        try:
            conn = self.__GetConnect()
            with conn.cursor() as cur:
                cur.execute(sql,param)
                res = cur.fetchone()
        except:
            raise Exception("查询数据失败：%s" % sql)
        finally:
            conn.close()
        return res


    def GetAll(self,sql,param=None):
        """
        执行查询语句
        返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段
        调用示例：
                ms = MYSQL(host="localhost",user="sa",pwd="123456",db="PythonWeiboStatistics")
                resList = ms.ExecQuery("SELECT id,NickName FROM WeiBoUser")
                for (id,NickName) in resList:
                    print str(id),NickName
        """
        try:
            conn = self.__GetConnect()
            with conn.cursor() as cur:
                cur.execute(sql,param)
                res = cur.fetchall()
        except:
            raise Exception("查询数据失败：%s" % sql)
        finally:
            conn.close()
        return res

    def insert(self, table, data):
        conn = self.__GetConnect()
        try:
            sql = "INSERT INTO " + table + "(" + ",".join(data.keys()) + ") VALUES(";
            for k in data:
                sql += "'" + addslashes(data[k]) + "',"
            sql = sql[0:-1] + ")";

            with conn.cursor() as cur:
                cur.execute(sql)
                conn.commit()
                lastid = cur.lastrowid
        except:
            conn.rollback()
            raise Exception("运行语句失败:%s" %(sql))
        finally:
            conn.close()
        if not lastid:
            return None
        return lastid

    def update(self, table, data, where):
        conn = self.__GetConnect()
        try:
            sql = "UPDATE " + table + " SET ";
            for k in data:
                sql += str(k) + "='" + addslashes(str(data[k])) + "',"
            sql = sql[0:-1]+ ' where '+where
            with conn.cursor() as cur:
                cur.execute(sql)
                conn.commit()
                rowcount = cur.rowcount
        except:
            conn.rollback()
            raise Exception("运行语句失败:%s" %(sql))
        finally:
            conn.close()
        return rowcount

if __name__ == '__main__':
    mysql = MYSQL(host="127.0.0.1",user="root",pwd="123456",db="bikong")
    res = mysql.insert('b_site',{'site_enname':'yunbi','site_name':'云币网','site_url':'https://yunbi.com'})
    print(res)