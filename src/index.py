#!/usr/bin/python
#main page

import cgi,view,dbconnection

class index:
	html = None
	dbconnection = None
	def __init__(this):
		this.dbconnection = dbconnection.dbconnection()
		this.html = []
		#build header
		this.html += ["Content-type: text/html\n"]
		this.html += ['''<html>
		<head>
			<title>InfoCentral</title>
			<script type='text/javascript' src='../js/jquery-1.4.4.min.js'></script>
			<script type='text/javascript' src='../js/jquery-ui-1.8.6.custom.min.js'></script>
			<script type='text/javascript' src='../js/main.js'></script>
			<link rel='stylesheet' type='text/css' href='../css/ui-lightness/jquery-ui-1.8.6.custom.css' >
			<link rel='stylesheet' type='text/css' href='../css/main.css' >
		</head>
		<body>''']
		#build content
		#get roles data
		userid = 1 #testing only
		roles = this.dbconnection.getroles(userid)
		#make roles sidebar
		this.html += ["<a id='roleslink' href='#'>Roles</a>"]
		this.html += ["<div id='roles' title='Roles'>"]
		this.html += ["		<ol>"]
		for role in roles:
			this.html += ["		<li><span class='hidden'>%s|#%s</span><img id='handle' src='../img/handle.gif'></img>%s<a id='remove' href='#'>[remove]</a><a id='edit' href='#'>[edit]</a></li>" %(role[0],role[3],role[2])]
		this.html += ["		</ol>"]                              
		this.html += ['</div>']
		#make tab bar from each feed
		this.html += ['''<div id='tabs'>
		<ul>
			<li><a href="view.py?of=-1"><span>All</span></a></li>
			<li><a href='view.py?of=1'><span>Email</span></a></li>
			<li><a href='view.py?of=2'><span>Calendar</span></a></li>
			<li><a href='view.py?of=0'><span>Articles</span></a></li>
		</ul>''']
	
		#build footer
		this.html += ["</body>\n</html>"]
		#output
		print "\n".join(this.html)
index()