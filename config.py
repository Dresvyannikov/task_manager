#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    CSRF_ENABLE = True  # Предотвращение поддельных межсайтовых запросов
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'may-the-force-be-with-you'  # Секретный ключ для модуля werkzeug
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')  # Путь к БД
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Флаг отключения функционала flask-sqlalchemy при изменении БД

