import os
from flask import Flask

config = os.environ.get('FLASK_CONFIG')

app = Flask(__name__)
app.config.from_object('config')

# Late Import for dependency stuff
from .views import index
