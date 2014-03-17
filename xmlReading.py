#!/usr/bin/env python
import os, sys
import xml.etree.ElementTree as et

# -------------- Functions --------------
#############################
#	Function "validateFile"
#		Checks if there is a provided file, and asks for it otherwise. 
#		"model_file" stores the path value.
#############################
def validateFile():
	# If no file is provided, ask for it
	if len(sys.argv) == 1:
		model_file = str(raw_input("Enter the name of the xml file descriptor: "))
	# If a file is provided, check if it is valid
	elif len(sys.argv) == 2:
		filePath = sys.argv[1]
		if os.path.exists(filePath):
			model_file = filePath
		# Else, ask for a new path
		else:
			model_file = str(raw_input("The file does not exist. Enter a valid path: "))

#############################
#	Function "updateDatabase"
#		Given the data to populate the database, it proceeds to do so.
#
#	@param: data, the information to build/update the database
#############################
def updateDatabase(data):

#############################
#	Function "readFile"
#		Given a valid file, proceeds to read it and to organize it in order to provide
#		info to build the database.
#
#	@param: model_file
#############################
def readFile(model_file):
	tree = et.parse(model_file)
	system = tree.getroot()

	data = [][][]
	for element in system:
		data[].append(element.tag)
		for part in element:
			data[][].append(part.tag)
			for charac in part:
				data[][][].append(charac.tag)
	updateDatabase(data)


# -------------- Program --------------

validateFile()
for part in root:
		print part.tag
		print '-------'
		for element in part:
			print element.tag, element.attrib
			for charac in element:
				print charac.tag, charac.text
			print '**** \n'
	updateDatabase(data)

# print et.tostring(root, encoding="us-ascii", method="xml")