#!/usr/bin/python
#dbconnection

import sqlite3,datetime,calendar,re,collections,time
from dateutil import parser

class dbconnection:
	cursor = None
	connection = None
	
	def __init__(this):
		this.connection = sqlite3.connect('../storage.db')
		this.cursor = this.connection.cursor()
		
	def getfeeds(this,userid): #get all feeds, return in array
		query = "SELECT * FROM feeds WHERE userid=%s" %(userid)
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
		if res is not None and res is not "": #item is already in db
			return False
		query = "INSERT INTO items (feedid,roleid,title,body,author,url,timestamp) VALUES (%i,%i,'%s','%s','%s','%s','%s')" %(feedid,roleid,ititle,ibody,iauthor,iurl,itimestamp)
		this.cursor.execute(query)
		this.connection.commit()
		return this.cursor.lastrowid
	
	def _escapequotes(this,str):
		#escape all quotes for string str
		newstr = str.replace('\\', '\\\\')
		newstr = newstr.replace('"', '\\"')
		newstr = newstr.replace("'", "\\'")
		return newstr
		
	def getitem(this,itemid):
		query = "SELECT * FROM items WHERE id=%s" %(itemid)
		this.cursor.execute(query)
		return this.cursor.fetchone()
		
	#get items from type, for role
	def getitems(this,userid,fromtype=None,forrole=None,orderby=None,recent=None):
		tempitems = None
		if orderby != 'role':
			orderby = 'items.timestamp'
		else:
			orderby = 'roles.position'
		if fromtype is not None and forrole is not None: #get items from a FEED TYPE for a ROLE
			fromtype = fromtype.value
			forrole = forrole.value
			#get all feed id's w/ type=getdata['of']
			feedidlist = this._getfeedidlist(userid,fromtype)
			#get all items with feedid in list and roleid=getdata['for']
			query = "SELECT * FROM items WHERE feedid in (%s) AND roleid=%s ORDER BY timestamp DESC" %(feedidlist,forrole)
			this.cursor.execute(query)
			tempitems = this.cursor.fetchall()
		elif fromtype is not None: #get items from a FEED TYPE
			fromtype = fromtype.value
			feedlist = this._getfeedidlist(userid,fromtype)
			#get all items with feedid in list
			query = "SELECT * FROM items WHERE feedid in (%s) ORDER BY timestamp DESC" %(feedlist)
			this.cursor.execute(query)
			tempitems = this.cursor.fetchall()
		elif forrole is not None: #get items for a ROLE
			forrole = forrole.value
			#get all items with roleid=getdata['for']
			feedlist = this._getfeedidlist(userid,'-1')
			query = "SELECT * FROM items WHERE feedid in (%s) roleid=%s ORDER BY timestamp DESC" %(feedlist,forrole)
			this.cursor.execute(query)
			tempitems = this.cursor.fetchall()
		#get subarray of items during or later than today
		today = datetime.datetime.utcnow().timetuple()
		basetoday = time.struct_time((today[0],today[1],today[2],0,0,0,today[6],today[7],today[8]))
		epochtoday = time.mktime(basetoday)
		items = []
		if recent is None or int(recent) == 0: #get items with time >= currenttime 
			for it in tempitems:
				if int(it[7]) >= epochtoday: #if item time is >= today
					items.append(it)
				else:
					break
		else: #get items with time >= currenttime + drecent items
			counter = 0
			for it in tempitems:
				if int(it[7]) >= epochtoday or counter < int(recent): #if item time is >= today
					items.append(it)
					counter = counter+1
				else:
					break
		return items

	def _getfeedidlist(this,userid,fromtype):
		#get all feed id's w/ type=getdata['of']
		if str(fromtype) == '-1':
			param = "WHERE userid=%s" %(userid)
		else:
			param = "WHERE type=%s AND userid=%s" %(fromtype,userid)
		query = "SELECT id FROM feeds %s" %(param)
		this.cursor.execute(query)
		res = this.cursor.fetchall()
		feeds = []
		for feed in res:
			feeds.append(str(feed[0]))
		return ','.join(feeds)
		
	def getfeedrole(this,feedid):
		query = "SELECT * FROM feedroles WHERE feedid=%s" %(feedid)
		this.cursor.execute(query)
		return this.cursor.fetchone()
		
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
	
	def getroleids(this,userid):
		roles = this.getroles(userid)
		ids = []
		for r in roles:
			ids.append(r[0])
		return ids
		
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
		
	def removefeed(this,feedid):
		query = "DELETE FROM feeds WHERE id=%s" %(feedid)
		this.cursor.execute(query)
		this.connection.commit()
		
	def addfeed(this,userid,feedtype,url,roleid,secureuser,securepass):
		if int(feedtype) == 2: #feed is gcal
			loc = url.find('google.com')
			if loc != -1:
				url = url[loc+10:]
		query = "INSERT INTO feeds (userid,url,type,secureuser,securepass) VALUES (%s,'%s',%s,'%s','%s')" %(userid,url,feedtype,secureuser,securepass)
		print query
		this.cursor.execute(query)
		feedid = this.cursor.lastrowid
		if roleid is not "":
			query = "INSERT INTO feedroles (feedid,roleid) VALUES (%s,%s)" %(feedid,roleid)
			this.cursor.execute(query)
		this.connection.commit()