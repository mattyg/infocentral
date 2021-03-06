#!/usr/bin/python
#viewing support functions

import cgi,dbconnection,Cookie,os

class viewtools:
	dbconnection = None
	def __init__(this):
		this.dbconnection = dbconnection.dbconnection()
		data = cgi.FieldStorage()
		print "Content-type: text/html\n"
		if data.has_key('do'):
			if data.has_key('roleid') and data.has_key('itemid') and data['do'].value == 'setrole': #set roleid of itemid to data['roleid']
				this.dbconnection.setrole(data['itemid'].value,data['roleid'].value)
			elif data.has_key('roleid') and data['do'].value == 'removerole': #remove role id and set all roles with that id to -1 (none)
				this.dbconnection.removerole(data['roleid'].value)
			elif data['do'].value == 'addrole': #add role
				#get user id of currently logged in user
				try:
					cookies = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
					userid = cookies['userid'].value
				except:
					return
				#add role 
				roleid = this.dbconnection.addrole(userid,data['rolename'].value,data['rolecolor'].value)
				#add attrroles
				attrdata = []
				for counter in range(10):
					if data.has_key('attr'+str(counter)):
						#turn params into array
						if data['attr'+str(counter)].value == "title" or data['attr'+str(counter)].value == "body" or data['attr'+str(counter)].value == "author": 
							if data['comp'+str(counter)].value == "includes":
								#value = "%"+data['val'+str(counter)].value+"%" fuck it
								value = data['val'+str(counter)].value
							elif data['comp'+str(counter)].value == "equals":
								value = data['val'+str(counter)].value
							print roleid,(data['attr'+str(counter)].value,value)
							this.dbconnection.addattrrole(roleid,(data['attr'+str(counter)].value,value))
					else:
						break
			elif data['do'].value == 'editpositions': #edit role positions (order)
				this.dbconnection.editroleposition(data['roleid'].value,data['roleposition'].value)
			elif data['do'].value == 'removefeed': #remove feed
				this.dbconnection.removefeed(data['feedid'].value)
			elif data['do'].value == 'addfeed': #add feed
				#userid,feedtype,url,roleid,secureuser,securepass
				secureuser = ""
				securepass = ""
				roleid = ""
				if data.has_key('secureuser'):
					secureuser = data['secureuser'].value
				if data.has_key('securepass'):
					securepass = data['securepass'].value
				if data.has_key('roleid'):
					roleid = data['roleid'].value
				this.dbconnection.addfeed(data['userid'].value,data['feedtype'].value,data['feedurl'].value,roleid,secureuser,securepass)
viewtools()