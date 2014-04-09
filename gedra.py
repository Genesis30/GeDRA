#!/usr/bin/python

import os, sys

import xmlread as xread
import systemdatabase as systemdb
import readincidents as read


# ---- Functions ----
#############################
#	Function "validateFile"
#		Checks if there is a provided file, and asks for it otherwise. 
#		"model_file" stores the path value.
#############################
def initialCheck():
	# If no file is provided, ask for it
	if len(sys.argv) == 1:
		read.background()

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
			xread.readFile(model_file)

		if option == '-a' or option == '--add':
			# Necesario aqui?
			systemdb.addToTable()
			pass

		if option == '-h' or option == '--help':
			usage()
			sys.exit(0)

def usage():
    print "\nUSAGE: %s [options]" % sys.argv[0]
    print "Without options      	  	run the module in background."
    print "OPTIONS:"
    print "-c --create 'xml.file'  	build a new system defined in the provided file."
    print "-a --add 'System'	   	add elements to previously created system."
    print "-h --help           		display this information."

# ---- Main ----

initialCheck()