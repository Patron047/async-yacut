from flask import Blueprint, jsonify, render_template, request

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def not_found(error):
    if request.path.startswith('/api/'):
        return jsonify({'message': 'Указанный id не найден'}), 404
    return render_template('error.html',
                           error_code=404,
                           error_message='Страница не найдена'
                           ), 404


@errors.app_errorhandler(500)
def internal_error(error):
    if request.path.startswith('/api/'):
        return jsonify({'message': 'Внутренняя ошибка сервера'}), 500
    return render_template('error.html',
                           error_code=500,
                           error_message='Внутренняя ошибка сервера'
                           ), 500
