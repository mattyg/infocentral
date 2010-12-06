#!/usr/bin/python
#main page

import cgi,view,dbconnection,Cookie,os

class index:
	html = None
	dbconnection = None
	def __init__(this):
		this.dbconnection = dbconnection.dbconnection()
		this.html = []
		try:
			cookies = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
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
			#userid = 1 #testing only
			userid = int(cookies['userid'].value)
			roles = this.dbconnection.getroles(userid)
			feeds = this.dbconnection.getfeeds(userid)
			#make new items notice
			this.html += ["<div id='newitems'>"]
			this.html += ["Updated [3]"]
			this.html += ["</div>"]
			#make role selection dropdown
			this.html += ["<div id='roleselect'>"]
			this.html += ["		<select name='roleid'>"]
			this.html += ["			<option selected='' value=''>All Roles</option>"]
			for role in roles:
					this.html += ["		<option value='%s'>%s</option>" %(role[0],role[2])]
			this.html += ["				<option value='-1'>None</option>"]
			this.html += ["		</select>"]
			this.html += ["</div>"]
			#make feeds controllor dialog
			this.html += ["<div id='feedslink'><a href='#'>Feeds</a></div>"]
			this.html += ["<div id='feeds' title='Feeds'>"]
			this.html += ["		<ul>"]
			for feed in feeds:
				this.html += ["		<li><img id='typeicon' src='../img/feedtype%s.gif' /><span id='url'>%s</span><span class='hidden'>%s</span><a id='remove' href='#'>[remove]</a></li>" %(feed[2],feed[1],feed[0])]
			this.html += ["		</ul>"]
			this.html += ["		<div id='addupdatefeed'>"]
			this.html += ["			<span class='hidden'>%s</span>" %(userid)]
			this.html += ["			Type:<select id='type' name='type'>"]
			this.html += ["				<option value='0'>RSS/ATOM</option>"]
			this.html += ["				<option value='1'>GMail</option>"]
			this.html += ["				<option value='2'>GCal</option>"]
			this.html += ["			</select>"]
			this.html += ["			</br><label for='url'>URL:<input id='url' name='url' type='text' /></label>"]
			this.html += ["			</br>Role (if applicable):<select id='roleid' name='roleid'"]
			this.html += ["				<option selected='' value=''>None</option>"]
			for role in roles:
					this.html += ["		<option value='%s'>%s</option>" %(role[0],role[2])]
			this.html += ["			</select>"]
			this.html += ["			</br>Login Info (if necessary):"]
			this.html += ["			</br><label for='secureuser'>User:<input id='secureuser' name='secureuser' type='text' /></label>"]
			this.html += ["			</br><label for='securepass'>Pass:<input id='securepass' name='securepass' type='text' /></label>"]
			this.html += ["			</br><a id='submit' href='#'>Create Feed</a>"]
			this.html += ["		</div>"]
			this.html += ["</div>"]
			#make roles controllor dialog 
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
			this.html += ["<div id='moreitems'>"]
			this.html += ["		<a href='#'>Get More Old Items</a>"]
			this.html += ["</div>"]
			#build footer
			this.html += ["</body>\n</html>"]
			#output
			print "\n".join(this.html)
		except:
			print "Location: ../cgi-bin/index.cgi\n"
index()