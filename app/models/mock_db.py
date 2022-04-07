from datetime import datetime, timezone
from dateutil import rrule
from .models import User, Club, Member, Announcement, Account, db
from app.views import accounts

# This script configures the database with dummy data for testing purposes

# Test Data for dev purposes. 
test_clubs = [
    Club("Coding Club", "The Creators of this website"),
    Club("Cooking Club", "Join if you love food"),
    Club("Nature Club", "We go on nature walks and stuff"),
]


# These need to be defined after the clubs are serialized in the database
def define_relational_test_data():
    test_announcements = [
        Announcement(test_clubs[0].id, "Meeting Every Two Weeks", "Come to the meeting, it'll be fun!"),
        Announcement(test_clubs[1].id, "Meeting Today", "Meeting today! We will be using a toaster."),
        Announcement(test_clubs[1].id, "The Toaster Incident", "Remember everyone, nothing happened."),
    ]
    return test_announcements


# Function to add all test data
def fill_with_test_data(database, ctx):
    with ctx:

        for club in test_clubs:
            database.session.add(club)
            club.add_event(
                start_date=datetime(2022, 3, 1, 10, 30, 0),
                end_date=datetime(2022, 3, 1, 12, 30, 0),
                summary="Test Event",
                desc="Testing Testing 1 2",
                recurrence_rule={
                    'freq': 'daily',
                    'interval': 2,
                    'until': datetime(2022, 3, 11, 0, 0, 0).astimezone(timezone.utc)
                }
            )
            event = club.get_events_by_summary("Test Event")[0]
            club.edit_event(event['uid'], {
                'dtstart': datetime(2022, 2, 25, 10, 30, 0).astimezone(timezone.utc),
                'dtend': datetime(2022, 2, 25, 11, 30, 0).astimezone(timezone.utc)
            })
            club.add_event(
                start_date=datetime(2022, 2, 28, 11, 30, 0),
                end_date=datetime(2022, 2, 28, 12, 30, 0),
                summary="Test Event 2",
                desc="Testing Testing 3 4 5 6",
                recurrence_rule={
                    'freq': 'daily',
                    'interval': 1,
                    'until': datetime(2022, 3, 22, 0, 0, 0).astimezone(timezone.utc)
                }
            )
            database.session.commit()

        test_announcements = define_relational_test_data()

        register_admin_user()
        admin_id = User.query.filter_by(email="admin@" + accounts.fcs_suffix).first().id
        for club in test_clubs:
            database.session.add(Member(user_id=admin_id, club_id=club.id, isLeader=True))
            database.session.commit()
        
        for announcement in test_announcements:
            db.session.add(announcement)
            db.session.commit()


def register_admin_user():
    # Ask Sean what this is de-hashed
    pw_hash = b'$2b$12$HDFalMQSEb3vbifqn5pvUOKv4Q/S2JriwQ78STfaBLZUZSVdCFmmG'
    # Add user data to user table
    admin_email = "admin@" + accounts.fcs_suffix
    account = Account.query.filter_by(email=admin_email).first()
    db.session.add(User(account.id, "Admin", "User", admin_email, pw_hash))
    db.session.commit()
