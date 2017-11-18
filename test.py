import lib.curl as curl
#引入mysql库
from lib.mysql_db import mysql_db as mysql

db = mysql()
print(db._conn)