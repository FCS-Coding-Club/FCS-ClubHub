from flask import abort, Blueprint, redirect, request
from flask.templating import render_template
from flask.helpers import url_for
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError
from datetime import datetime
import calendar
from app.models import dbutils, models

mod = Blueprint('community', __name__, template_folder='../templates')

class UniqueClubName:
    def __call__(self, form, field):
        exists = models.Club.query.filter_by(name=field.data).first()
        if exists:
            raise ValidationError(f'Club with name {field.data} already exists')

class RegisterClubForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=30), UniqueClubName()])
    desc = TextAreaField('Description', validators=[DataRequired(),Length(max=280)])

def get_calendar_data(month, year):
    mr = calendar.monthrange(year, month)
    cal_dictionary = {}
    for row in range(0, 6):
        for col in range(0, 7):
            cal_dictionary[(row, col)] = ""
    current_row = 0
    for day in range(mr[0],mr[1]+1):
        weekday = calendar.weekday(int(year), int(month), day)
        cal_dictionary[(current_row,weekday)] = day
        if weekday == 6: current_row += 1
    return cal_dictionary

# Profile Routing
@mod.route("/profile/<userid>", methods=["GET"])
@login_required
def profile(userid):
    profile_user = dbutils.load_user(userid)
    user_clubs = dbutils.load_user_clubs(userid)
    if profile_user is not None:
        return render_template('profile.html', 
        profile_user=profile_user, 
        current_user=current_user, 
        user_clubs=user_clubs)
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
    current_club = dbutils.load_club(clubid)
    if current_club is not None:
        members = dbutils.load_club_members(clubid)
        td = datetime.today()
        calendar = get_calendar_data(td.month, td.year)
        return render_template('club.html', 
        current_club=current_club, 
        current_user=current_user, 
        members=members,
        calendar=calendar)
    abort(404)