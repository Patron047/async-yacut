from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import (
    DataRequired, URL, Length, ValidationError, Regexp, Optional
)

from yacut.constants import (
    CUSTOM_ID_MAX_LENGTH,
    CUSTOM_ID_PATTERN,
    RESERVED_SHORT_IDS
)
from yacut.models import URLMap


class ShortenLinkForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[DataRequired(), URL(message='Некорректный URL')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(max=CUSTOM_ID_MAX_LENGTH),
            Regexp(
                CUSTOM_ID_PATTERN,
                message='Недопустимые символы в короткой ссылке'
            )
        ]
    )

    def validate_custom_id(self, field):
        if field.data:
            if field.data in RESERVED_SHORT_IDS:
                raise ValidationError(
                    'Предложенный вариант короткой ссылки уже существует.'
                )
            if URLMap.query.filter_by(short=field.data).first():
                raise ValidationError(
                    'Предложенный вариант короткой ссылки уже существует.'
                )


class UploadFilesForm(FlaskForm):
    files = FileField('Файлы', validators=[DataRequired()])
