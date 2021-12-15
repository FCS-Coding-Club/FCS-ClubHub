import json
import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from .models import models, test_db, utils
from .views import accounts

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
        init_account_json()
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

admin_json = {
    "NAME": "Admin",
    "GRADE": "12",
    "EMAIL": "admin@"+accounts.fcs_suffix
}

def sanitize_account_json(json):
    for e in json:
        # TODO: Add Name Sanitation
        e["GRADE"] = e["GRADE"].replace("GRADE ", "")
        e["EMAIL"] = e["EMAIL"].lower()
    return json
# Checks for a file accts.json, if not, creates one, and then fills clubhub.db with json data
def init_account_json():
    # Create File if it does not exist
    open('accts.json', 'w').close()
    # Open and Read File
    with open('accts.json', 'r+') as file:
        r = file.read()
        if r == "":
            accts_json = []
        else: 
            accts_json = json.loads(r)
        accts_json = sanitize_account_json(accts_json)
        if not utils.account_exists(accts_json, "Admin"):
            accts_json.append(admin_json)

    utils.fill_account_json_in_db(accts_json)