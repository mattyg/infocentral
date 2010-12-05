#!/usr/bin/python
#dbconnection

import sqlite3,datetime,calendar,re,collections
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
			ititle = item['title']
			ibody = item['summary_detail']['value']
			iauthor = item['author']
			iurl = item['link']
			itimestamp = calendar.timegm(item['date_parsed'])
		elif feed[2] == 1:	#feed is gmail
			ititle = item['title']
			ibody = item['summary_detail']['value']
			iauthor = item['author_detail']['email']
			iurl = item['link']
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
		#escape data strings and strip whitespace
		ititle = this._escapequotes(ititle).strip()
		ibody = this._escapequotes(ibody).strip()
		iauthor = this._escapequotes(iauthor).strip()
		#remove img tags from data
		p = re.compile(r'<.*?>')
		ibody = p.sub('', ibody)
		#decode strings to unicode objects
		ititle = ititle.decode()
		ibody = ibody.decode()
		iauthor = iauthor.decode()
		#check if item is in db
		query = "SELECT id FROM items WHERE title=\"%s\" AND body=\"%s\"" %(ititle,ibody)
		try:
			result = this.cursor.execute(query)
		except Exception, e:
			print "exception",e,"</br>"
		res = this.cursor.fetchone()
		if res is not None and res is not "": #item is in db
			return False
		query = "INSERT INTO items (feedid,roleid,title,body,author,url,timestamp) VALUES (%i,%i,'%s','%s','%s','%s','%s')" %(feedid,roleid,ititle,ibody,iauthor,iurl,itimestamp)
		this.cursor.execute(query)
		this.connection.commit()
		return True
	
	def _escapequotes(this,str):
		#escape all quotes for string str
		newstr = str.replace('\\', '\\\\')
		newstr = newstr.replace('"', '\\"')
		newstr = newstr.replace("'", "\\'")
		return newstr
		
	#get items from type, for role
	def getitems(this,fromtype=None,forrole=None):
		if fromtype is not None and forrole is not None: #get items from a FEED TYPE for a ROLE
			fromtype = fromtype.value
			forrole = forrole.value
			#get all feed id's w/ type=getdata['of']
			feedidlist = this._getfeedidlist(fromtype)
			#get all items with feedid in list and roleid=getdata['for']
			query = "SELECT * FROM items WHERE feedid in (%s) AND roleid=%s ORDER BY timestamp DESC" %(feedidlist,forrole)
			this.cursor.execute(query)
			return this.cursor.fetchall()
		elif fromtype is not None: #get items from a FEED TYPE
			fromtype = fromtype.value
			feedlist = this._getfeedidlist(fromtype)
			#get all items with feedid in list
			query = "SELECT * FROM items WHERE feedid in (%s) ORDER BY timestamp DESC" %(feedlist)
			this.cursor.execute(query)
			return this.cursor.fetchall()
		elif forrole is not None: #get items for a ROLE
			forrole = forrole.value
			#get all items with roleid=getdata['for']
			query = "SELECT * FROM items WHERE roleid=%s ORDER BY timestamp DESC" %(forrole)
			this.cursor.execute(query)
			return this.cursor.fetchall()
	
	def _getfeedidlist(this,fromtype):
		#get all feed id's w/ type=getdata['of']
		if str(fromtype) == '-1':
			param = ""
		else:
			param = "WHERE type=%s" %(fromtype)
		query = "SELECT id FROM feeds %s" %(param)
		this.cursor.execute(query)
		res = this.cursor.fetchall()
		feeds = []
		for feed in res:
			feeds.append(str(feed[0]))
		return ','.join(feeds)
		
	def getfeedtypes(this):
		query = "SELECT id,type FROM feeds"
		this.cursor.execute(query)
		feedtypes = this.cursor.fetchall()
		typesdict = collections.defaultdict(list)
		for feedid,typeid in feedtypes:
			typesdict[feedid].append(typeid)
		return typesdict
	
	def getroles(this,userid):
		query = "SELECT * FROM roles WHERE userid=%s ORDER BY position ASC" %(userid)
		this.cursor.execute(query)
		return this.cursor.fetchall()
	
	def setrole(this,itemid,roleid):
		query = "UPDATE items SET roleid=%s WHERE id=%s" %(roleid,itemid)
		this.cursor.execute(query)
		this.connection.commit()
	
	def removerole(this,roleid):
		query = "DELETE FROM roles WHERE id=%s" %(roleid)
		this.cursor.execute(query)
		query = "UPDATE items SET roleid=-1 WHERE roleid=%s" %(roleid)
		this.cursor.execute(query)
		this.connection.commit()
		
	def addrole(this,userid,name,color):
		query = "INSERT INTO roles (userid,name,color) VALUES (%s,'%s','%s')" %(userid,name,color)
		this.cursor.execute(query)
		lrid = this.cursor.lastrowid
		this.connection.commit()
		return lrid
		
	def addattrrole(this,roleid,attrdata): #attrdata = [] of strings, each string is attr=value or attr=%value%
		query = "INSERT INTO attrroles (roleid,attr,value) VALUES (%s,'%s','%s')" %(roleid,attrdata[0],attrdata[1])
		this.cursor.execute(query)
		this.connection.commit()
	
	def editroleposition(this,roleid,roleposition):
		query = "UPDATE roles SET position=%s WHERE id=%s" %(roleposition,roleid)
		this.cursor.execute(query)
		this.connection.commit()