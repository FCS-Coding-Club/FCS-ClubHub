from flask import Blueprint, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import models

mod = Blueprint('accounts', __name__, template_folder="../templates")

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
            raise ValidationError(f'email must be part of {self.suffix} domain')

# If the tech dept. ever decides to change the domain, we can just change it here
fcs_suffix = "friendscentral.org"

# Form for registration
class RegisterForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(), ValidEmailDomain(suffix=fcs_suffix)])
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
    email = StringField('Email', validators=[DataRequired(), Email(), ValidEmailDomain(suffix=fcs_suffix)])
    password = StringField(label='Password', validators=[DataRequired()])


@mod.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template("register.html", form=form)
    if request.method == 'POST':
        # This is where the registration request is handled
        if form.validate_on_submit():
            # This person successfully entered the form
            models.db.session.add(models.User(form.data['fname'], form.data['lname'], form.data['email']))
            models.db.session.commit()
            return redirect("/")
        # This person did not successfully enter the form
        return render_template('register.html', form=form)
        


@mod.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template("login.html", form=form)
    if request.method == 'POST':
        # This is where the login request is handled
        if form.validate_on_submit():
            # This is where the JWT auth will be
            return redirect("/")
        # This person did not successfully entered the form
        return render_template('login.html', form=form)

# SQL DEMO, DELETE LATER       
@mod.route("/show_users", methods=['GET'])
def show_user_list():
    usertable = models.db.session.query(models.User).all()
    return render_template('demo_users.html', users=usertable)