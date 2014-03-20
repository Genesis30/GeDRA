#!/usr/bin/python
import os, sys
import xml.etree.ElementTree as et
import MySQLdb as mdb
from database import *

#############################
#	Function "readFile"
#		Given a valid file, proceeds to read it and to organize it in order to provide
#		info to build the database.
#
#	@param: model_file
#############################
def readFile(model_file):
	tree = et.parse(model_file)
	root = tree.getroot()

	dbName = root.attrib.get('name')

	createDB(dbName)
	# Building up the system structure
	for part in root:
		# Create HW & SW
		createPartTable(dbName,part.tag)
		for element in part:
			# Create table for each element
			createElementTable(dbName,element.tag,part.tag)
			for instance in element:
				ident = instance.attrib.get('name')	
				temp = ''
				for charact in instance:
					temp += ',"' + str(charact.text) +'"'
				data = '"'+ident+'"'+temp
				# Add info to the previously created table
				addToTable(dbName,element.tag,data,ident,part.tag)
		print '"%s" done.' % part.tag

	closeDatabase()