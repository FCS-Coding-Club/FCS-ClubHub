from flask import Blueprint, render_template

mod = Blueprint('general', __name__, template_folder='../templates')

# Landing Page Routing
@mod.route("/")
@mod.route("/home")
def hello():
    return render_template("index.html")
