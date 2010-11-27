#!/usr/bin/python
#main page

import feedparser,urllib,urllib2,gdata.calendar,gdata.calendar.service,feedparser,datetime,calendar
from xml.etree.ElementTree import ElementTree


class index:
	def __init__(this):
		gcal = gdata.calendar.service.CalendarService('matt.gabrenya@gmail.com','fuckSchool')
		#link = gcal.GenerateAuthSubURL("http://localhost/src/taketoken.py","https://www.google.com/calendar/feeds/",0,1)
		#next = 'http://localhost/src/taketoken.py'
		#scope = 'http://www.google.com/calendar/feeds/'
		#secure = 0  # set secure=True to request secure AuthSub tokens
		#session = 1
		print "Content-type: text/html\n"
		try:
			gcal = gdata.calendar.service.CalendarService('matt.gabrenya@gmail.com','fuckSchool')
			gcal.ProgrammaticLogin()	
			items =  gcal.GetCalendarEventFeed('/calendar/feeds/matt.gabrenya@gmail.com/private/full')
			print items.__dict__
			print items.entry
			for item in items.entry:
				print item.title,item.link
			#print feedxml.__dict__,'</br>','</br>'
			#for feeditem in feedxml.entry:
			#	print feeditem.title,feeditem.when[0].start_time,feeditem.link[0],'</br></br>'
		except gdata.service.BadAuthentication, e:
			print "Authentication error logging in: %s" % e
			return
		except Exception, e:
			print "Error: %s" % e
			return
		#print "<a href='%s'>link</a>" %(link)
		# Unlike the other calls, extract_auth_sub_token_from_url() will create an AuthSubToken or SecureAuthSubToken object.
		# Use str(single_use_token) to return the token's string value.
index()
#if feedurl[1].has('.google.com') and authgoogle == False: #if feed is from google, authenticate google user
#	authgoogle = True
#	authvalues = {'Email':}
#	urllib.urlencode()
#	urllib2.urlopen('url','data')
#print str.find(str(feeds[-1]))

#checks if user is logged in
#logs user in
##authenticates google if user has it as feed
#>>> urldata = urllib.urlencode({'Email':'matt.gabrenya@gmail.com','Passwd':'fuckSchool','source':'infocentral','service':'cl'})
