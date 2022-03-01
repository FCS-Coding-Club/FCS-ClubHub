from .models import Account, Club, db, Member, User
from app.views.accounts import login_manager
def account_exists(json, name):
    for e in json:
        if e["NAME"] == name:
            return True
    return False

def fill_account_json_in_db(json):
    for e in json:
        name = e["NAME"]
        grade = int(e["GRADE"])
        email = e["EMAIL"] 
        db.session.add(Account(name, grade, email))
    db.session.commit()

# Handy Utility functions for moving across different relational tables

def load_club(club_id):
    return Club.query.get(club_id)

def load_club_members(club_id):
    return Member.query.filter_by(club_id=club_id)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

def load_user_memberships(user_id):
    return Member.query.filter_by(user_id=user_id)

# Loads the clubs a user is in, and returns a list of dictionaries:
# The "club" key holds the club object as defined in the SQLAlchemy Schema.
# The "isLeader" key holds a boolean of whether the member is a leader or not.
# Feel free to change this if you have a cleaner way to structure it.
def load_user_clubs(user_id):
    memberships = load_user_memberships(user_id)
    clubs = []
    for membership in memberships:
        club = Club.query.get(membership.club_id)
        clubs.append({"club": club, "isLeader": membership.isLeader})
    return clubs