#!/usr/bin/python

import Cookie, os, cgi, sqlite3

try:
	cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
				
	new = Cookie.SimpleCookie()
	new["userid"] = cookie["userid"].value
	new["userid"]["expires"] = 0
	new["userid"]["path"] = cookie["userid"]["path"]
	print new
	
	print 'Location: ../src/index.py\r\n'
	
except:	
		
	print 'Location: ../src/index.py\r\n'
							

