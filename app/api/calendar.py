import calendar
import json
from flask import Blueprint, request
from flask_login import login_required, current_user
from time import sleep

mod = Blueprint('calendar', __name__, url_prefix='/api/calendar')

def gen_calendar_json(month, year):
    mr = calendar.monthrange(year, month)
    cal_dictionary = {}
    for row in range(0, 6):
        for col in range(0, 7):
            cal_dictionary[f"{row}{col}"] = {"day": "", "isMeeting": False}
    current_row = 0
    for day in range(1,mr[1]+1):
        weekday = calendar.weekday(int(year), int(month), day)
        cal_dictionary[f"{current_row}{weekday}"]["day"] = day
        # TODO: Add isMeeting database query
        if weekday == 6: current_row += 1
    return json.dumps(cal_dictionary)

@mod.route("/month_json")
@login_required
def month_json():
    month = request.args.get("month", 1, type=int)
    year = request.args.get("year", 1970, type=int)
    return gen_calendar_json(month, year)