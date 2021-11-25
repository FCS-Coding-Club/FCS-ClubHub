import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from .models import models

def create_app():
    # Init App
    app = Flask(__name__)
    # Configuration
    app_config(app)
    register_blueprints(app)
    # CSRF 
    csrf = CSRFProtect(app)
    csrf.init_app(app)
    # DB Init
    models.db.init_app(app)
    return app

def app_config(app):
    config = os.environ.get('FLASK_CONFIG')
    app.config.from_object(config)
    app.config.update(dict(
    SECRET_KEY=os.environ.get("SECRET_KEY"),
    WTF_CSRF_SECRET_KEY=os.environ.get("SECRET_KEY"),
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../clubhub.db',
    SQLALCHEMY_TRACK_MODIFICATIONS = False))


def register_blueprints(app):
    from .views import general
    from .views import accounts
    for blueprint in [general.mod, accounts.mod]:
        app.register_blueprint(blueprint)
