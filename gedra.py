#!/usr/bin/python

import os, sys

from database import *
from xmlread import *


model_file = 0
# ---- Functions ----
#############################
#	Function "validateFile"
#		Checks if there is a provided file, and asks for it otherwise. 
#		"model_file" stores the path value.
#############################
def initialCheck(model_file):
	# If no file is provided, ask for it
	if len(sys.argv) == 1:
		sys.exit(0)
		#model_file = str(raw_input("Enter the name of the xml file descriptor: "))
	# If a file is provided, check if it is valid
	elif len(sys.argv) >= 2:
		option = sys.argv[1]

		if (option == '-c') or (option == '--create'):
			if len(sys.argv) == 3:
				filePath = sys.argv[2]
				if os.path.exists(filePath):
					model_file = filePath
				# Else, ask for a new path
				else:
					model_file = str(raw_input("The file does not exist. Enter a valid path: "))
			else:
				model_file = str(raw_input("Enter the name of the xml file descriptor: "))

		if option == '-u' or option == '--update':
			#update()
			pass

		if option == '-a' or option == '--add':
			#addToSystem()
			pass

		if option == '-i' or option == '--image':
			#createImage()
			pass

		if option == '-h' or option == '--help':
			usage()
			sys.exit(0)
	return model_file


def usage():
    print "\nUSAGE: %s [options]" % sys.argv[0]
    print "Without options      	  	run the module in background."
    print "OPTIONS:"
    print "-c --create 'xml.file'  	build a new system defined in the provided file."
    print "-u --update			force the system to update."
    print "-a --add 'System'	   	add elements to previously created system."
    print "-i --image              	get status of the system with an image."  
    print "-h --help           		display this information."

# ---- Main ----

while model_file == 0:
	model_file = initialCheck(model_file)

readFile(model_file)
