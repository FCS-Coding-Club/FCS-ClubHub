from .models import Account, db

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