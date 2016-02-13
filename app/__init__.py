from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)       # создаем объект приложения (наследую Flask)
app.config.from_object('config')  # настройки нужны расширению Flask-WTF

db = SQLAlchemy(app)


import os
from flask_login import LoginManager
from config import basedir


lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'


from app import views, models       # из /mysite/app файл views.py models.py

