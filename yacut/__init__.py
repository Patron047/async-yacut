import os

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

# Импорты blueprint после инициализации db для избежания циклических импортов.
from yacut.views import main
from yacut.api_views import api
from yacut.error_handlers import errors


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URI', 'sqlite:///db.sqlite3'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DISK_TOKEN'] = os.environ.get('DISK_TOKEN')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main)
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(errors)

    return app


app = create_app()
