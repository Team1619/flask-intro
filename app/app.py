from flask import Flask
from app.extensions import db
from app.commands import db_init, print_concepts
from . import concepts  # noqa


def create_app():
    app = Flask('app')
    app.config.update(
        ENV='development',
        DEBUG=1,
        SQLALCHEMY_DATABASE_URI='sqlite:///app.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True,
        SECRET_KEY='secret',
    )
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    return app


def register_extensions(app: Flask):
    db.init_app(app)


def register_blueprints(app: Flask):
    app.register_blueprint(concepts.views.blueprint)


def register_commands(app: Flask):
    app.cli.add_command(db_init)
    app.cli.add_command(print_concepts)