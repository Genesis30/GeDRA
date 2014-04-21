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
directoryPath = '/home/genesis/Desktop/'
syslogPath = '/home/genesis/Desktop/asd'

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
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
	observer.join()

#############################


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
	"""
	data[i] = AK, CK0, BK, RS0, priority_IDS, IDS_name
	"""

#############################
#	Function "decideAffectedElement"
#		Provided an attack name, it compares with a defined dictionary and returns
#		the affected parts of the system.
#############################
def decideAffectedElement(attack_name, affected_element_ip):

	attack_dict = {"Attempted Administrator Privilege Gain": '',
					"Attempted User Privilege Gain": '',
					"SCORE! Get the lotion!": '',
					"Potential Corporate Privacy Violation": '',
					"Executable code was detected": '',
					"Successful Administrator Priviledge Gain": '',
					"Successful User Priviledge Gain": '',
					"A Network Trojan was Detected": '',
					"Unsuccessful User Privilege Gain": '',
					"Web Application Attack": '',
					"Attempted Denial of Service": '',
					"Attempted Information Leak": '',
					"Potentially Bad Traffic": '',
					"Attempt to login by a default username and password": '',
					"Detection of a Denial of Service Attack": '',
					"Misc Attack": '',
					"Detection of a non-standard protocol or event": '',
					"Decode of an RPC query": '',
					"Denial of Service": '',
					"Large Scale Information Leak": '',
					"Information Leak": '',
					"A suspicious filename was detected": '',
					"An attempted login using a suspicious user-name was detected": '',
					"A system call was detected": '',
					"A client was using an unusual port": '',
					"Access to a potentially vulnerable web application": '',
					"Generic ICMP event": '',
					"Misc activity": '',
					"Detection of a Network Scan": '',
					"Not Suspicious Traffic": '',
					"Generic Protocol Command Decode": '',
					"A suspicious string was detected": '',
					"Unknown Traffic= -": '',
					"A TCP connection was detected= -": '',
	}

	affected_element = rf.parseSystemFile(affected_element_ip)

	#####
	#
	db = systemdb.systemDatabase()
	affected_element_relevance = db.getFromTable('prueba1',affected_element,'rating','ip="'+affected_element_ip+'"')
	#
	#####	

	info = ['' for i in range(3)]
	info[0], info[1], info[2] = affected_element , affected_element_relevance, attack_dict[affected_element]
	return info