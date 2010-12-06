#!/usr/bin/python

import dbconnection,cgi,time,operator,datetime,time,Cookie,os

#views to display data
class view:
	dbconnection = None
	html = None
	def __init__(this):
		this.dbconnection = dbconnection.dbconnection()
		this.html = []
		try:
			cookies = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
			userid = int(cookies['userid'].value)
			this.html += ["Content-type: text/html\n"]
			this.html += ['''<html>
			<head>
				<link rel='stylesheet' type='text/css' href='../css/items.css' />
				<script type='text/javascript' src='../js/items.js'></script>
			</head>
			<body>''']
			#get parameters from GET
			getdata = cgi.FieldStorage()

			#get desired items from database
			dof = None
			dfor = None
			drecent = None
			dorderby = None
			haskey = False
			currentattrs = ""
			if getdata.has_key('of'):
				dof = getdata['of']
				haskey = True
				currentattrs = "of="+getdata['of'].value
			if getdata.has_key('for'):
				dfor = getdata['for']
				haskey = True
				if currentattrs != '':
					currentattrs = currentattrs+"&for="+getdata['for'].value
				else:
					currentattrs = "for="+getdata['for'].value
			if getdata.has_key('orderby'):
				dorderby = getdata['orderby']
				if currentattrs != '':
					currentattrs = currentattrs+"&orderby="+getdata['orderby'].value
				else:
					currentattrs = "orderby="+getdata['orderby'].value
				haskey = True
			if getdata.has_key('recent'):
				drecent = getdata['recent'].value	
				if currentattrs != '':
					currentattrs = currentattrs+"&recent="+getdata['recent'].value
				else:
					currentattrs = "recent="+getdata['recent'].value		
			if not haskey:
				return
			items = this.dbconnection.getitems(userid,dof,dfor,dorderby,drecent)

			feedtypes = this.dbconnection.getfeedtypes()
			#userid = 1 #for testing purposes only
			roles = this.dbconnection.getroles(userid)
			this.html += ["<div id='items'>"]
			#put current url in hidden span
			this.html += ["		<span id='hiddenurl' class='hidden'>view.py?%s</span>" %(currentattrs)]
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
				this.html += ["			<a id='permalink' href='#item-%s'>#</a><a id='title' href='%s'>%s</a>"%(item[0],item[6],item[3])]
				this.html += ["			<form action='#' method='post'>"]
				this.html += ["				<select name='roleid'>"]
				#display role options
				beenselected = False
				for role in roles:
					if int(role[0]) == int(item[2]):
						selected = "selected=''"
						beenselected = True
					else:
						selected = ""
					this.html += ["				<option %s value='%s|#%s'>%s</option>" %(selected,role[0],role[3],role[2])]
				if not beenselected:
					selected = "selected=''"
				else:
					selected = ""
				this.html += ["					<option %s value='none|white'>None</option>" %(selected)]
				this.html += ["				</select>"]
				this.html += ["			</form>"]
				this.html += ["			<span id='time'>%s</span>" %(itemtime)]
				this.html += ["		</div>"]
				this.html += ["		<div id='content'>"]
				this.html += ["			<p>%s @ %s,</p>" %(itemauthor,itemtime)]
				this.html += ["			<p>%s</p>" %(item[4])]
				this.html += ["		</div>"]
				this.html += ["</div>"]
			numitems = len(items)
			this.html += ["		<span id='hiddenrecent' class='hidden'>%s</span>" %(numitems)]
			this.html += ["</div>"]

			#add footer
			this.html += ['''</body>
			</html>''']
			#output
			print '\n'.join(this.html)
		except:
			print "Location: ../src/index.py"
view()