#!/usr/bin/python

import MySQLdb as mdb

# http://127.0.0.1/phpmyadmin/
# User: gedra
# Pass: gedra
con = mdb.connect('localhost', 'gedra', 'gedra')
cursor = con.cursor()

class reportDatabase():
	
	def readThings(self):
		print 'Reading things.'