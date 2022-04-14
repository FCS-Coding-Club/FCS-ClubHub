from .models import Account, Club, db, Member, User
from app.views.accounts import login_manager


# JSON Funcs

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


def load_member(club_id, user_id):
    m = Member.query.filter(Member.club_id == club_id, 
                            Member.user_id == user_id)
    if m is None:
        return None
    return m.first()

# Checks if user (user_id) is a member of club (club_id)
def is_member(club_id, user_id):
    return bool(Member.query.filter(Member.club_id == club_id,
                                 Member.user_id == user_id).first())


# Checks if user (user_id) is a leader of club (club_id)
def is_leader(club_id, user_id):
    return bool(Member.query.filter(Member.club_id == club_id,
                                    Member.user_id == user_id,
                                    Member.isLeader).first())


# Checks if user (user_id) is a site admin
# Returns None if user / account DNI
def is_admin(user_id):
    user = Member.query.get(user_id)
    if user is None:
        return None
    acct = Account.query.get(id=user.account_id)
    if acct is None:
        return None
    return acct.admin

def event_exists(club: Club, event_id: str):
    e = club.get_event_by_uid(event_id)
    return e is not None


"""Loads the clubs a user is in, and returns a list of dictionaries:
The "club" key holds the club object as defined in the SQLAlchemy Schema.
The "isLeader" key holds a boolean of whether the member is a leader or not.
Feel free to change this if you have a cleaner way to structure it."""


def load_user_clubs(user_id):
    memberships = load_user_memberships(user_id)
    clubs = []
    for membership in memberships:
        club = Club.query.get(membership.club_id)
        clubs.append({"club": club, "isLeader": membership.isLeader})
    return clubs
