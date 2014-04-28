#!/usr/bin/python

import os, sys, time
import readfile as rf
import ds
import systemdatabase as systemdb
import systemstatus
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

#############################
# Monitoring the syslog directory & file
#############################
directoryPath = '/home/carlos/Desktop/'
syslogPath = '/home/carlos/Desktop/asd'

#directoryPath = '/home/genesis/Desktop/'
#syslogPath = '/home/genesis/Desktop/asd'

#############################
#	Class "MyHandler"
#		Modified event handler. When it detects a change in syslog file, proceeds to process it. 
#############################
class MyHandler(FileSystemEventHandler):
	def on_modified(self,event):
		if event.src_path == syslogPath:
			checkSystem()

#############################
#	Function "background"
#		Creates an observer who checks the desired directory every second. 
#		Stopped by a Keyboard interrupt.
#############################
def background():
	observer = Observer()
	event_handler = MyHandler()
	observer.schedule(event_handler, directoryPath, recursive=False)
	observer.start()
	flag = 0
	try:
		while (True):
			# Sleep 1 second
			time.sleep(1)
			# Reset the risk values of the system
			flag+=1
			if flag == 60:
				systemstatus.reportStatus()
				
			if flag	== 600:
				flag = 0
				ds.restartAlertNumber
				systemstatus.init()
	except KeyboardInterrupt:
		print "\nStopping GeDRA. This shouldn't take long."
		observer.stop()
	observer.join()

#############################
#	Function "checkSystem"
#		When a change in the syslog file is detected, this function is called.
#		Calls rf.parseInfo and provides it the current time. This function returns
#		a data structure, that is passed over to be evaluated.
#############################
def checkSystem():
	params = rf.parseInfo(time.ctime())
	if 'snort' in params[7]:
		print 'New incident detected @ %s. Processing.' % time.ctime()
		evaluateIncident(params)
		print 'Incident processed @ %s.' % time.ctime()
		print 'Status of the system updated.'

#############################
#	Function "evaluateIncident"
#		Given a data structure "params", it extracts the relevant information and calls
#		the "ds" module to get the correct parameters to evaluate risk.
#############################
def evaluateIncident(params):
	attack_name = params[2]
	affected_element_ip = params[6]
	affected_element_info = decideAffectedElement(attack_name, affected_element_ip)

	data = ds.calculateParams(params,affected_element_info[0],affected_element_info[1],affected_element_info[2])
	
	risk = ds.calculateRisk(data)
	
	print 'New risk: %s  on  "%s" with IP direction "%s"' % (risk, affected_element_info[0], affected_element_ip)
	report(risk, affected_element_info[0], affected_element_ip, params[0])
	systemstatus.updateElement(affected_element_info[0], affected_element_info[3], risk)

#############################
#	Function "decideAffectedElement"
#		Provided an attack name, it compares with a defined dictionary and returns
#		the affected parts of the system.
#############################
def decideAffectedElement(attack_name, affected_element_ip):

	attack_dict = { "attempted administrator privilege gain": 4,
					"attempted user privilege gain": 4,
					"score! get the lotion!": 4,
					"potential corporate privacy violation": 4,
					"executable code was detected": 4,
					"successful administrator priviledge gain": 4,
					"successful user priviledge gain": 4,
					"a network trojan was detected": 4,
					"unsuccessful user privilege gain": 4,
					"web application attack": 4,
					"attempted denial of service": 3,
					"attempted information leak": 3,
					"potentially bad traffic": 3,
					"attempt to login by a default username and password": 3,
					"detection of a denial of service attack": 3,
					"misc attack": 3,
					"detection of a non-standard protocol or event": 3,
					"decode of an rpc query": 3,
					"denial of service": 3,
					"large scale information leak": 3,
					"information leak": 3,
					"a suspicious filename was detected": 3,
					"an attempted login using a suspicious user-name was detected": 3,
					"a system call was detected": 3,
					"a client was using an unusual port": 3,
					"access to a potentially vulnerable web application": 3,
					"generic icmp event": 2,
					"misc activity": 2,
					"detection of a network scan": 2,
					"not suspicious traffic": 2,
					"generic protocol command decode": 2,
					"a suspicious string was detected": 2,
					"unknown traffic= -": 2,
					"a tcp connection was detected= -": 1,
	}

	affected_element = rf.parseSystemFile(affected_element_ip)
	#####
	# Query the database of the system
	db = systemdb.systemDatabase()
	temp = db.getFromTable('prueba1',affected_element,'rating','ip="'+affected_element_ip+'"')
	temp2 = db.getFromTable('prueba1',affected_element,'id','ip="'+affected_element_ip+'"')
	affected_element_relevance = temp.strip("'(,)'")
	affected_element_id = temp2.strip("'(,)'")
	#
	#####	

	info = ['' for i in range(4)]
	info[0], info[1], info[2], info[3] = affected_element , affected_element_relevance, attack_dict[attack_name], affected_element_id
	return info

#############################
#	Function "report"
#		Write information in the report file.
#############################
def report(risk, affected_element, affected_element_ip, incidentTime):
	user = os.getlogin()
	f =  open('/home/'+ user +'/gedra/report','a')
	data = 	'\nNew risk: %s  on  "%s" with IP direction "%s"\nDetected @ %s\n' % (risk, affected_element, affected_element_ip, incidentTime)
	f.write(data)
	f.close()