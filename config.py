#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class Config():
    CSRF_ENABLE = True  # Предотвращение поддельных межсайтовых запросов
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'may-the-force-be-with-you'
