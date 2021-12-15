import bcrypt
from .models import User, Club, Member, Announcement
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
        
        for announcement in test_announcements:
            db.session.add(announcement)
            db.session.commit()