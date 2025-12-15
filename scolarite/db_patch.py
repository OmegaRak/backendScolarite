# db_patch.py
import pymysql
pymysql.install_as_MySQLdb()

# Patcher la version pour satisfaire Django
import sys
sys.modules['MySQLdb'] = pymysql
pymysql.__version__ = "2.2.7"
pymysql.version_info = (2, 2, 7, "final", 0)

# Désactiver la vérification de version de la base de données
from django.db.backends.base import base

def patched_check(self):
    pass  # Ne rien faire

base.BaseDatabaseWrapper.check_database_version_supported = patched_check

# Désactiver le support RETURNING pour MariaDB 10.4
from django.db.backends.mysql import features

class PatchedDatabaseFeatures(features.DatabaseFeatures):
    can_return_columns_from_insert = False
    can_return_rows_from_bulk_insert = False

features.DatabaseFeatures = PatchedDatabaseFeatures