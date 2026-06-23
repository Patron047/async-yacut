import re

from flask import Blueprint, jsonify, request, url_for

from yacut import db
from yacut.models import URLMap
from yacut.utils import get_unique_short_id

api = Blueprint('api', __name__)


@api.route('/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'message': 'Отсутствует тело запроса'}), 400

    url = data.get('url')
    if not url:
        return jsonify({'message': '"url" является обязательным полем!'}), 400

    custom_id = data.get('custom_id')
    if custom_id is not None and custom_id != '':
        pattern = r'^[a-zA-Z0-9]+$'
        if len(custom_id) > 16 or not re.match(pattern, custom_id):
            return jsonify({
                'message': 'Указано недопустимое имя для короткой ссылки'
            }), 400

        if custom_id == 'files':
            return jsonify({
                'message': (
                    'Предложенный вариант короткой ссылки уже существует.'
                )
            }), 400

        existing = URLMap.query.filter_by(short=custom_id).first()
        if existing:
            return jsonify({
                'message': (
                    'Предложенный вариант короткой ссылки уже существует.'
                )
            }), 400

        short_id = custom_id
    else:
        short_id = get_unique_short_id()

    new_url = URLMap(original=url, short=short_id)
    db.session.add(new_url)
    db.session.commit()
    full_short_link = url_for(
        'main.redirect_to_original',
        short_id=new_url.short,
        _external=True
    )

    return jsonify({
        'url': new_url.original,
        'short_link': full_short_link
    }), 201


@api.route('/id/<short_id>/', methods=['GET'])
def get_original_link(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        return jsonify({'message': 'Указанный id не найден'}), 404
    return jsonify({'url': url_map.original}), 200
