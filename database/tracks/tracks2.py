# This application will read an iTunes export file in XML 
# and produce a properly normalized database with this  structure
import xml.etree.ElementTree as ET
import sqlite3 as sq
fname=input("Enter file name: ")
if len(fname)<1:
	fname="Library.xml"
try:
	data=open(fname).read()
except:
	print("Invalid file name")
	quit()
conn=sq.connect("tracks2.sqlite")
cur=conn.cursor()
cur.execute('''DROP TABLE IF EXISTS Artist;''')
cur.execute('''DROP TABLE IF EXISTS Album''')
cur.execute("DROP TABLE IF EXISTS Track;")
cur.execute("DROP TABLE IF EXISTS Genre;")
cur.execute('''CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
)''')
cur.execute('''CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
)''')
cur.execute('''CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
)''')
cur.execute('''CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
)''')

# define a function that could retieve value in the xml
def retrieve(trees,query):
	# trees is the part of the xml, and query is the vakues
	# you would like to retrieve
	found=False
	for child in trees:
		if found:
			return child.text
		if child.tag=='key' and child.text==query:
			found=True
	return None
tree=ET.fromstring(data)
all=tree.findall("dict/dict/dict")
for child in all:
	if retrieve(child,"Track ID") is None:
		continue
	name=retrieve(child,"Name")
	artist=retrieve(child,"Artist")
	album=retrieve(child,"Album")
	count=retrieve(child,"Play Count")
	rating=retrieve(child,"Rating")
	length=retrieve(child,"Total Time")
	genre=retrieve(child,"Genre")
	if name is None or artist is None or album is None or genre is None:
		continue
	print("name:",name,"\nartist:",artist,"\nalbum:",album,"\ncount:",count,
		"\nrating:",rating,"\nlength:",length,"\ngenre:",genre,
		"\n=========================================")
	cur.execute('''INSERT OR IGNOR
		E INTO Artist (name) VALUES (?)''',(artist,))
	cur.execute('SELECT id FROM Artist WHERE name = ? ', (artist,))
	artist_id = cur.fetchone()[0]
	cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id) 
        VALUES ( ?, ? )''',(album,artist_id))
	cur.execute('SELECT id FROM Album WHERE title = ?',(album,))
	album_id=cur.fetchone()[0]
	cur.execute('''INSERT OR IGNORE INTO Genre (name) VALUES (?)''',(genre,))
	cur.execute('SELECT id FROM Genre WHERE name = ? ',(genre,))
	genre_id = cur.fetchone()[0]
	cur.execute('''INSERT OR REPLACE INTO Track
        (title, album_id, genre_id,len, rating, count) 
        VALUES ( ?, ?, ?, ?, ? ,?)''', 
        ( name, album_id, genre_id,length, rating, count ) )
	conn.commit()
cur.close()