#!/usr/bin/python
#dbconnection

import sqlite3

class dbconnection:
	cursor = None
	connection = None
	
	def __init__(this):
		this.connection = sqlite3.connect('../storage.db')
		this.cursor = this.connection.cursor()
		
	def getfeedurls(this): #get all feed urls, return in array
		query = "SELECT * FROM feeds"
		this.cursor.execute(query)
		return this.cursor.fetchall()
		
	def additem(this,feedid,roleid,name,content,timestamp):
		query = "INSERT INTO items (feedid,roleid,name,content,timestamp) VALUES ('%s','%s','%s','%s','%s')" %(feedid,roleid,name,content,timestamp)
		#this.cursor.execute(query)