from app.models.dbutils import load_club
import calendar
from datetime import datetime
from icalendar import Event
from icalevents import icalparser
import jicson
import json
from flask import abort, Blueprint, request
from flask_login import login_required

mod = Blueprint('calendar', __name__, url_prefix='/api/calendar')


def gen_calendar_json(club, month, year):
    # Variable Init
    mr = calendar.monthrange(year, month)
    cal_dictionary = {}
    ical = club.calendar
    # Fill cal_dictionary with empty strings for day value
    for row in range(0, 6):
        for col in range(0, 7):
            cal_dictionary[f"{row}{col}"] = {"day": ""}
    # Count variable for calendar row
    current_row = 0
    # For every day in the month
    for day in range(1, mr[1] + 1):
        # Set the corresponding entry in the table to the day
        weekday = calendar.weekday(int(year), int(month), day)
        cal_dictionary[f"{current_row}{weekday}"]["day"] = day
        # Parse the calendar for events
        events = icalparser.parse_events(ical, datetime(year, month, day, 0, 0, 0),
                                         datetime(year, month, day, 23, 59, 59))
        # Sort events by start time
        events.sort(key=lambda e: e.start)
        # If there is an event, set isMeeting to true
        cal_dictionary[f"{current_row}{weekday}"]["isMeeting"] = bool(events)
        # If there are events... fill in data about events for the modals
        if events:
            cal_dictionary[f"{current_row}{weekday}"]["names"] = [e.summary for e in events]
            cal_dictionary[f"{current_row}{weekday}"]["descriptions"] = [e.description for e in events]
            # dtstart and dtend in format: 10:30 - 11:30 for modal presentation
            formatted_times = [f"{e.start.strftime('%H:%M')} - {e.end.strftime('%H:%M')}" for e in events]
            print(formatted_times)
            cal_dictionary[f"{current_row}{weekday}"]["times"] = formatted_times
            # Used for frontend API calls to "/api/calendar/meeting"
            cal_dictionary[f"{current_row}{weekday}"]["uids"] = [e.uid for e in events]
        else:
            # Otherwise, fill with empty arrays
            cal_dictionary[f"{current_row}{weekday}"]["names"] = []
            cal_dictionary[f"{current_row}{weekday}"]["descriptions"] = []
            cal_dictionary[f"{current_row}{weekday}"]["times"] = []
            cal_dictionary[f"{current_row}{weekday}"]["uids"] = []
        # If the day is a sunday, move to the next row
        if weekday == 6:
            current_row += 1
    # Return calendar in json format
    return json.dumps(cal_dictionary)


@mod.route("/month_meetings")
@login_required
def month_meetings():
    club_id = request.args.get("club")
    club = load_club(club_id)
    if club is not None:
        month = request.args.get("month", 1, type=int)
        year = request.args.get("year", 1970, type=int)
        if year <= 1 or month < 1 or month > 12:
            return abort(400)
        return gen_calendar_json(club, month, year)
    return abort(404)


# Returns json of event by ID
# TODO: The jicson library doesn't format rrule as object, 
# so we could either format that here, or parse it in the JS
@mod.route("/meeting")
@login_required
def meeting():
    club_id = request.args.get("club")
    event_uid = request.args.get("uid")
    club = load_club(club_id)
    if club is None:
        return abort(404)
    event: Event = club.get_event_by_uid(event_uid)
    if event is None:
        return abort(404)
    return jicson.fromText(event.to_ical().decode('utf-8'))
