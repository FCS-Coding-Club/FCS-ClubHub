from calendar import monthrange
from datetime import datetime, timezone
from flask import abort, Blueprint, redirect, request
from flask.templating import render_template
from flask.helpers import url_for
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SelectField, TextAreaField
from wtforms.fields import DateField, TimeField, IntegerField
from wtforms.validators import DataRequired, Length, Optional, ValidationError
from app.models import dbutils, models

mod = Blueprint('community', __name__, template_folder='../templates')


class UniqueClubName:
    def __call__(self, form, field):
        exists = models.Club.query.filter_by(name=field.data).first()
        if exists:
            raise ValidationError(f'Club with name {field.data} already exists')

# "Inspired" by:
# https://stackoverflow.com/questions/56085973/flask-wtforms-disabling-multiple-fields-with-multiple-buttons
class OptionalIf(Optional):

    def __init__(self, otherFieldName, *args, **kwargs):
        self.otherFieldName = otherFieldName
        #self.value = value
        super(OptionalIf, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        otherField = form._fields.get(self.otherFieldName)
        if otherField is None:
            raise Exception('no field named "%s" in form' % self.otherFieldName)
        if bool(otherField.data):
            super(OptionalIf, self).__call__(form, field)


class RegisterClubForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=30), UniqueClubName()])
    desc = TextAreaField('Description', validators=[Optional(), Length(max=280)])


class AddEventForm(FlaskForm):
    name = StringField('Event Name', id="aef-name", validators=[DataRequired(), Length(min=4, max=30)])
    desc = TextAreaField('Event Description', id="aef-description", validators=[Length(max=280)])
    start_time = TimeField('Start Time', id="aef-start_time", validators=[DataRequired()])
    end_time = TimeField('End Time', id="aef-end_time", validators=[DataRequired()])
    repeat = BooleanField('Repeat Event?', id="aef-repeat", validators=[Optional()])
    indefrepeat=BooleanField('Repeat Indefinitely?', id="aef-indefrepeat",
    validators=[OptionalIf("repeat")])
    every = IntegerField('Every', id="aef-every", validators=[OptionalIf("repeat")])
    freq = SelectField(label='Frequency', validators=[OptionalIf("repeat")], id="aef-frequency",
    choices=[("daily", "Day(s)"), ("weekly", "Week(s)"), ("monthly", "Month(s)")])
    until = DateField(label='Until', id="aef-until", validators=[OptionalIf("indefrepeat")])

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
    # Check if club exists
    if current_club is not None:
        members = dbutils.load_club_members(clubid)
        leaders = list(filter(lambda m: m.isLeader, members))
        # For join / leave buttons
        isMember = dbutils.is_member(clubid, current_user.id)
        # Add Administrative buttons if leader
        isLeader = dbutils.is_leader(clubid, current_user.id) 
        return render_template('club.html',
                               current_club=current_club,
                               current_user=current_user,
                               members=members,
                               leaders=leaders,
                               isClubMember=isMember,
                               isClubLeader=isLeader)
    abort(404)

# Join Club Function
@mod.route("/join_club", methods=["GET"])
@login_required
def join_club():
    clubid = request.args.get('club')
    if clubid is None:
        abort(404)
    club = dbutils.load_club(clubid)
    if club is None:
        abort(400)
    member = dbutils.is_member(clubid, current_user.id)
    if member:
        abort(403)
    models.db.session.add(models.Member(current_user.id, clubid, False))
    models.db.session.commit()
    return redirect(url_for('community.club', clubid=clubid))

# Leave Club Function
@mod.route("/leave_club", methods=["GET"])
@login_required
def leave_club():
    clubid = request.args.get('club')
    if clubid is None:
        abort(404)
    club = dbutils.load_club(clubid)
    if club is None:
        abort(400)
    member: models.Member = dbutils.load_member(clubid, current_user.id)
    if not bool(member):
        abort(403)
    models.db.session.delete(member)
    models.db.session.commit()
    return redirect(url_for('community.club', clubid=clubid))

def validmmddyyyy(day: str):
    if len(day) != 8:
        return False
    try:
        m = int(day[0:2])
        d = int(day[2:4])
        y = int(day[4:8])
    except ValueError:
        return False
    if m == 0 or m > 12:
        return False
    _, mr = monthrange(y, m)
    if d == 0 or d > mr:
        return False
    return True

def parse_mmddyyyy(day: str):
    assert validmmddyyyy(day)
    m = int(day[0:2])
    d = int(day[2:4])
    y = int(day[4:8]) 
    return m, d, y


# Add Club Meeting Form
@mod.route("/add_meeting", methods=["GET", "POST"])
@login_required
def add_meeting():
    clubid = request.args.get('club')
    day = request.args.get('day')
    # Check for valid arguments
    if clubid is None or day is None:
        abort(404)
    if not dbutils.is_leader(clubid, current_user.id):
        abort(403)
    if not validmmddyyyy(day):
        abort(400)
    m, d, y = parse_mmddyyyy(day)
    # For the min value of the "until" date-type input
    day_yyyy_mm_dd = f"{y}-{str(m).zfill(2)}-{str(d).zfill(2)}"
    form = AddEventForm()
    if request.method == "GET":
        # Return form
        return render_template('add_meeting.html', clubid=clubid,
        day=day, day_yyyy_mm_dd=day_yyyy_mm_dd, form=form)
    if request.method == "POST":
        if form.validate_on_submit():
            # Check for valid Club id
            club = dbutils.load_club(clubid)
            if club is None:
                abort(400)
            # start time and end time vars
            st, et = form.start_time.data, form.end_time.data
            # Create recurrence rule dict if needed
            rrule = {
                    'freq': form.freq.data,
                    'interval': form.every.data,
            }  if form.repeat.data else None
            # Add Until if needed
            if not form.indefrepeat.data and rrule is not None:
                rrule['until'] = datetime.combine(form.until.data,
                    datetime.min.time()).astimezone(timezone.utc)
            # Add Event to Club Calendar
            club.add_event(
                start_date=datetime(y, m, d, st.hour, st.minute, st.second).astimezone(timezone.utc),
                end_date=datetime(y, m, d, et.hour, et.minute, et.second).astimezone(timezone.utc),
                summary=form.name.data,
                desc=form.desc.data,
                recurrence_rule = rrule
            )
            # Commit Changes
            models.db.session.commit()
            return redirect(url_for('community.club', clubid=clubid))
        return render_template('add_meeting.html', clubid=clubid,
        day=day, day_yyyy_mm_dd=day_yyyy_mm_dd, form=form)
    abort(404)

# Delete Club Meeting
@mod.route("/delete_meeting", methods=["GET"])
@login_required
def delete_meeting():
    clubid = request.args.get('club')
    uid = request.args.get('uid')
    if clubid is None or uid is None:
        abort(404)
    if not dbutils.is_leader(clubid, current_user.id):
        abort(403)
    club: models.Club = dbutils.load_club(clubid)
    if club is None:
        abort(400)
    if dbutils.event_exists(club, uid):
        club.remove_event(uid)
        models.db.session.commit()
        return redirect(url_for('community.club', clubid=clubid))
    abort(400)