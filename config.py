#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:

    CSRF_ENABLE = True  # Предотвращение поддельных межсайтовых запросов
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'may-the-force-be-with-you'  # Секретный ключ для модуля werkzeug
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')  # Путь к БД
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Флаг отключения функционала flask-sqlalchemy при изменении БД

    UPLOADED_PATH = os.getcwd() + '/upload'
    DROPZONE_MAX_FILES = 10
    DROPZONE_MAX_FILE_SIZE = 5
    DROPZONE_INPUT_NAME = 'file'
    DROPZONE_SERVE_LOCAL = True

    DROPZONE_DEFAULT_MESSAGE = "Перетащите файлы для задания"
    DROPZONE_INVALID_FILE_TYPE = "Вы не можете загружать такой формат файлов"
    DROPZONE_FILE_TOO_BIG = "Размер файла большой {{filesize}}. Допустимый максимальный размер: {{maxFilesize}}Мб."
    DROPZONE_BROWSER_UNSUPPORTED = "Выш браузер не поддерживает систему drag'n'drop, необходимо обновить"
    DROPZONE_MAX_FILE_EXCEED = "Вы не можете больше загружать файлы."
    DROPZONE_SERVER_ERROR = "Server error: {{statusCode}}"
    allowed_file_type = {
            'default': 'image/*, audio/*, video/*, text/*, application/*',
            'image': 'image/*',
            'audio': 'audio/*',
            'video': 'video/*',
            'text': 'text/*',
            'app': 'application/*'
        }
