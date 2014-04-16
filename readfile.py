#!/usr/bin/python

#logPath = '/var/log/syslog'
syslogPath = '/home/genesis/Desktop/asd'

def parseInfo(incidentTime):
	with open(syslogPath,'r') as log:
		temp = log.readlines()
		lines = len(temp)
		# Format the last line in the file
		data = formatLine(temp[lines-1], incidentTime)
		return data

def formatLine(line, incidentTime):

	# Remove unnecessary info & get only relevant info
	splitWhite = line.split(None,2)
	temp1 = splitWhite[2]

	# Split the desired info
	temp2 = temp1.split('[')

	# Wat?
	var1 = temp2[0].strip()

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

	#printThings()
	#print '********'
	#print 'Incident report: '
	#print var1
	#print classification
	#print priority
	#print protocol
	#print sourceIp
	#print destinationIp
	#print '********'

	params = ['' for i in range(7)]
	params[0],params[1],params[2],params[3],params[4],params[5],params[6] = incidentTime, var1, classification, priority, protocol, sourceIp, destinationIp
	return params