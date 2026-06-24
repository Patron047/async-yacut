import random
import string

from yacut.constants import SHORT_ID_LENGTH
from yacut.models import URLMap


def get_unique_short_id(length=SHORT_ID_LENGTH):
    chars = string.ascii_letters + string.digits
    while True:
        short_id = ''.join(random.choices(chars, k=length))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id
