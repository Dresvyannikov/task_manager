#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
from flask import request
from app import app
from app import db
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.models import User
from app.models import Role
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
    # хард код примера будущих задач
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]

    return render_template('index.html', title="Главная", posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Ошибка в имени пользователи или неверный пароль")
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        # обработка url с префиксом next
        next_page = request.args.get('next')
        # проверка нет ли перенаправлений на другие сайты (можно подставить)
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html',  title="Вход", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        if current_user.priority.user_role != 'admin':
            return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,
                    priority=Role.query.get(int(form.select_role.data)))
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Успешная регистрация пользователя")
        return redirect(url_for('index'))
    return render_template('register.html', title="Регистрация", form=form)

