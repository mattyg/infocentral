#!/usr/bin/python
import dbconnection,Cookie,os
#role analysis

class analysis:
	dbconnection = None
	
	def __init__(this):
		this.dbconnection = dbconnection.dbconnection()
		
	def analyze(this,userid,itemid): 
		item = this.dbconnection.getitem(itemid)
		feedrole = this.dbconnection.getfeedrole(item[1])
		if feedrole is not None: #this feed has a specified role
			#set item to specified role
			this.dbconnection.setrole(itemid,feedrole[2])
		else:
			#attempt to determine item role
			roleids = this.dbconnection.getroleids(userid)
			roleids = str(",".join(str(item) for item in roleids))
			attrroles = this.dbconnection.getattrroles(roleids)
			for key in attrroles:
				if (str(key[3]) in str(item[3])) or (str(key[3]) in str(item[4])) or (str(key[3]) in str(item[5])) or (str(key[3]) in str(item[6])):
					itemid = str(item[0])
					roleid = str(key[1])
					this.dbconnection.setrole(itemid,roleid)