#!/usr/bin/python

import dbconnection,cgi,time

#views to display data
class view:
	dbconnection = None
	html = None
	def __init__(this):
		#testing only
		print "Content-type: text/html\n"
		
		this.dbconnection = dbconnection.dbconnection()
		this.html = []
		#get parameters from GET
		getdata = cgi.FieldStorage()

		#get desired items from database
		dof = None
		dfor = None
		if getdata.has_key('of'):
			dof = getdata['of']
		if getdata.has_key('for'):
			dfor = getdata['for']
		items = this.dbconnection.getitems(dof,dfor)
		feedtypes = this.dbconnection.getfeedtypes()
		
		this.html += ["<div id='items'>"]
		for item in items:
			this.html += ["<div id='#item%s'>" %(item[0])]
			this.html += ["		<div id='header'>"]
		
			print item[5]
			this.html += ["			<img id='typeicon' src='../img/feedtype%s.gif' />" %(feedtypes[item[1]][0])]
			this.html += ["			<span id='title'>%s</span>"%(item[3])]
			this.html += ["			<a id='link' href='%s'>GO</a>" %(item[6])]
			itemtime = time.strftime("%I:%M%p - %b %d '%y",time.gmtime(float(item[7])))
			this.html += ["			<span id='time'>%s</span>" %(itemtime)]
			this.html += ["		</div>"]
			this.html += ["		<div id='body'>"]
			itemauthor = item[5].encode('utf-8')
			this.html += ["			<p>By %s on %s,</p>" %(itemauthor,itemtime)]
			itembody = item[4].encode('utf-8')
			this.html += ["			<p>%s</p>" %(itembody)]
			this.html += ["		</div>"]
			this.html += ["</div>"]
		this.html += ["</div>"]
		
		#testing only (should be return)
		html = []
		for line in this.html:
			html.append(repr(line))
		print '\n'.join(html)
		
#testing only
view()