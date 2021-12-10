import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from .models import models, test_db

isDebug = os.environ.get("DEBUG")
isTesting = os.environ.get("TESTING")

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
    with app.app_context():
        models.db.drop_all()
        models.db.create_all()
        models.db.session.commit()
        # Adds dummy data for dev purposes
        if isDebug or isTesting:
            test_db.fill_with_test_data(models.db, app.app_context())
            
    return app

# App configuration Function
def app_config(app):
    config = os.environ.get('FLASK_CONFIG')
    app.config.from_object(config)
    app.config.update(dict(
    SECRET_KEY=os.environ.get("SECRET_KEY"),
    WTF_CSRF_SECRET_KEY=os.environ.get("SECRET_KEY"),
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../clubhub.db',
    SQLALCHEMY_TRACK_MODIFICATIONS = False))

# Blueprint Registration Function
def register_blueprints(app):
    from .views import general
    from .views import accounts
    for blueprint in [general.mod, accounts.mod]:
        app.register_blueprint(blueprint)
