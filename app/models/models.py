from datetime import datetime
from typing import Any

from dateutil import rrule
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from icalendar import Calendar, Event, vDatetime
import uuid
from app.utils import gen_barebones_ical

import json

db = SQLAlchemy()

# All allowed keys for an icalendar VEVENT
date_keys = (
    'dtend',
    'dtstamp',
    'dtstart'
)
event_keys = date_keys + (
    'location',
    'name',
    'rrule',
    'summary',
    'uid'
)


# Club Model
class Club(db.Model):
    __tablename__ = 'clubs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    desc = db.Column(db.Text, nullable=True)
    # This will be stored in iCal format
    calendar = db.Column(db.Text, nullable=False)
    verified = db.Column(db.Boolean, nullable=False)

    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        self.calendar = gen_barebones_ical(name, desc)
        self.verified = False

    def __repr__(self):
        return f'<Club {self.name}, id {self.id}>'

    # Add event to calendar
    def add_event(self, start_date: datetime, end_date: datetime,
                  summary: str, desc: str = "", recurrence_rule: rrule = None):
        # Create Event and fill in data
        e = Event()
        e.add('dtstart', start_date)
        e.add('dtend', end_date)
        e.add('dtstamp', datetime.now())
        e.add('uid', str(uuid.uuid4()))
        e.add('summary', summary)
        e.add('description', desc)
        # Recurrence Rule not required
        if recurrence_rule:
            e.add('rrule', recurrence_rule)
        # Parse calendar, add event, re-encode calendar to utf-8
        c = Calendar.from_ical(self.calendar)
        c.add_component(e)
        # Encode to UTF-8, add to database
        self.calendar = c.to_ical().decode('utf-8')

    # Edit calendar event
    def edit_event(self, uid: str, changes: dict):
        c = Calendar.from_ical(self.calendar)
        # Get event, copy event to mutate
        event = self.get_event_by_uid(uid, c)
        if not event:
            pass
        event_new = event
        # Change new event params according to changes dictionary
        for change_key in changes:
            if change_key in date_keys:
                event_new[change_key] = vDatetime(changes[change_key])
            elif change_key in event_keys:
                event_new[change_key] = changes[change_key]
        # Replace old event in parsed calendar with changed event
        c.subcomponents.remove(event)
        c.subcomponents.append(event_new)
        # Recompile to UTF-8 and enter data to SQL
        self.calendar = c.to_ical().decode('utf-8')

    # Returns events with name param
    def get_events_by_summary(self, summary: str, cal=None) -> list:
        # Calendar reference is needed for editing / removing
        if not cal:
            cal = Calendar.from_ical(self.calendar)
        # We're only using VEVENT so this works
        events = cal.subcomponents
        # Filter events by name
        event_filter = list(filter(lambda e: e['summary'] == summary, events))
        return event_filter

    # Returns event with uid param (UIDs shouldn't be duplicate)
    def get_event_by_uid(self, uid: str, cal=None):
        # Calendar reference is needed for editing / removing
        if not cal:
            cal = Calendar.from_ical(self.calendar)
        # We're only using VEVENT so this works
        events = cal.subcomponents
        # Filter events by uid
        event_filter = list(filter(lambda e: e['uid'] == uid, events))
        # Check for if the event with uid doesn't exist
        if len(event_filter) == 0:
            return None
        # Return the one event without the list
        return event_filter[0]

    # Remove Calendar Event
    def remove_event(self, uid: str):
        c = Calendar.from_ical(self.calendar)
        # Get event according to uid
        event = self.get_event_by_uid(uid, c)
        # Remove event
        c.remove(event)
        # Recompile to UTF-8 and enter data to SQL
        self.calendar = c.to_ical().decode('utf-8')


# Account Model (Whitelisted but Unclaimed)
class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(320), nullable=False, unique=True)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, name, grade, email, admin=False):
        self.name = name
        self.grade = grade
        self.email = email
        self.admin = admin


# User Model (Claimed)
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(db.Integer, db.ForeignKey(Account.id), nullable=False, unique=True)
    fname = db.Column(db.Text, nullable=False)
    lname = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(320), db.ForeignKey(Account.email), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)

    def __init__(self, account_id, fname, lname, email, password, admin=False):
        self.account_id = account_id
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = password
        self.admin = admin

    def __repr__(self):
        return f'<User {self.fname} {self.lname} - id {self.id}>'


# Club Member Model
class Member(db.Model):
    __tablename__ = 'members'
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False, primary_key=True)
    club_id = db.Column(db.Integer, db.ForeignKey(Club.id), nullable=False, primary_key=True)
    isLeader = db.Column(db.Boolean, nullable=False)

    def __init__(self, user_id, club_id, isLeader):
        self.user_id = user_id
        self.club_id = club_id
        self.isLeader = isLeader

    def __repr__(self):
        return f'<Club {"Leader" if self.isLeader else "Member"}, id {self.user_id}, club_id {self.club_id}>'


# Club Announcement Model
class Announcement(db.Model):
    __tablename__ = 'announcements'
    announcement_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    club_id = db.Column(db.Integer, db.ForeignKey(Club.id), nullable=False)
    title = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    # This will be added on construction of class
    time = db.Column(db.Text, nullable=False)

    def __init__(self, club_id, title, description):
        self.club_id = club_id
        self.title = title
        self.desc = description
        self.time = str(datetime.utcnow())

    def __repr__(self):
        return f'<Announcement: {self.title} - by {self.club_id}>'
