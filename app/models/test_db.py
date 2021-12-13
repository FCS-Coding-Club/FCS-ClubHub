import bcrypt
from .models import User, Club, Member, Announcement
# This script configures the database with dummy data for testing purposes

# Hashing function so that the users table has the passwords in plaintext
def dbhash(password):
    return bcrypt.hashpw(password.encode(),bcrypt.gensalt())


# Test Data for dev purposes. 
test_users = [
    User("John", "Smith", "johnsemail@friendscentral.org", dbhash("johntest")),
    User("Jane", "Doe", "janesemail@friendscentral.org", dbhash("janetest")),
    User("Lorem", "Ipsum", "latingibberish@friendscentral.org", dbhash("loremtest")),
    User("Lord", "Farquaad", "kingfromshrek@friendscentral.org", dbhash("lordtest")),
    User("Admin", "User", "admin@friendscentral.org", dbhash("password123"), admin=True)
]

test_clubs = [
    Club("Coding Club", "The Creators of this website"),
    Club("Cooking Club", "Join if you love food"),
    Club("Nature Club", "We go on nature walks and stuff"),
]

# These need to be defined after the clubs are serialized in the database
def define_relational_test_data():
    test_members = [
            Member(test_users[0].id, test_clubs[0].id, True),
            Member(test_users[0].id, test_clubs[1].id, False),
            Member(test_users[1].id, test_clubs[1].id, True),
            Member(test_users[0].id, test_clubs[2].id, False),
            Member(test_users[1].id, test_clubs[2].id, False),
            Member(test_users[2].id, test_clubs[2].id, True),
            Member(test_users[3].id, test_clubs[2].id, True),
        ]

    test_announcements = [
            Announcement(test_clubs[0].id, "Meeting Every Two Weeks", "Come to the meeting, it'll be fun!"),
            Announcement(test_clubs[1].id, "Meeting Today", "Meeting today! We will be using a toaster."),
            Announcement(test_clubs[1].id, "The Toaster Incident", "Remember everyone, nothing happened."),
        ]
    return test_members, test_announcements

# Function to add all test data
def fill_with_test_data(db, ctx):
    with ctx:
        for user in test_users:
            db.session.add(user)
            db.session.commit()
        
        for club in test_clubs:
            db.session.add(club)
            db.session.commit()

        test_members, test_announcements = define_relational_test_data()

        for member in test_members:
            db.session.add(member)
            db.session.commit()
        
        for announcement in test_announcements:
            db.session.add(announcement)
            db.session.commit()