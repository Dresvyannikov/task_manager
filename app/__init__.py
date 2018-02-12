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
from flask_dropzone import Dropzone
from flask_mail import Mail


app = Flask(__name__)
app.config.from_object(Config)  # Задание конфигурации приложения

login = LoginManager(app)
login.login_view = 'login'  # Указание какой route использовать при login
db = SQLAlchemy(app)

if app.app_context():
    migrate = Migrate(app, db, render_as_batch=True)
else:
    migrate = Migrate(app, db)

Bootstrap(app)

dropzone = Dropzone(app)

mail = Mail(app)

from app import routes, models, errors


# Проверка заполненой таблицы, при первом запуске на новой машине
try:
    if not models.Role.query.all():
        admin = models.Role(user_role='admin')
        user = models.Role(user_role='user')
        db.session.add(admin)
        db.session.add(user)
        db.session.commit()

except:
    print('Таблицы Role не существует!')


try:
    if not models.Mode.query.all():
        ksh = models.Mode(name="КШ")
        ou = models.Mode(name="ОУ")
        db.session.add(ksh)
        db.session.add(ou)
        db.session.commit()
except:
    print('Таблицы Mode не существует!')
