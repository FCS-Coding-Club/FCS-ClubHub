from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Club List
class Club(db.Model):
    __tablename__='clubs'
    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True, primary_key=True)
    desc = db.Column(db.Text, nullable=True)
    members = db.relationship("Member", backref="club",lazy='dynamic', primaryjoin="Club.id == Member.club_id")
    def __init__(self, cid, name, desc):
        self.cid = cid
        self.name = name
        self.desc = desc
    
    def __repr__(self):
        return f'<Club {self.name}, id {self.id}>'

# User List
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    fname = db.Column(db.Text, nullable=False)
    lname = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)

    def __init__(self, fname, lname, email):
        self.fname = fname
        self.lname = lname
        self.email = email

    def __repr__(self):
        return f'<User {self.fname} {self.lname}>'

# Club Member List
class Member(db.Model):
    __tablename__='members'
    member_id = db.Column(db.Integer, nullable=False, primary_key=True, unique=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable = False)
    club_id = db.Column(db.Integer, db.ForeignKey(Club.id), nullable = False)
    isLeader = db.Column(db.Boolean, nullable = False)

    def __init__(self, user_id, club_id, isLeader):
        self.user_id = user_id
        self.club_id = club_id
        self.isLeader = isLeader
    
    def __repr__(self):
        return f'<Club {self.isLeader : "Leader" ? "Member"}, id {self.user_id}>'