import pymysql
from . import db_patch

pymysql.install_as_MySQLdb()
