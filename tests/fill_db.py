import sqlite3

# This script creates a database with dummy data for testing purposes. Run this before running run.py

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
cur.execute("""
INSERT INTO users (fname, lname, email)
VALUES 
    ("John", "Smith", "johnsemail@friendscentral.org"),
    ("Jane", "Doe", "janesemail@friendscentral.org"),
    ("Lorem", "Ipsum", "latingibberish@friendscentral.org");
""")

con.commit()
con.close()