import sqlite3

con = sqlite3.connect('clubhub.db')

cur = con.cursor()

cur.execute("DROP TABLE IF EXISTS users")
# Table Creation Code
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
INSERT INTO users (user_id, fname, lname, email)
VALUES 
    (1, "John", "Smith", "johnsemail@friendscentral.org"),
    (2, "Jane", "Doe", "janesemail@friendscentral.org"),
    (3, "Lorem", "Ipsum", "latingibberish@friendscentral.org");
""")

con.commit()
con.close()