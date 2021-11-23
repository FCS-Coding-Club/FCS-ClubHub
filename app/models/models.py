from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Database Models
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key = True)
    fname = db.Column(db.Text)
    lname = db.Column(db.Text)
    email = db.Column(db.Text, unique=True)

    def __init__(self, name, email):
        self.id = user_id
        self.fname = fname
        self.lname = lname
        self.email = email

    def __repr__(self):
        return f'<User {self.fname} {self.lname}>'