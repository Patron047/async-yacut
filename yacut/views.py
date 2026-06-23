import asyncio

from flask import (
    Blueprint, redirect, render_template, request, url_for
)

from yacut import db
from yacut.forms import ShortenLinkForm, UploadFilesForm
from yacut.models import URLMap
from yacut.utils import get_unique_short_id
from yacut.yandex_disk import upload_files_to_disk

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    form = ShortenLinkForm()
    short_link = None

    if form.validate_on_submit():
        short_id = form.custom_id.data or get_unique_short_id()
        new_url = URLMap(
            original=form.original_link.data,
            short=short_id
        )
        db.session.add(new_url)
        db.session.commit()
        short_link = url_for(
            'main.redirect_to_original',
            short_id=new_url.short,
            _external=True
        )

    return render_template(
        'index.html', form=form, short_link=short_link
    )


@main.route('/files', methods=['GET', 'POST'])
def upload_files():
    form = UploadFilesForm()
    uploaded_links = []

    if form.validate_on_submit():
        files = request.files.getlist('files')
        if files:
            loop = asyncio.new_event_loop()
            try:
                results = loop.run_until_complete(
                    upload_files_to_disk(files)
                )
            finally:
                loop.close()

            for result in results:
                short_id = get_unique_short_id()
                new_url = URLMap(
                    original=result['download_link'],
                    short=short_id
                )
                db.session.add(new_url)
            db.session.commit()

            for result in results:
                url_map = URLMap.query.filter_by(
                    original=result['download_link']
                ).first()
                uploaded_links.append({
                    'filename': result['filename'],
                    'short_id': url_map.short,
                    'short_url': url_for(
                        'main.redirect_to_original',
                        short_id=url_map.short,
                        _external=True
                    )
                })

    return render_template(
        'files.html', form=form, links=uploaded_links
    )


@main.route('/<short_id>', methods=['GET'])
def redirect_to_original(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original)
