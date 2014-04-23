#!/usr/bin/python

import os, sys, time
import readfile as rf
import ds
import systemdatabase as systemdb
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

#############################
# Monitoring the syslog directory & file
#############################
directoryPath = '/home/carlos/Desktop/'
syslogPath = '/home/carlos/Desktop/asd'

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
	
	try:
		while (True):
			# Sleep 1 second
			time.sleep(1)
	except KeyboardInterrupt:
		print "Stopping GeDRA. This shouldn't take long."
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

#############################
#	Function "decideAffectedElement"
#		Provided an attack name, it compares with a defined dictionary and returns
#		the affected parts of the system.
#############################
def decideAffectedElement(attack_name, affected_element_ip):

	attack_dict = { "attempted administrator privilege gain": ,
					"attempted user privilege gain": ,
					"score! get the lotion!": ,
					"potential corporate privacy violation": ,
					"executable code was detected": ,
					"successful administrator priviledge gain": ,
					"successful user priviledge gain": ,
					"a network trojan was detected": 5,
					"unsuccessful user privilege gain": ,
					"web application attack": ,
					"attempted denial of service": ,
					"attempted information leak": ,
					"potentially bad traffic": ,
					"attempt to login by a default username and password": ,
					"detection of a denial of service attack": ,
					"misc attack": ,
					"detection of a non-standard protocol or event": ,
					"decode of an rpc query": ,
					"denial of service": ,
					"large scale information leak": ,
					"information leak": ,
					"a suspicious filename was detected": ,
					"an attempted login using a suspicious user-name was detected": ,
					"a system call was detected": ,
					"a client was using an unusual port": ,
					"access to a potentially vulnerable web application": ,
					"generic icmp event": ,
					"misc activity": ,
					"detection of a network scan": ,
					"not suspicious traffic": ,
					"generic protocol command decode": ,
					"a suspicious string was detected": ,
					"unknown traffic= -": ,
					"a tcp connection was detected= -": ,
	}
	

	affected_element = rf.parseSystemFile(affected_element_ip)
	#####
	# Query the database of the system
	db = systemdb.systemDatabase()
	temp = db.getFromTable('prueba1',affected_element,'rating','specifications="'+affected_element_ip+'"')
	affected_element_relevance = temp.strip("'(,)'")
	#
	#####	

	info = ['' for i in range(3)]
	info[0], info[1], info[2] = affected_element , affected_element_relevance, attack_dict[attack_name]
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