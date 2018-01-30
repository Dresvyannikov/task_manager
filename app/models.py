#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from app import db
from app import login
from flask_login import UserMixin  # класс для работы с моделью пользователя использую при этом flask_login
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


class User(UserMixin, db.Model):
    """
    Модель описывает таблицу user.
    У таблицы есть связь OTM [one-to-many](один-ко-многим)с таблицей Task поле author
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    code = db.Column(db.String(32), unique=True)  # код подтверждения, нужен для востановления пароля

    tasks = db.relationship('Task', backref='author', lazy='dynamic')
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    # Пример отображения объектов для отладки
    def __repr__(self):
        return '<User {id} {name} {role} {email}>'.format(id=self.id, name=self.username, email=self.email,
                                                          role=self.priority.user_role)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)  # Функция переводит str в хэш-код пароля

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)  # Функция проверяет пароль сравнивая его с хэш-кодом


@login.user_loader
def load_user(id):  # Пользовательский загрузчик для указания объекта (класс Flask_login ничего не знает о БД)
    return User.query.get(int(id))


class Task(db.Model):
    """
    Модель описывает таблицу task.
    """
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(140))
    timestamp = db.Column(db.DATETIME, index=True, default=datetime.now)
    files = db.Column(db.String(320))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    mode_id = db.Column(db.Integer, db.ForeignKey('mode.id'))

    def __init__(self, comment=None):
        self.comment = comment

    # Пример отображения объектов для отладки
    def __repr__(self):
        return '<Task {id} {author} {mode} {files} {timestamp} {comment}>'.format(id=self.id, author=self.author,
                                                                                  mode=self.mode, files=self.files,
                                                                                  timestamp=self.timestamp,
                                                                                  comment=self.comment)


class Role(db.Model):
    """
    Модель описывает таблицу ролей, которая является справочной таблицей.
    У теблицы есть связь ОТО [one-to-one](один-к-одному) с таблицей User поле priority
    """
    id = db.Column(db.Integer, primary_key=True)
    user_role = db.Column(db.String(32), index=True, unique=True)  # уникальное(unique)

    user_id = db.relationship('User', backref='priority', uselist=False)

    # Пример отображения объектов для отладки
    def __repr__(self):
        return '<Role {}>'.format(self.user_role)


class Mode(db.Model):
    """
    Модель описывает таблицу режим, которая является справочной таблицей по доступным режимам.
    У теблицы есть связь ОТО [one-to-one](один-к-одному) с таблицей Task поле mode
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, unique=True)
    tasks = db.relationship('Task', backref='mode', lazy='dynamic')

    # Пример отображения объектов для отладки
    def __repr__(self):
        return '<Mode {}>'.format(self.name)
