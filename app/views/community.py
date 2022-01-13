from flask import Blueprint, request
from flask.templating import render_template
from flask_login import current_user, login_required

from app.views.accounts import load_user

mod = Blueprint('community', __name__, template_folder='../templates')

# Profile Routing
@mod.route("/profile/<userid>", methods=["GET"])
@login_required
def profile(userid):
    profile_user = load_user(userid)
    return render_template('profile.html', profile_user=profile_user, current_user=current_user)