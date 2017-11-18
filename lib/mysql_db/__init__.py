import pymysql

class mysql_db:
    def __init__(self, host='119.29.223.130', dbname='volunteer', user='liu', password='qq470401911', port='3306'):
        self.name='liu'
        self._host          = host
        self._dbuser        = user
        self._dbname        = dbname
        self._dbpassword    = password
        self._dbcharset     = 'utf8'
        self._dbport        = int(port)

        self._conn = self.getConnection()

    def getConnection(self):
        try:
            conn = pymysql.connect(self._host, self._dbuser, self._dbpassword, self._dbname,charset="utf8")
        except:
            conn = False
        return conn

    def select(self,filed = "*", table = '', more = ''):
        pass

    def close(self):
        self._conn.close()