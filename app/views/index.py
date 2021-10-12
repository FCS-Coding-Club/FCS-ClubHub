from flask import render_template
from app import app


@app.route("/")
@app.route("/home")
def hello():
    return render_template("index.html", name="Coding Club")
