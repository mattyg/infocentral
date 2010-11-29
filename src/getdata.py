#!/usr/bin/python
#get data input

import urllib,urllib2,feedparser,dbconnection,gdata.calendar,gdata.calendar.service,sys

class getdata:
	dbconnection = None
	
	def __init__(this):
		this.dbconnection = dbconnection.dbconnection()
		
		#for testing only:
		print "Content-type: text/html\n"
		print "<html><head><meta http-equiv='Content-Type' content=text/html; charset=UTF-8/></head><body>"		
		this.update()
		print "</body></html>"
		
	def update(this): #poll all data feeds, add new data to db
		#1 - get data feed urls from db
		feeds = this.dbconnection.getfeeds()
		#2 - check data feeds for new items
		feeddata = []
		for feed in feeds:
			if feed[2] == 2:	#feed is gcal
				try:
					#2.1 - auth to gcal
					gcal = gdata.calendar.service.CalendarService(feed[3],feed[4])
					gcal.ProgrammaticLogin()
					#2.2 - get items	
					items =  gcal.GetCalendarEventFeed(feed[1])
					for item in items.entry:
						#print item
						#for testing only:
						roleid = 2 					
						#do role analysis on new item
						#roleid = this.analysis...
						#add item to db
						#print item.title,item.link,item.when[0].start_time,item.link[0],"</br></br>"
						isnew = this.dbconnection.additem(feed,roleid,item)
						if isnew is False:
							print "broken1","</br>"
							break
				except gdata.service.BadAuthentication, e:
					print "Authentication error logging in: %s" % e
					return
				except Exception, e:
					print "Error: %s" % e
					return
			else:	#feed is regular RSS/ATOM
				if str(feed[3]).strip() is not "" and feed[3] is not None: #if feed requires auth, modify url with auth
					feedurl = feed[1].replace("://","://%s:%s@" %(feed[3],feed[4]))
					feeddata = feedparser.parse(feedurl)
				else:
					feeddata = feedparser.parse(feed[1])
				if feeddata['items']: #if there are new entries
					for item in feeddata['items']:
						#for testing only:
						roleid = 2 					
						#do role analysis on new item
						#roleid = this.analysis...
						#add item to db
						#print item['title'],item['summary_detail']['value'].encode('utf-8'),"</br></br>"
						isnew = this.dbconnection.additem(feed,roleid,item)
						if isnew is False:
							print 'broken2',"</br>"
							break
getdata()