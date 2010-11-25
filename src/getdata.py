#!/usr/bin/python
#get data input

import sqlite3,feedparser,dbconnection

class getdata:
	dbconnection = None
	
	def __init__(this):
		this.dbconnection = dbconnection.dbconnection()
		this.update()
		
	def update(this): #poll all data feeds, add new data to db
		#1 - get data feed urls from db
		feedurls = this.dbconnection.getfeedurls()
		print feedurls
		#2 - check data feeds for new items
		feeds = []
		for feedurl in feedurls:
			feeds.append(feedparser.parse(feedurl[1]))
			print feeds[-1]
			if feeds[-1]['entries']: #if there are new entries
				#print feeds[-1]['entries']
				for entry in feeds[-1]['entries']:
					#print entry['summary_detail']['value'],'-',entry['title'],'-',entry[]
					print entry,'\n'
					#do analysis to get roleid
					#add new data to db
		
		
		#login to gcal feed with:
		#https://www.google.com/accounts/ClientLogin
		#
		#The POST body should contain a set of query parameters, as described in the following table. They should look like parameters passed by an HTML form, using the application/x-www-form-urlencoded content type.
		#Parameter 	Description
		#Email 	The user's email address.
		#Passwd 	The user's password.
		#source 	Identifies your client application. Should take the form companyName-applicationName-versionID; below, we'll use the name exampleCo-exampleApp-1.
		#service 	The string cl, which is the service name for Google Calendar.			
getdata()