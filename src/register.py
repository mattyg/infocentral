#!/usr/bin/python

import Cookie, os, cgi, sqlite3


form = cgi.FieldStorage()
cursor = None
connection = None

if form.has_key("username"):
	username = form["username"].value
	password = form["password"].value
				
	print "Content-Type: text/html\n"
	connection = sqlite3.connect('../storage.db')
	cursor = connection.cursor()

	query = "insert into users (username,password) values ('%s','%s')" %(username,password) 
	cursor.execute(query)
	connection.commit()	


	print "You have registered! Please <a href='../src/index.py'>Log In</a>"

else:
	
	print "Content-Type: text/html\n"
	print "Register: <form name='new' method='post' action='../src/register.py'> Username: <input type='text' name='username'> Password: <input type='password' name='password'><input type='submit' name='submit' value='Submit'></form>"
