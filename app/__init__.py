#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Файл инициализации приложения
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config.from_object(Config)  # Задание конфигурации приложения
# TODO: нет переключения в debug, возможно нужно сделать через Config
app.debug = True   # Флаг включения debug mode

login = LoginManager(app)
login.login_view = 'login'  # Указание какой route использовать при login
db = SQLAlchemy(app)
migrate = Migrate(app, db)
Bootstrap(app)

from app import routes, models

# Проверка заполненой таблицы, при первом запуске на новой машине
if not models.Role.query.all():
    admin = models.Role(user_role='admin')
    user = models.Role(user_role='user')
    db.session.add(admin)
    db.session.add(user)
    db.session.commit()
