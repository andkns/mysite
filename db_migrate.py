#!flask/bin/python
#
# файл миграции - запускается на компе разработчика для создания скрипта
# который впоследствии будет нужен для обновления базы на на рабочем сервере
# (скрипт запускается посредством db_upgrade.py на сервере)
#
# when you are ready to release the new version of the app to your production server you just need
# to record a new migration, copy the migration scripts to your production server and
# run a simple script that applies the changes for you
#
# This script will downgrade the database one revision.
# You can run it multiple times to downgrade several revisions.
#

import types
from migrate.versioning import api
from app import db
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO

v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)

migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v+1))


tmp_module = types.ModuleType('old_model')

old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
a = tmp_module.__dict__

exec(old_model, tmp_module.__dict__)

script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)

open(migration, "wt").write(script)
api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('New migration saved as ' + migration)
print('Current database version: ' + str(v))