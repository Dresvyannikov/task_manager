from flask import render_template
from app import app
from app import db
from flask_login import current_user
from flask import jsonify


@app.errorhandler(404)
def not_found_error(error):
    if current_user.is_authenticated:
        if current_user.priority.user_role == 'remote':
            response = {
                'status': 'error',
                'message': 'not found source',
                'code': 404,
                'data': ''
            }
            return jsonify(response)
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if current_user.is_authenticated:
        if current_user.priority.user_role == 'remote':
            response = {
                'status': 'error',
                'message': 'error db',
                'code': 500,
                'data': ''
            }
            return jsonify(response)
    return render_template('500.html'), 500

