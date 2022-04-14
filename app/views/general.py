from flask import Blueprint, render_template
from flask_login import current_user
from json import dumps
from werkzeug.exceptions import HTTPException

mod = Blueprint('general', __name__, template_folder='../templates')


# Landing Page Routing
@mod.route("/")
def homepage():
    return render_template("index.html", current_user=current_user)

# Non-2xx Status Handling
@mod.app_errorhandler(HTTPException)
def page_not_found(e: HTTPException):
    # Custom Error Pages
    if e.code in [400, 403, 404]:
        return render_template(f'error/4xx.html', e = e)
    # Fallback Default JSON Error
    r = e.get_response()
    # replace the body with JSON
    r.data = dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    r.content_type = "application/json"
    return r