#!/usr/bin/python
#main page

import cgi,view

class index:
	html = None
	def __init__(this):
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
		#make roles sidebar
		this.html += ["<div id='roles'>"]
		this.html + ['roles']
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