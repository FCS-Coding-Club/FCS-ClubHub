import json
import os
import random
import string
from flask import Flask
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
import sass
from sqlalchemy import create_engine
from .models import dbutils, models, mock_db
from .views import accounts
from .utils import render_functions

isDebug = os.environ.get("DEBUG") if os.environ.get("DEBUG") else "True"
isTesting = os.environ.get("TESTING") if os.environ.get("TESTING") else "False"


def create_app():
    # Compile Sass
    compile_sass()
    # Set env vars
    if isDebug == "True":
        setDebugEnvironmentVars()
    else:
        setProdEnvironmentVars()
    # Init App
    app = Flask(__name__)
    # Configuration
    app_config(app)
    register_blueprints(app)
    # CORS
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

    # CSRF 
    csrf = CSRFProtect(app)
    csrf.init_app(app)
    # Login Manager
    accounts.login_manager.init_app(app)
    # DB Init
    if "MYSQL_URL" in os.environ:
        e = create_engine(os.environ['MYSQL_URL'])
        e.execute(f"CREATE DATABASE IF NOT EXISTS {os.environ['RDS_DB_NAME']}")
    models.db.init_app(app)
    # Add Render Functions to Jinja Globals
    app.jinja_env.globals.update(render_functions)
    # Context Processing
    with app.app_context():
        if isDebug == "True":
            print(f"Debug env set to {isDebug}, flushing database...")
            models.db.drop_all()
            models.db.create_all()
            models.db.session.commit()
        init_account_json()
        # Adds dummy data for dev purposes
        if isDebug == "True" or isTesting == "True":
            mock_db.fill_with_test_data(models.db, app.app_context())
    return app


# App configuration Function
def app_config(app):
    config = os.environ.get('FLASK_CONFIG')
    app.config.from_object(config)
    app.config.update(dict(
        SECRET_KEY=os.environ.get("SECRET_KEY"),
        WTF_CSRF_SECRET_KEY=os.environ.get("SECRET_KEY"),
        SQLALCHEMY_DATABASE_URI=os.environ["SQLALCHEMY_DATABASE_URI"],
        SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_pre_ping": True,
            "pool_recycle": 300,
        },
        SQLALCHEMY_TRACK_MODIFICATIONS=False))


# Sass Compiling Function
def compile_sass():
    print("Compiling Sass...")
    compiled = sass.compile(filename='app/static/sass/main.scss', include_paths="bootstrap")
    with open('app/static/css/bootstrap_min.css', 'w') as css:
        css.write(compiled)

# Set Debug Environment Variables
def setDebugEnvironmentVars():
    setSecretKeyVars()
    os.environ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clubhub.db"

# Set Production Environment Variables
def setProdEnvironmentVars():
    setSecretKeyVars()
    # Set mysql uri for sqlalchemy
    if 'RDS_HOSTNAME' in os.environ:
        os.environ["MYSQL_URL"] = f"mysql+pymysql://{os.environ['RDS_USERNAME']}:{os.environ['RDS_PASSWORD']}@{os.environ['RDS_HOSTNAME']}:{os.environ['RDS_PORT']}"
        os.environ["SQLALCHEMY_DATABASE_URI"] = os.environ["MYSQL_URL"] + f"/{os.environ['RDS_DB_NAME']}"
    else:
        # Otherwise, fallback to sqlite
        os.environ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clubhub.db"

# Randomized secret keys for Flask and CSRF
def setSecretKeyVars():
    os.environ["SECRET_KEY"] = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
    os.environ["WTF_CSRF_SECRET_KEY"] = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))

# Blueprint Registration Function
def register_blueprints(app):
    from .api import calendar

    from .views import accounts
    from .views import community
    from .views import general
    for blueprint in [accounts.mod, calendar.mod, community.mod, general.mod]:
        app.register_blueprint(blueprint)


admin_json = {
    "NAME": "Admin",
    "GRADE": "12",
    "EMAIL": "admin@" + accounts.fcs_suffix
}


def sanitize_account_json(account_json):
    for e in account_json:
        # TODO: Add Name Sanitation
        e["GRADE"] = e["GRADE"].replace("GRADE ", "")
        e["EMAIL"] = e["EMAIL"].lower()
    return account_json


# Checks for a file accts.json, if not, creates one, and then fills clubhub.db with json data
def init_account_json():
    # Create File if it does not exist
    open('accts.json', 'a+').close()
    # Open and Read File
    with open('accts.json', 'r+') as file:
        r = file.read()
        if r == "":
            accts_json = []
        else:
            accts_json = json.loads(r)
        accts_json = sanitize_account_json(accts_json)
        if not dbutils.account_exists(accts_json, "Admin"):
            accts_json.append(admin_json)

    dbutils.fill_account_json_in_db(accts_json)
