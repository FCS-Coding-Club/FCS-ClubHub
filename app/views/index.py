from flask import render_template, request
from app import app


@app.route("/")
@app.route("/home")
def hello():
    return render_template("index.html", name="Coding Club")

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    if request.method == 'POST':
        return render_template("index.html", name=request.form.get("fname", "Coding Club"))