from yacut import db
from yacut.models import URLMap


def create_url_record(original_url, short_id):
    """Создает запись URLMap в базе данных."""
    new_url = URLMap(original=original_url, short=short_id)
    db.session.add(new_url)
    return new_url