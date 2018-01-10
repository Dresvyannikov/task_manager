#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from app import app
from flask import request
from flask import redirect
from flask import flash
from flask import url_for
from flask import render_template
from forms import LoginForm

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

@app.route('/')
@app.route('/index')
def index():
    args = {'title': 'main'}
    return render_template('index.html', args=args)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # flash('{mes}'.format(mes=u'Успешный вход'))
        print(form.username.label)
        return redirect(url_for('index'))
    args = {'title': 'auth'}
    return render_template('login.html', args=args, form=form)
