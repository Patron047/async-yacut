from datetime import datetime

from yacut import db
from yacut.constants import ORIGINAL_URL_MAX_LENGTH, SHORT_ID_MAX_LENGTH


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(
        db.String(ORIGINAL_URL_MAX_LENGTH), nullable=False
    )
    short = db.Column(
        db.String(SHORT_ID_MAX_LENGTH), unique=True, nullable=False
    )
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'url': self.original,
            'short_link': self.short,
        }
