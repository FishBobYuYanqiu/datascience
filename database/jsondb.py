# This application will read roster data in JSON format, 
# parse the file, and then produce an SQLite database that 
# contains a User, Course, and Member table and populate 
# the tables from the data file
import json
import sqlite3
fname=input("Enter file name:")
if len(fname)<1:
	fname="roster_data.json"
try:
	data=open(fname).read()
except:
	print("Invald file name")
conn=sqlite3.connect("roster.sqlite")
cur=conn.cursor()
cur.executescript('''DROP TABLE IF EXISTS User;
	DROP TABLE IF EXISTS Member;
	DROP TABLE IF EXISTS Course;
	CREATE TABLE User (id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Course (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
)
''')
js=json.loads(data)
for datum in js:
	name=datum[0]
	course=datum[1]
	cur.execute("INSERT OR IGNORE INTO User (name) VALUES (?)",(name,))
	cur.execute("INSERT OR IGNORE INTO Course (title) VALUES (?)",(course,))
	cur.execute("SELECT id FROM User WHERE name=?",(name,))
	user_id=cur.fetchone()[0]
	cur.execute("SELECT id FROM Course WHERE title=?",(course,))
	course_id=cur.fetchone()[0]
	print("======================================")
	print("User:",name,"\nuser_id:",user_id)
	print("Course:",datum[1],"\ncourse_id:",course_id)
	print("role:",datum[2])
	cur.execute("INSERT OR REPLACE INTO Member (user_id,course_id,role) VALUES (?,?,?)",(user_id,course_id,datum[2]))
	conn.commit()
cur.close()