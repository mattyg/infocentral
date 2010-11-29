#!/usr/bin/python

import dbconnection,cgi,time

#views to display data
class view:
	dbconnection = None
	html = None
	def __init__(this):
		this.dbconnection = dbconnection.dbconnection()
		this.html = []
		this.html += ["Content-type: text/html\n"]
		this.html += ['''<html>
		<head>
			
			<link rel='stylesheet' type='text/css' href='../css/items.css' />
			<script type='text/javascript' src='../js/jquery-1.4.4.min.js'></script>
			<script type='text/javascript' src='../js/items.js'></script>
		</head>
		<body>''']
		#get parameters from GET
		getdata = cgi.FieldStorage()

		#get desired items from database
		dof = None
		dfor = None
		haskey = False
		if getdata.has_key('of'):
			dof = getdata['of']
			haskey = True
		if getdata.has_key('for'):
			dfor = getdata['for']
			haskey = True
		if not haskey:
			return
		items = this.dbconnection.getitems(dof,dfor)
		feedtypes = this.dbconnection.getfeedtypes()
		userid = 1 #for testing purposes only
		roles = this.dbconnection.getroles(userid)
		this.html += ["<div id='items'>"]
		for item in items:
			#encode data in proper form
			itemtime = time.strftime("%I:%M%p - %b %d '%y",time.gmtime(float(item[7])))
			if item[5].strip() == "":
				itemauthor = ""
			else:
				itemauthor = "From %s" %(item[5])
			#display item
			this.html += ["<div id='item-%s'>" %(item[0])]
			this.html += ["		<div id='header'>"]
			this.html += ["			<img id='typeicon' src='../img/feedtype%s.gif' />" %(feedtypes[item[1]][0])]
			this.html += ["			<a id='title' href='%s'>%s</a>"%(item[6],item[3])]
			this.html += ["			<form action='#' method='post'>"]
			this.html += ["				<select name='roleid' selected='%s'" %(item[2])]
			#display role options
			for role in roles:
				this.html += ["				<option value='%s'>%s</option>" %(role[0],role[2])]
			this.html += ["				</select>"]
			this.html += ["			</form>"]
			this.html += ["			<span id='time'>%s</span>" %(itemtime)]
			this.html += ["		</div>"]
			this.html += ["		<div id='content'>"]
			this.html += ["			<p>%s @ %s,</p>" %(itemauthor,itemtime)]
			this.html += ["			<p>%s</p>" %(item[4])]
			this.html += ["		</div>"]
			this.html += ["</div>"]
		this.html += ["</div>"]
		
		#add footer
		this.html += ['''</body>
		</html>''']
		#output
		print '\n'.join(this.html)
view()