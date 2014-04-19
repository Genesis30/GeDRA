#!/usr/bin/python

#logPath = '/var/log/syslog'
syslogPath = '/home/genesis/Desktop/asd'

#############################
#	Function "parseInfo"
#		Open the syslog file, retrieve the last line and calls
#		the function to format it as desired.
#############################
def parseInfo(incidentTime):
	with open(syslogPath,'r') as log:
		temp = log.readlines()
		lines = len(temp)
		# Format the last line in the file
		data = formatLine(temp[lines-1], incidentTime)
		return data

#############################
#	Function "formatLine"
#		Given a line of the syslog file, it process it. If the line is not build from 
#		the "IDS", no process is made.
#
#		If it is made by the IDS, it proceeds to process it and returns the relevant info.		
#############################
def formatLine(line, incidentTime):
	# Data structure to retrieve info
	params = ['' for i in range(8)]
	# Remove unnecessary info & get only relevant info
	splitWhite = line.split(None,2)
	isIds = splitWhite[0]
	if not 'snort' in isIds:
		params[7] = 'notRelevant'
		return params
	else:
		temp1 = splitWhite[2]

		# Split the desired info
		temp2 = temp1.split('[')

		# Attack step?
		step = temp2[0].strip()

		# Classification
		temp21 = temp2[1].rstrip()
		classification = temp21.rstrip(']')

		# Priority
		temp3 = temp2[2]
		temp4 = temp3.split(']')
		priority = temp4[0].strip()

		# Protocol & ip directions
		temp5 = temp4[1].lstrip(':')
		temp6 = temp5.lstrip()
		temp7 = temp6.split()
		temp7.pop(2)

		protocol = temp7[0]
		sourceIp = temp7[1]
		destinationIp = temp7[2]

		# Data structure to be returned
		params[0],params[1],params[2],params[3],params[4],params[5],params[6], params[7] = incidentTime, step, classification, priority, protocol, sourceIp, destinationIp, isIds
		return params