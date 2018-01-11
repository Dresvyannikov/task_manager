#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField(u'Имя пользователя', validators=[DataRequired()])
    password = PasswordField(u'Пароль', validators=[DataRequired()])
    remember_me = BooleanField(u'Запомнить меня')
    submit = SubmitField(u'Войти')
