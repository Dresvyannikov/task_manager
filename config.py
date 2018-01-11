#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os


class Config():
    CSRF_ENABLE = True  # Предотвращение поддельных межсайтовых запросов
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'may-the-force-be-with-you'
