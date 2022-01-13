import bcrypt
from flask import Blueprint, render_template, redirect, request, flash
from flask.helpers import url_for
from flask_login import current_user, LoginManager, login_user, logout_user
from flask_login.utils import login_required
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import models

mod = Blueprint('accounts', __name__, template_folder="../templates")

login_manager = LoginManager() 

# Email Domain Validation (making sure the email ends in fcs domain)
class ValidEmailDomain:
    def __init__(self, suffix, message = None):
        assert suffix != None
        self.suffix = suffix
        self.message = message
    def __call__(self, form, field):
        if field.data.endswith(self.suffix):
            return
        else:
            raise ValidationError(f'Email must be part of {self.suffix} domain')

class ValidRegistrationEmail:
    def __call__(self, form, field):
        exists = models.Account.query.filter_by(email=field.data.lower()).first()
        if not exists:
            raise ValidationError(f'Email not whitelisted, please contact your administrator')

# This will probably get deleted later if we go with the account claiming system.
class UniqueRegistrationEmail:
    def __call__(self, form, field):
        exists = models.User.query.filter_by(email=field.data.lower()).first()
        if exists:
            raise ValidationError(f'User with email already exists')

# Email Validation
class ValidLoginEmail:
    def __call__(self, form, field):
        user = models.User.query.filter_by(email=form.data['email'].lower()).first()
        if user is None:
            raise ValidationError(f'Email Not Registered')

# Password Validation
class CheckPassword:
    def __call__(self, form, field):
        user = models.User.query.filter_by(email=form.data['email'].lower()).first()
        if user is None:
            return
        valid = bcrypt.hashpw(field.data.encode(), user.password) == user.password
        if not valid:
            raise ValidationError(f'Incorrect password')

# If the tech dept. ever decides to change the domain, we can just change it here
fcs_suffix = "friendscentral.org"

# Form for registration
class RegisterForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(), ValidEmailDomain(suffix=fcs_suffix), ValidRegistrationEmail(), UniqueRegistrationEmail()])
    password = StringField(label='Password', validators=[
        DataRequired(),
        Length(min=8),
        EqualTo('password_confirm', message='Passwords must match')
    ])
    password_confirm = StringField(label='Password confirm', validators=[
        DataRequired(),
        Length(min=8),
        EqualTo('password', message='Passwords must match')
    ])

# Form for logging in
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), ValidEmailDomain(suffix=fcs_suffix), ValidLoginEmail()])
    password = StringField(label='Password', validators=[DataRequired(), CheckPassword()])
    remember_me = BooleanField(label = 'Remember Me')

# Registration Routing
@mod.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template("register.html", form=form)
    if request.method == 'POST':
        # This is where the registration request is handled
        if form.validate_on_submit():
            # Hash Password with Bcrypt
            pw_hash = bcrypt.hashpw(form.password.data.encode(),bcrypt.gensalt())
            # Add user data to user table
            account = models.Account.query.filter_by(email=form.email.data).first()
            models.db.session.add(models.User(account.id, form.data['fname'], form.data['lname'], form.data['email'], pw_hash))
            models.db.session.commit()
            return redirect("/")
        # This person did not successfully enter the form
        return render_template('register.html', form=form)
        
# Load User
@login_manager.user_loader
def load_user(userid):
    return models.User.query.get(userid)

# Login Unauthorized Handler
@login_manager.unauthorized_handler
def handle_needs_login():
    flash("You have to be logged in to access this page.")
    return redirect(url_for('accounts.login', next=request.endpoint))

# Redirect Destination
def redirect_dest(fallback):
    dest = request.args.get('next')
    try:
        dest_url = url_for(dest)
    except:
        return redirect(fallback)
    return redirect(dest_url)

# Login Routing
@mod.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template("login.html", form=form)
    if request.method == 'POST':
        # This is where the login request is handled
        if form.validate_on_submit():
            user = models.User.query.filter_by(email=form.email.data).first()
            login_user(user, remember=form.remember_me)
            flash('Logged in successfully.')
            # This works, but does not redirect, only renders the index page
            return redirect(url_for('community.profile', userid=current_user.id))
        # This person did not successfully enter the form
        return render_template('login.html', form=form)

@mod.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('general.homepage'))


# SQL TEST, SEE ../templates/demo_users.html for details     
@mod.route("/show_users", methods=['GET'])
def show_user_list():
    usertable = models.db.session.query(models.User).all()
    return render_template('demo_users.html', users=usertable)