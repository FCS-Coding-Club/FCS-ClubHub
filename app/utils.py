from datetime import datetime
from icalendar import Calendar, Timezone

# NOTHING THAT ACCESSES THE DATABASE SHOULD BE PUT IN THIS DICTIONARY
# CONSIDER THIS IS A THREAT
render_functions = {
    "today": datetime.today(),
    "current_month": datetime.today().strftime('%B'),
    "current_year": datetime.today().strftime('%Y')
}

def gen_barebones_ical(name, desc):
    cal = Calendar()
    cal.add('prodid', '-//FCCC//FCS ClubHub//')
    cal.add('version', '2.0')
    cal.add('name', name)
    cal.add('summary', desc)
    return cal.to_ical().decode('utf-8')
