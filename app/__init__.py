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
import click


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


from app import routes, models, errors, rest


@app.cli.command()
def initdb():
    click.echo('Init the db')
    db.create_all()

    try:
        if not models.Role.query.all():
            admin = models.Role(user_role='admin')
            user = models.Role(user_role='user')
            remote = models.Role(user_role='remote')
            db.session.add_all([admin, user, remote])
            db.session.commit()
    except:
        click.echo('Таблицы Role не существует!')

    try:
        if not models.User.query.all():
            user = models.User(username='admin', email="test@mail.ru",
                               priority=models.Role.query.filter_by(user_role='admin').first())
            user.set_password('5198')
            db.session.add(user)
            db.session.commit()
    except:
        click.echo('Таблицы User не существует!')

    try:
        if not models.Mode.query.all():
            ksh = models.Mode(name="КШ")
            ou = models.Mode(name="ОУ")
            db.session.add(ksh)
            db.session.add(ou)
            db.session.commit()
    except:
        click.echo('Таблицы Mode не существует!')

    try:
        if not models.State.query.all():
            done = models.State(name="done", name_rus="Выполнено")
            loaded = models.State(name="loaded", name_rus="В процессе")
            queue = models.State(name="queue", name_rus="В очереди")
            error = models.State(name="error", name_rus="Ошибка")
            db.session.add_all([done, loaded, queue, error])
            db.session.commit()
    except:
        click.echo('Таблицы State не существует!')

    try:
        if not models.Position.query.all():
            position = models.Position(name='арм-р')
            position2 = models.Position(name='коап')
            db.session.add(position)
            db.session.add(position2)
            db.session.commit()
    except:
        click.echo('Таблицы Position не существует!')