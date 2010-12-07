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
			print ",".join(roleids)
			attrroles = this.dbconnection.getattrroles(roleids)
			for key in attrroles:
				if (key[4] in item[3]) or (key[4] in item[4]) or (key[4] in item[5]) or (key[4] in item[6]):
					itemid = item[0]
					roleid = keys[1]
					this.dbconnection.setrole(this,itemid,roleid)
				else:
					itemid = item[0]
					roleid = -1
					this.dbconnection.setrole(this,itemid,roleid)