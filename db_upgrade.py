#!flask/bin/python
#
# нужен для обновления базы на на рабочем сервере
# (скрипт запускается посредством db_upgrade.py на сервере)
# (сам скрипт миграции создается посредством запуска db_migrate.py)
#
#  When you run this script, the database will be upgraded to the latest revision,
#  by applying the migration scripts stored in the database repository.
#
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO


api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('Current database version: ' + str(v))
