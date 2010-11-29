#!/usr/bin/python
#viewing support functions

import cgi,dbconnection

class viewtools:
	dbconnection = None
	def __init__(this):
		this.dbconnection = dbconnection.dbconnection()
		data = cgi.FieldStorage()
		print 'Content-type:text/html\n'
		print 'hi'
		if data.has_key('roleid') and data.has_key('itemid'): #set roleid of itemid to data['roleid']
			this.dbconnection.setrole(data['itemid'].value,data['roleid'].value)
viewtools()