from flask import Blueprint, render_template
from flask_login import current_user

mod = Blueprint('general', __name__, template_folder='../templates')

# Landing Page Routing
@mod.route("/")
@mod.route("/home")
def homepage():
    return render_template("index.html", current_user=current_user)
