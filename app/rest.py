from app import app
from app import db
from flask import jsonify
from flask_login import login_required


@app.route('/manager/api/v1.0/last_task')
@login_required
def login_pkcu():
    data = {'1': '111',
            '2': '2222'}

    return jsonify(data)
