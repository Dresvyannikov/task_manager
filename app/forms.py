#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import BooleanField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms.validators import DataRequired

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class LoginForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Passwd', validators=[DataRequired()])
    remember_me = BooleanField('Remember me', default=False)
    submit = SubmitField('Sign in')
