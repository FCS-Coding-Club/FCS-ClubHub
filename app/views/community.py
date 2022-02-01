from flask import abort, Blueprint, redirect, request
from flask.templating import render_template
from flask.helpers import url_for
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError

from app.views.accounts import load_user
from app.models import models

mod = Blueprint('community', __name__, template_folder='../templates')

class UniqueClubName:
    def __call__(self, form, field):
        exists = models.Club.query.filter_by(name=field.data).first()
        if exists:
            raise ValidationError(f'Club with name {field.data} already exists')

class RegisterClubForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=30), UniqueClubName()])
    desc = TextAreaField('Description', validators=[DataRequired(),Length(max=280)])

# Profile Routing
@mod.route("/profile/<userid>", methods=["GET"])
@login_required
def profile(userid):
    profile_user = load_user(userid)
    if profile_user is not None:
        return render_template('profile.html', profile_user=profile_user, current_user=current_user)
    abort(404)

# Register Club Form
@mod.route("/register_club", methods=["GET", "POST"])
@login_required
def register_club():
    form = RegisterClubForm()
    if request.method == 'GET':
        return render_template("register_club.html", form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            # Create Club
            models.db.session.add(models.Club(form.data['name'], form.data['desc']))
            models.db.session.commit()
            # Add Creator as Leader of Said Club
            new_club = models.Club.query.filter_by(name=form.data['name']).first()
            models.db.session.add(models.Member(current_user.id, new_club.id, True))
            models.db.session.commit()
            return redirect(url_for('community.club', clubid=new_club.id))
        return render_template('register_club.html', form=form)


# Club Routing
@mod.route("/club/<clubid>", methods=["GET"])
@login_required
def club(clubid):
    current_club = load_club(clubid)
    if current_club is not None:
        members = load_club_members(clubid)
        return render_template('club.html', current_club=current_club, current_user=current_user, members=members)
    abort(404)

def load_club(club_id):
    return models.Club.query.get(club_id)

def load_club_members(clubid):
    return models.Member.query.filter_by(club_id=clubid)