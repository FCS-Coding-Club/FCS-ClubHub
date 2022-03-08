from datetime import datetime

# NOTHING THAT ACCESSES THE DATABASE SHOULD BE PUT IN THIS DICTIONARY
# CONSIDER THIS IS A THREAT
render_functions = {
    "today": datetime.today(),
    "current_month": datetime.today().strftime('%B'),
    "current_year": datetime.today().strftime('%Y')
}