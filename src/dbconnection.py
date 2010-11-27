#!/usr/bin/python
#dbconnection

import sqlite3,datetime,calendar

class dbconnection:
	cursor = None
	connection = None
	
	def __init__(this):
		this.connection = sqlite3.connect('../storage.db')
		this.cursor = this.connection.cursor()
		
	def getfeeds(this): #get all feeds, return in array
		query = "SELECT * FROM feeds"
		this.cursor.execute(query)
		return this.cursor.fetchall()
		
	def additem(this,feed,roleid,item):
		#determine feed type and get data
		feedid = feed[0]
		if feed[2] == 0:	#feed is a normal RSS/ATOM
			ititle = item['title'].encode('utf-8')
			ibody = item['summary_detail']['value'].encode('utf-8')
			iauthor = item['author'].encode('utf-8')
			iurl = item['link'].encode('utf-8')
			itimestamp = calendar.timegm(item['date_parsed'])
		elif feed[2] == 1:	#feed is gmail
			ititle = item['title'].encode('utf-8')
			ibody = item['summary_detail']['value'].encode('utf-8')
			iauthor = item['author_detail']['email'].encode('utf-8')
			iurl = item['link'].encode('utf-8')
			itimestamp = calendar.timegm(item['date_parsed'])
		elif feed[2] == 2:	#feed is gcal	
			ititle = item.title
			ibody = item.title
			iauthor = ""
			iurl = item.link[0]
			itimestamp = item.when[0].start_time
			print 'ey1'
		#check if item is in db
		print ititle,ibody,"</br>"
		query = "SELECT id FROM items WHERE title=\"%s\" AND body=\"%s\"" %(ititle,ibody)
		result = this.cursor.execute(query)
		res = this.cursor.fetchone()
		print 'ey2:',res,"</br>"
		if res is not None and res is not "": #item is in db
			return False
		query = "INSERT INTO items (feedid,roleid,title,body,author,url,timestamp) VALUES (%i,%i,'%s','%s','%s','%s','%s')" %(feedid,roleid,ititle,ibody,iauthor,iurl,itimestamp)
		this.cursor.execute(query)
		this.connection.commit()
		return True