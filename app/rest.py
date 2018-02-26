from app import app
from app import db
from app.models import Position
from app.models import Task
from app.models import State
from app.models import Mode
from app.models import User
from flask import jsonify
import json
from flask import request
from flask_login import login_required
from flask import send_from_directory


'''
Описание как выглядит ответ или запрос с данными

| ''Type'' | ''Description''                                        | ''Required Keys''  | ''Optional Keys'' |
|----------+--------------------------------------------------------+--------------------+-------------------|
| success  | All went well, and (usually) some data was returned.   | status, code, data |                   |
|          |                                                        |                    |                   |
| fail     | There was a problem with the data submitted,           | status, code, data |                   |
|          | or some pre-condition of the API call wasn't satisfied |                    |                   |
|          |                                                        |                    |                   |
| error    | An error occurred in processing the request,           | status, message    | code, data        |
|          | i.e. an exception was thrown                           |                    |                   |

{
    status : "success",
    data : {
        "post" : { "id" : 1, "title" : "A blog post", "body" : "Some useful content" }
     }
}

'''


def get_last_task(id_position):
    return Task.query.filter(Task.task_state != State.query.filter_by(name='done').first(),
                             Task.task_position == Position.query.get(int(id_position))).first()


class Response:
    status = ''
    data = ''
    message = ''
    code = ''
    response = {
        'status': status,
        'data': data,
        'message': message,
        'code': code
    }

    def __init__(self, status, data, message, code):
        self.status = status
        self.data = data
        self.message = message
        self.code = code

    def get(self):
        """
        прежде чем юзать класс, протести
        правильность выполнения уже существущих дынных и сделай вередачу файлов!!!
        """
        return jsonify(self.response)


@app.route('/manager/api/v0.1/positions.json')
@login_required
def get_positions():
    positions = Position.query.all()
    data_positions = list()
    for position in positions:
        data_positions.append({'id': position.id, 'name': position.name})
    response = {
        'status': 'success',
        'data': {
            'positions': data_positions
        }
    }
    return jsonify(response)


@app.route('/manager/api/v0.1/positions/<id_position>/last_task.json', methods=['GET', 'PUT'])
@login_required
def get_last_task_position(id_position):

    # фильт выбирает одну задачу из задач, которые не имеют статус done, указанной позиции.
    task = get_last_task(id_position)

    if not task:
        response = {
            'status': 'error',
            'message': 'not found last task',
            'code': 404,
            'data': ''
        }
        return jsonify(response)

    if request.method == "GET":
        files = []
        for file in task.files_id:
            files.append(file.name)
        data = {
            'id': task.id,
            'comment': task.comment,
            'timestamp': task.timestamp,
            'author': task.author.username,
            'mode': task.mode.name,
            'state': task.task_state.name,
            'position': task.task_position.name,
            'files': files
        }

        response = {
            'status': 'success',
            'data': {
                'task': data
            }
        }
        return jsonify(response)

    if request.method == "PUT":
        data = json.loads(request.data.decode('utf-8')).get('task')
        task = Task.query.get(int(data.get('id')))
        task.comment = data.get('comment')

        author = User.query.filter_by(username=data.get('author')).first()
        if author:
            task.author = author
        else:
            response = {
                'status': 'fail',
                'message': 'not found author {name}'.format(name=data.get('author')),
                'code': 404,
                'data': ''
            }
            return jsonify(response)

        mode = Mode.query.filter_by(name=data.get('mode')).first()
        if mode:
            task.mode = mode
        else:
            response = {
                'status': 'fail',
                'message': 'error: not found {name}'.format(name=data.get('mode')),
                'code': 404,
                'data': ''
            }
            return jsonify(response)

        state = State.query.filter_by(name=data.get('state')).first()
        if state:
            task.task_state = state
        else:
            response = {
                'status': 'fail',
                'message': 'error: not found {name}'.format(name=data.get('state')),
                'code': 404,
                'data': ''
            }
            return jsonify(response)

        position = Position.query.filter_by(name=data.get('position')).first()
        if position:
            task.task_position = position
        else:
            response = {
                'status': 'fail',
                'message': 'error: not found {name}'.format(name=data.get('position')),
                'code': 404,
                'data': ''
            }
            return jsonify(response)

        db.session.commit()

    response = {
        'status': 'success',
        'data': 'result'
    }

    return jsonify(response)

# TODO: при необходимости добавить обновление файлов


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

    response = {
        'status': 'success',
        'data':
            {'states': data}
    }

    return jsonify(response)


@app.route('/manager/api/v1.0/tasks/<task_id>/app_result', methods=['GET', 'PUT', 'POST'])
@login_required
def set_result_files(task_id):
    if request.method == 'POST':
        # создание результата ДИ
            files = request.files
            for key, upload_file in files.items():
                print(key, upload_file)
            print(request.data)
            print(request.get_data())

    if request.method == 'PUT':
        # обновление результата ДИ
        pass
    return ''


@app.route('/manager/api/v1.0/positions/<id_position>/last_task/files/<file_name>/file_info.json')
@login_required
def get_file_info(id_position, file_name):
    # передать информацию о файле

    response = {
        'status': 'fail',
        'message': 'not found file {name}'.format(name=file_name),
        'code': 404,
        'data': ''
    }

    task = get_last_task(id_position)
    # если файл будет найден, то переменная перезапишется
    for file in task.files_id:
        if file.name == file_name:
            response = {
                'status': 'success',
                'data': {
                    'type': file.type,
                    'size': file.size,
                    'md5sum': file.md5sum
                }
            }

    return jsonify(response)


@app.route('/manager/api/v1.0/positions/<id_position>/last_task/files/<file_name>', methods=['GET', 'PUT'])
@login_required
def upload_files(id_position, file_name):
    # отдать файл
    if request.method == 'GET':
        task = get_last_task(id_position)
        for file in task.files_id:
            if file.name == file_name:
                return send_from_directory(file.path, file.name)
    # перезаписать файл
    if request.method == 'PUT':
        # TODO: при необходимости оформить как form с файлом
        pass
