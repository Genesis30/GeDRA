#!/usr/bin/python

import os, sys

import xmlread as xread
import systemdatabase as systemdb
import readincidents as read

#############################
#	Function "validateFile"
#		Checks if there is a provided file, and asks for it otherwise. 
#		"model_file" stores the path value.
#############################
def initialCheck():
	# Basic usage, working daemonized
	if len(sys.argv) == 1:
		print 'GeDRA started running.'
		print 'If you want to stop the execution, please use "Ctrl+C"'
		read.background()

	# Check wich option is provided
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
		else:
			print 'The option provided is not supported.'
			usage()
			sys.exit(0)

#############################
#	Function "usage"
#		Help page
#############################
def usage():
    print "\nUSAGE: %s [options]" % sys.argv[0]
    print "Without options      	  	run the module in background.\n"
    print "OPTIONS:"
    print "-c --create 'file.xml'  	build a new system defined in the provided file."
    print "-a --add 'System'	   	add elements to previously created system."
    print "-h --help           		display this information."
    print

# ---- Main ----
initialCheck()