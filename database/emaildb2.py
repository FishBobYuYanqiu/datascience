# This application will read the mailbox data (mbox.txt) 
# count up the number email messages per organization 
# (i.e. domain name of the email address) using a database 
# with the following schema to maintain the counts.

# CREATE TABLE Counts (org TEXT, count INTEGER)
import sqlite3 as sq
fname=input("Enter file name: ")
if len(fname)<1:
	fname="mbox.txt"
try:
	handle=open(fname)
except:
	print("Invalid file name")
	quit()
conn=sq.connect("emaildb2.sqlite")
cur=conn.cursor()
cur.execute('''DROP TABLE IF EXISTS Counts''')
cur.execute('''CREATE TABLE Counts(org TXET,count INTEGER)''')
for line in handle:
	if not line.startswith("From:"):
		continue
	word=line.split()
	email=word[1]
	org=email.split("@")[1]
	cur.execute('''SELECT * FROM Counts WHERE org=?''',(org,))
	row=cur.fetchone()
	if row is None:
		cur.execute('''INSERT INTO Counts (org,count) VALUES (?,1)''',(org,))
	else:
		cur.execute("UPDATE Counts SET count=count+1 WHERE org=?",(org,))
	conn.commit()
cur.close()