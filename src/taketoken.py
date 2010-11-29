#!/usr/bin/python
#taketoken

import cgi,urllib,urllib2,gdata.calendar,gdata.calendar.service

data = cgi.FieldStorage()

token = data['token'].value
print "Content-type: text/html\n"
#print token
gcal = gdata.caldendar.service.CalendarService()
gcal.UpgradeToSessionToken(token) 
#print "Authorization: AuthSub token=\"%s\"" %(token)
#res = urllib2.Request('https://www.google.com/accounts/AuthSubSessionToken',None,authtoken)
#word =urllib2.urlopen(res)
#print word