import os
from flask import Flask


def create_app():
    config = os.environ.get('FLASK_CONFIG')
    app = Flask(__name__)
    app.config.from_object(config)
    register_blueprints(app)
    return app


def register_blueprints(app):
    from .views import general
    from .views import accounts
    app.register_blueprint(general.mod)
    app.register_blueprint(accounts.mod)
