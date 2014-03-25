#!/usr/bin/python

import xml.etree.ElementTree as et
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

	db = database()

	dbName = root.attrib.get('name')

	db.createDB(dbName)
	# Building up the system structure
	for part in root:
		# Create HW & SW
		db.createPartTable(dbName,part.tag)
		for element in part:
			# Create table for each element
			db.createElementTable(dbName,element.tag,part.tag)
			for instance in element:
				ident = instance.attrib.get('name')	
				temp = ''
				for charact in instance:
					temp += ',"' + str(charact.text) +'"'
				data = '"'+ident+'"'+temp
				# Add info to the previously created table
				db.addToTable(dbName,element.tag,data,ident,part.tag)
		print '"%s" done.' % part.tag
	db.closeDatabase()

#############################
#	Function "modifyFile"
#		Given data, proceeds to format it correctly and to modify the file
#		who describes the system. Also updates the system database.
#
#	@param: data
#############################
def modifyFile(data):
	# Do fancy stuff with the data
	# once the data is formatted, rebuild the system file
	# and pass it to readFile() to update the system db.
	modifiedFile = ''
	readFile(modifiedFile)