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
			<script type='text/javascript' src='../jq/farbtastic/farbtastic.js'></script>
			<script type='text/javascript' src='../js/main.js'></script>
			<link rel='stylesheet' type='text/css' href='../css/ui-lightness/jquery-ui-1.8.6.custom.css' >
			<link rel='stylesheet' type='text/css' href='../css/main.css' >
			<link rel='stylesheet' type='text/css' href='../jq/farbtastic/farbtastic.css' >
		</head>
		<body>''']
		#build content
		#get roles data
		userid = 1 #testing only
		roles = this.dbconnection.getroles(userid)
		#make roles sidebar
		this.html += ["<div id='roleslink'><a href='#'>Roles</a></div>"]
		this.html += ["<div id='roles' title='Roles'>"]
		this.html += ["		<ol>"]
		for role in roles:
			this.html += ["		<li><span class='hidden'>%s|#%s</span><img id='handle' src='../img/handle.gif'></img>%s<a id='remove' href='#'>[remove]</a></li>" %(role[0],role[3],role[2])]
		this.html += ["		</ol>"]  
		this.html += ["		<div id='addupdaterole'>"]
		this.html += ["			<label for='name'>Name:<input name='name' id='name' type='text' /></label>"]
		this.html += ["			<div id='colorchoose'></div><label for='color'>Color:<input id='color' type='text' name='color' /></label>"]
		this.html += ["			<div id='attrs'>"]
		this.html += ["				Attributes:"]
		this.html += ["				<div id='attr-0'>"]
		this.html += ["					<select id='attr' name='attr'>"]
		this.html += ["						<option value='title'>Title</option>"]
		this.html += ["						<option value='body'>Body</option>"]
		this.html += ["						<option value='author'>Author</option>"]
		this.html += ["					</select>"]
		this.html += ["					<select id='comparison' name='comparison'>"]
		this.html += ["						<option value='equals'>Equals</option>"]
		this.html += ["						<option value='includes'>Includes</option>"]
		this.html += ["					</select>"]
		this.html += ["					<input id='value' name='value' type='text' />"]
		this.html += ["					</br><a id='showattr-1' href='#'>(+ another attribute)</a>"]
		this.html += ["				</div>"]
		for i in range(10):
			this.html += ["				<div id='attr-%s'>" %(i+1)]
			this.html += ["					<select id='attr' name='attr'>"]
			this.html += ["						<option value='title'>Title</option>"]
			this.html += ["						<option value='body'>Body</option>"]
			this.html += ["						<option value='author'>Author</option>"]
			this.html += ["					</select>"]
			this.html += ["					<select id='comparison' name='comparison'>"]
			this.html += ["						<option value='equals'>Equals</option>"]
			this.html += ["						<option value='includes'>Includes</option>"]
			this.html += ["					</select>"]
			this.html += ["					<input id='value' name='value' type='text' />"]
			if i < 9:
				this.html += ["					</br><a id='showattr-%s' href='#'>(+ another attribute)</a>" %(i+2)]
			this.html += ["				</div>"]
		this.html += ["			</div>"]
		this.html += ["			<a href='#' id='submit'>Create Role</a>"]
		this.html += ["		</div>"]                            
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