from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Club Model
class Club(db.Model):
    __tablename__='clubs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    desc = db.Column(db.Text, nullable=True)

    def __init__(self, name, desc):
        self.name = name
        self.desc = desc   
    
    def __repr__(self):
        return f'<Club {self.name}, id {self.id}>'

# User Model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.Text, nullable=False)
    lname = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    password = db.Column(db.Text, nullable=False)

    def __init__(self, fname, lname, email, password, admin=False):
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
        return f'<Club {"Leader" if self.isLeader else "Member"}, id {self.user_id}>'

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