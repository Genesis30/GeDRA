#!/usr/bin/python

#logPath = '/var/log/syslog'
syslogPath = '/home/carlos/Desktop/asd'
#syslogPath = '/home/genesis/Desktop/asd'
gedraPath = '/home/carlos/Desktop/pfc/GeDRA/model.xml'
#gedraPath = '/home/genesis/Desktop/GeDRA/model.xml'
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

		# Attack step
		step = temp2[0].strip()

		# Classification
		temp21 = temp2[1].rstrip()
		temp22 = temp21.rstrip(']')
		temp23 = temp22.split(None,1)
		classification = temp23[1].lower()
		
		# Priority
		temp3 = temp2[2]
		temp4 = temp3.split(']')
		temp41 = temp4[0].strip()
		temp42 = temp41.split(None)
		priority = temp42[1]

		# Protocol & IP directions
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


#############################
#	Function "parseSystemFile"
#		Open the system file, retrieve the desired info
#############################
def parseSystemFile(affected_element_ip):
	with open(gedraPath, 'r') as model:
		temp = model.readlines()
		i = 0
		for line in temp:
			if affected_element_ip in line:
				data = temp[i-3]
			i+=1
		temp = data.split(None)
		temp2 = temp[0]
		element = temp2.lstrip('<')
		return element


#############################
#	Function "getElements"
#		Open the system file, retrieve the desired info
#############################
def getElements():
	with open(gedraPath, 'r') as model:
		temp = model.readlines()
		i = 0
		elements = []
		
		for line in temp:
			if '<instance' in line:
				data_name = temp[i-1]
				data_id = temp[i]
				data_rating = temp[i+4]

				# Element Name
				temp_name = data_name.split(None)
				temp2_name = temp_name[0]
				element_name = temp2_name.lstrip('<')

				# Element ID
				temp_id = data_id.split('name=')
				temp2_id = temp_id[1]
				element_id = temp2_id.strip('">\n')

				# Element Rating
				temp_rating = data_rating.split('>')
				temp2_rating = temp_rating[1]
				element_rating = temp2_rating.rstrip('</rating')

				# Update elements
				info = element_name + ':' + element_id + ':' + element_rating
				elements.append(info)

			elif '<software>' in line:
				return elements
			i+=1