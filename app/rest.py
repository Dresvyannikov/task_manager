from app import app
from app import db
from app.models import Position
from app.models import Task
from app.models import State
from app.models import Mode
from flask import jsonify
import json

from flask import request
from flask_login import login_required


@app.route('/manager/api/v0.1/positions.json')
@login_required
def get_positions():
    positions = Position.query.all()
    data = list()
    for position in positions:
        data.append({'id': position.id, 'name': position.name})
    return jsonify(data)


@app.route('/manager/api/v0.1/positions/<id_position>/last_task.json', methods=['GET', 'PUT'])
@login_required
def get_last_task(id_position):
    # фильт выбирает одну задачу из задач. которые не имеют статус done, указанной позиции.
    task = Task.query.filter(Task.task_state != State.query.filter_by(name='done').first(),
                             Task.task_position == Position.query.get(int(id_position))).first()
    data = {}
    if request.method == "GET":
        data = {

            'id': task.id,
            'comment': task.comment,
            'timestamp': task.timestamp,
            'author': task.author.username,
            'mode': task.mode.name,
            'state': task.task_state.name,
            'position': task.task_position.name,
            'files': task.files_id
        }

    if request.method == "PUT":
        data = json.loads(request.data.decode('utf-8'))
        task = Task.query.get(int(data.get('id')))
        if task:
            task.comment = data.get('comment')
            task.author = data.get('data')

            mode = Mode.query.filter_by(name=data.get('mode')).first()
            if mode:
                task.mode = mode
            else:
                return 'error: not found {name}'.format(name=data.get('mode'))
            state = State.query.filter_by(name=data.get('state')).first()
            if state:
                task.task_state = state
            else:
                return 'error: not found {name}'.format(name=data.get('state'))

            position = Position.query.filter_by(name=data.get('position')).first()
            if position:
                task.task_position = position
            else:
                return 'error: not found {name}'.format(name=data.get('position'))

            db.session.commit()
            # TODO: при необходимости добавить обновление файлов
        else:
            return 'error: not found task id = {name}'.format(name=data.get('id'))

    return jsonify(data)


@app.route('/manager/api/v0.1/all_states.json')
@login_required
def get_all_states():
    states = State.query.all()
    data = list()
    for state in states:
        data.append({
            'id': state.id,
            'name': state.name,
            'name_rus': state.name_rus
        })

    return jsonify(data)
