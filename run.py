#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from app import app
from app import db
from app.models import User
from app.models import Role
from app.models import Task


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Task': Task, 'Role': Role}

