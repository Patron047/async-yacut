import random
import string

from yacut.models import URLMap


def get_unique_short_id(length=6):
    chars = string.ascii_letters + string.digits
    while True:
        short_id = ''.join(random.choices(chars, k=length))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id
