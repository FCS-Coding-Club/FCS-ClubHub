import bcrypt
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
def fill_with_test_data(db, ctx):
    with ctx:
        
        for club in test_clubs:
            db.session.add(club)
            db.session.commit()
        
        test_announcements = define_relational_test_data()
        
        register_admin_user()

        for announcement in test_announcements:
            db.session.add(announcement)
            db.session.commit()

def register_admin_user():
    pw_hash = b'$2b$12$HDFalMQSEb3vbifqn5pvUOKv4Q/S2JriwQ78STfaBLZUZSVdCFmmG'
    # Add user data to user table
    admin_email = "admin@"+accounts.fcs_suffix
    account = Account.query.filter_by(email=admin_email).first()
    db.session.add(User(account.id, "Admin", "User", admin_email, pw_hash))
    db.session.commit()