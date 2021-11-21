import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect



def create_app():
    config = os.environ.get('FLASK_CONFIG')
    app = Flask(__name__)
    app.config.from_object(config)
    register_blueprints(app)
    csrf = CSRFProtect(app)
    app.config.update(dict(
    SECRET_KEY=os.environ.get("SECRET_KEY"),
    WTF_CSRF_SECRET_KEY=os.environ.get("SECRET_KEY")
    ))
    csrf.init_app(app)
    return app


def register_blueprints(app):
    from .views import general
    from .views import accounts
    app.register_blueprint(general.mod)
    app.register_blueprint(accounts.mod)
