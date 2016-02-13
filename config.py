import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

USER_NAMES = [
    {'name': 'andkns', 'password': 'andkns@gmail.com'},
    {'name': 'user1', 'password': 'user1@u.u'},
    {'name': 'user2', 'password': 'user2@u.u'}]
