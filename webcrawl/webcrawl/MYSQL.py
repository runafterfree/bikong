#coding=utf-8
#!/usr/bin/python
import pymysql

def addslashes(s):
    return s

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
        self.conn = pymysql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset=self.char)
        cur = self.conn.cursor()
        if not cur:
            raise Exception("连接数据库失败")
        else:
            return cur

    def GetRow(self,sql,param=None):
        """
        获得单条记录
        """
        cur = self.__GetConnect()
        cur.execute(sql)
        res = cur.fetchone()
        #查询完毕后必须关闭连接
        self.conn.close()
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
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()
        #查询完毕后必须关闭连接
        self.conn.close()
        return resList
    
    def execInsert(self, tablename, data):
        sql = 'INSERT INTO '+tablename+'('+','.join(data.keys())+') VALUES('
        for k,v in data.items():
            sql += "'"+addslashes(str(v))+"',"
        sql = sql[0:-1]+')'
        print(sql)
        cur = self.__GetConnect()
        try:
            cur.execute(sql)
            #cur.commit()
        except:
            raise Exception("执行语句 %s 失败: %s" % (sql,cur.Error))
        finally:
            self.conn.close()
        return cur.lastrowid

if __name__ == '__main__':
    mysql = MYSQL(host="127.0.0.1",user="root",pwd="123456",db="bikong")
    res = mysql.GetRow("select spec_name,spec_id FROM spec_yunbi")
    print(res)