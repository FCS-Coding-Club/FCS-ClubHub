import sqlite3

con = sqlite3.connect('clubhub.db')

cur = con.cursor()

cur.execute("DROP TABLE IF EXISTS users")
# Table Creation Code
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    fname TEXT NOT NULL,
    lname TEXT NOT NULL,
    email TEXT NOT NULL
);
""")

'''
    Filling the DB with dummy data for now.
    Eventually, we will have the extracted student data
    imported into the db through a function that the backend
    team creates.
'''
cur.execute("""
INSERT INTO users (fname, lname, email)
VALUES 
    ("John", "Smith", "johnsemail@friendscentral.org"),
    ("Jane", "Doe", "janesemail@friendscentral.org"),
    ("Lorem", "Ipsum", "latingibberish@friendscentral.org");
""")

con.commit()
con.close()