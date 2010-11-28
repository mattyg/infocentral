#!/usr/bin/python
#dbconnection

import sqlite3,datetime,calendar,re
from dateutil import parser

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
			ititle = item.title.text
			ibody = ititle
			iauthor = ""
			iurl = item.link[0].href
			#get timestamp
			itimestamp = item.when[0].start_time #returns xs:datetime
			dt = parser.parse(itimestamp) #returns python datetime
			itimestamp = calendar.timegm(dt.timetuple()) #returns epoch
		#escape data strings
		ititle = this._escapequotes(ititle)
		ibody = this._escapequotes(ibody)
		iauthor = this._escapequotes(iauthor)
		#remove img tags from data
		p = re.compile(r'<.*?>')
		ibody = p.sub('', ibody)
		#check if item is in db
		query = "SELECT id FROM items WHERE title=\"%s\" AND body=\"%s\"" %(ititle,ibody)
		print query,"</br>"
		try:
			result = this.cursor.execute(query)
		except Exception, e:
			print "exception",e,"</br>"
		res = this.cursor.fetchone()
		if res is not None and res is not "": #item is in db
			return False
		query = "INSERT INTO items (feedid,roleid,title,body,author,url,timestamp) VALUES (%i,%i,'%s','%s','%s','%s','%s')" %(feedid,roleid,ititle,ibody,iauthor,iurl,itimestamp)
		print query,"</br>"
		this.cursor.execute(query)
		this.connection.commit()
		return True
	
	def _escapequotes(this,str):
		#escape all quotes for string str
		newstr = str.replace('\\', '\\\\')
		newstr = newstr.replace('"', '\\"')
		newstr = newstr.replace("'", "\\'")
		return newstr