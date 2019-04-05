#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
from flask import request
from app import app
from app import mail
from app import db
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.forms import TaskForm
from app.forms import EditProfileForm
from app.forms import PasswordRecoveryForm
from app.forms import ControleCode
from app.models import User
from app.models import Role
from app.models import Task
from app.models import Mode
from app.models import File
from app.models import State
from app.models import Position
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from werkzeug.urls import url_parse
import os
from datetime import datetime
import shutil
from flask_mail import Message
import random


@app.route('/')
@app.route('/index')
def index():
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
    path_upload = os.path.join(app.config['UPLOADED_PATH'], "tmp", current_user.username, "new_task")

    # загрузка файлов из dropzone
    if request.method == 'POST':
        files = request.files
        for key, upload_file in files.items():
            # проверка существования каталога
            if not os.path.isdir(path_upload):
                os.makedirs(path_upload)
            upload_file.save(os.path.join(path_upload, upload_file.filename))

    form = TaskForm()
    if form.validate_on_submit():
        for mode in form.modes.data:
            task = Task(comment=form.comment.data)
            task.mode = Mode.query.get(int(mode))
            task.author = current_user
            task.task_state = State.query.filter_by(name='queue').first()
            task.task_position = Position.query.get(int(form.position.data))

            db.session.add(task)
            db.session.commit()

            # копирование файлов в папку на сервере из временной папки
            # для записи в папку используем iso 8601 фрмат
            dir_name = datetime.now().isoformat()
            path_to_files = os.path.join(os.path.realpath(app.config['UPLOADED_PATH']), "tasks", dir_name)

            if os.path.isdir(path_upload):
                shutil.copytree(path_upload, path_to_files)

            if os.path.isdir(path_to_files):
                for file_name in os.listdir(path_to_files):
                    file = File()
                    file.add(path_to_files, file_name)
                    db.session.add(file)
                    db.session.commit()
                    task.files_id.append(file)
                    db.session.commit()

        if os.path.isdir(path_upload):
            shutil.rmtree(path_upload)

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
        current_user.email = form.email.data
        current_user.set_password(form.password.data)
        db.session.commit()
        flash("Данные профиля успешно изменены")
        return redirect(url_for('edit_profile'))
    elif request.method == "GET":
        form.username.data = current_user.username
    return render_template('edit_profile.html', title='Редактор профиля', form=form)


@app.route('/password_recovery', methods=['GET', 'POST'])
def password_recovery():
    email_form = PasswordRecoveryForm()
    code_form = ControleCode()

    args = {'email': True,
            'code': False}

    if email_form.validate_on_submit() and email_form.submit_email.data:
        msg = Message('Восстановление пароля', sender=app.config['MAIL_USERNAME'], recipients=[email_form.email.data])
        code = get_code()
        messege = 'Код подтверждения:<b>{code}</b>'.format(code=code)
        msg.html = messege
        mail.send(msg)
        args = {'email': False,
                'code': True}
        flash("На Ваш почтовый адресс отправлено письмо с кодом")
        user = User.query.filter_by(email=email_form.email.data).first()
        user.code = code
        db.session.commit()

    if code_form.validate_on_submit() and code_form.submit_code.data:
        user = User.query.filter_by(code=code_form.code.data).first_or_404()
        if user.code == code_form.code.data:
            password = random.randint(1000, 9999)
            msg = Message('Новый пароль', sender=app.config['MAIL_USERNAME'],
                          recipients=[user.email])
            messege = 'Ваш новый пароль:<b>{password}</b>'.format(password=password)
            msg.html = messege
            mail.send(msg)
            user.set_password(str(password))
            db.session.commit()
            flash("Ваш пароль успешно изменен")
            return redirect(url_for('edit_profile'))
        else:
            flash("Неверный код подтверждения")

    return render_template('password_recovery.html', title='Восстановление пароля',
                           email_form=email_form, code_form=code_form, args=args)


def get_code():
    code = random.getrandbits(32)
    if User.query.filter_by(code=code).first() is None:
        return code
    else:
        get_code()
