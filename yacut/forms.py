from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired, URL, Length, ValidationError

from yacut.models import URLMap


class ShortenLinkForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[DataRequired(), URL(message='Некорректный URL')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(max=16, message='Максимум 16 символов')]
    )

    def validate_custom_id(self, field):
        if field.data and URLMap.query.filter_by(short=field.data).first():
            raise ValidationError(
                'Предложенный вариант короткой ссылки уже существует.'
            )
        if field.data == 'files':
            raise ValidationError(
                'Предложенный вариант короткой ссылки уже существует.'
            )


class UploadFilesForm(FlaskForm):
    files = FileField('Файлы', validators=[DataRequired()])
