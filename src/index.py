#!/usr/bin/python

import Cookie, os, cgi, sqlite3

logged_in = False

form = cgi.FieldStorage()
			
if form.has_key("username"):
	
	
	username = form["username"].value
	password = form["password"].value

	connection = sqlite3.connect('../storage.db')
	cursor = connection.cursor()

	query = "SELECT * FROM users WHERE username='%s' AND password='%s'" %(username,password)
	cursor.execute(query)
	result = ""
	result = cursor.fetchone()
	
	if result is not None:
				
		C = Cookie.SimpleCookie()
		C["userid"] = result[0]

		print C	

		print 'Location: ../src/index.py\r\n\r\n' 

				
				
				
	else:
		
		
		print 'Location: ../src/index.py\r\n\r\n' 

	

	

else:
	try:
		cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
				
		userid = cookie["userid"].value
	

		if userid is not None and userid != "":
			logged_in = True
			
			
			print 'Location: ../src/home.py\r\n\r\n'
	except:
		
				
		
		print "Content-Type: text/html\n"

		print "<form name='login' method='post' action='../src/index.py'>Username: <input type='text' name='username'> Password: <input type='password' name='password'> <input type='submit' name='submit' value='Login'> </form>"
		print "<a href='../src/register.py'>Register</a>"
							

				
