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
from app.forms import TaskForm
from app.forms import EditProfileForm
from app.models import User
from app.models import Role
from app.models import Task
from app.models import Mode
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from werkzeug.urls import url_parse
import os
from datetime import datetime
import shutil


@app.route('/')
@app.route('/index')
# @login_required
def index():
    # хард код примера будущих задач
    tasks = Task.query.all()

    return render_template('index.html', title="Главная", tasks=tasks)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Ошибка в имени пользователя или неверный пароль")
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
@login_required
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


@app.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    path_upload = os.path.join(app.config['UPLOADED_PATH'], "new_task")

    # загрузка файлов из dropzone
    if request.method == 'POST':
        files = request.files
        for key, file in files.items():
            # проверка существования каталога
            if not os.path.isdir(path_upload):
                os.makedirs(path_upload)
            file.save(os.path.join(path_upload, file.filename))

    form = TaskForm()
    if form.validate_on_submit():
        new_tasks = list()
        for mode in form.modes.data:
            # для записи в папку используем iso 8601 фрмат
            dirname = datetime.now().isoformat()
            task = Task(comment=form.comment.data)
            task.mode = Mode.query.get(int(mode))
            task.author = current_user
            path = os.path.join(os.path.realpath(app.config['UPLOADED_PATH']), "tasks", dirname)
            task.files = path
            shutil.copytree(path_upload, path)
            new_tasks.append(task)
        shutil.rmtree(path_upload)
        db.session.add_all(new_tasks)
        db.session.commit()
        flash("Успешная регистрация задания")
        return redirect(url_for('index'))

    return render_template('add_task.html', title="Новая задача", form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user, tasks=user.tasks)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash("Данные профиля успешно изменены")
        return redirect(url_for('edit_profile'))
    elif request.method == "GET":
        form.username.data = current_user.username
    return render_template('edit_profile.html', title='Редактор профиля', form=form)

