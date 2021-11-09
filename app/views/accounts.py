from flask import Blueprint, render_template, request

mod = Blueprint('accounts', __name__, template_folder="../templates")


@mod.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    if request.method == 'POST':
        return render_template("index.html", name=request.form.get("fname", "Coding Club"))
