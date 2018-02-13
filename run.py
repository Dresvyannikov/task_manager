#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from app import app
from app import db
from app.models import User
from app.models import Role
from app.models import Task
from app.models import Mode
from app.models import File
from app.models import Status


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Task': Task, 'Role': Role, 'Mode': Mode, 'File': File, 'Status': Status}
