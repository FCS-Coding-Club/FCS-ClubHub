from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# Club Model
class Club(db.Model):
    __tablename__='clubs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    desc = db.Column(db.Text, nullable=True)
    verified = db.Column(db.Boolean, nullable=False)

    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        self.verified = False
    
    def __repr__(self):
        return f'<Club {self.name}, id {self.id}>'

# Account Model (Whitelisted but Unclaimed)
class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, name, grade, email, admin=False):
        self.name = name
        self.grade = grade
        self.email = email
        self.admin = admin

# User Model (Claimed)
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(db.Integer, db.ForeignKey(Account.id), nullable=False)
    fname = db.Column(db.Text, nullable=False)
    lname = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, db.ForeignKey(Account.email), nullable=False)
    admin = db.Column(db.Boolean, db.ForeignKey(Account.admin), nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __init__(self, account_id, fname, lname, email, password, admin=False):
        self.account_id = account_id
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = password
        self.admin = admin

    def __repr__(self):
        return f'<User {self.fname} {self.lname} - id {self.id}>'

# Club Member Model
class Member(db.Model):
    __tablename__='members'
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable = False, primary_key=True)
    club_id = db.Column(db.Integer, db.ForeignKey(Club.id), nullable = False, primary_key=True)
    isLeader = db.Column(db.Boolean, nullable = False)
    user = db.relationship("User")

    def __init__(self, user_id, club_id, isLeader):
        self.user_id = user_id
        self.club_id = club_id
        self.isLeader = isLeader
    
    def __repr__(self):
        return f'<Club {"Leader" if self.isLeader else "Member"}, id {self.user_id}, club_id {self.club_id}>'

# Club Announcement Model
class Announcement(db.Model):
    __tablename__='announcements'
    announcement_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    club_id = db.Column(db.Integer, db.ForeignKey(Club.id), nullable = False)
    title = db.Column(db.Text, nullable = False)
    desc = db.Column(db.Text, nullable = False)
    # This will be added on construction of class
    time = db.Column(db.Text, nullable = False)

    def __init__(self, club_id, title, description):
        self.club_id = club_id
        self.title = title
        self.desc = description
        self.time = str(datetime.utcnow())

    def __repr__(self):
        return f'<Announcement: {self.title} - by {self.club_id}>'

class Meeting(db.Model):
    __tablename__='meetings'
    meeting_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    club_id = db.Column(db.Integer, db.ForeignKey(Club.id), nullable = False)
    # In MMDDYYYY Format
    meeting_day = db.Column(db.Text, nullable = False)
    # Repeats are in days (7 = weekly, 14 = bi-weekly, etc)
    repeats = db.Column(db.Integer, nullable = False)

    def __init__(self, club_id, meeting_day, repeats):
        self.club_id = club_id
        self.meeting_day = meeting_day
        self.repeats = repeats
    
    def __repr__(self):
        return f'<Meeting: on {self.meeting_day} - by {self.club_id}>'