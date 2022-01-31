import os
import random
import string
import sass
from app import create_app

# This file will run a Flask's WSGI server for development purposes. We will need to set up our own WSGI for production.

# Debug Checking
if os.environ.get('DEBUG') is None:
    os.environ["DEBUG"] = "True"
if os.environ.get('TESTING') is None:
    os.environ["TESTING"] = "False"

if os.environ.get('TESTING') == "False" and os.environ["DEBUG"] == "True":
    os.environ["SECRET_KEY"] = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
    os.environ["WTF_CSRF_SECRET_KEY"] = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
    os.environ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clubhub.db"
    app = create_app()
    app.run(host="0.0.0.0", port=3000, debug=os.environ["DEBUG"])
else:
    print("TESTING flag set to not False.")
