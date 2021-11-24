from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Database Models
class User(db.Model):
    __tablename__ = 'users'
    fname = db.Column(db.Text, nullable=False)
    lname = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True, primary_key=True)

    def __init__(self, fname, lname, email):
        self.fname = fname
        self.lname = lname
        self.email = email

    def __repr__(self):
        return f'<User {self.fname} {self.lname}>'