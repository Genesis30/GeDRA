#!/usr/bin/python

import os, sys, time
import readfile as rf
import ds
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

directoryPath = '/home/genesis/Desktop/'
syslogPath = '/home/genesis/Desktop/asd'

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

def checkSystem():
	print 'New incident detected @ %s. Processing.' % time.ctime()
	params = readLogFile(time.ctime())
	evaluateIncident(params)
	print 'Incident processed @ %s.' % time.ctime()
	print 'Status of the system updated.'


class MyHandler(FileSystemEventHandler):
	def on_modified(self,event):
		if event.src_path == syslogPath:
			checkSystem()

def readLogFile(incidentTime):
	
	params = rf.parseInfo(incidentTime)
	return params

def evaluateIncident(params):
	print params
	
	attack_step = params[1]
	attack_name = params[2]

	affected_element = decideAffectedElement(attack_name)
	affected_element_ip = params[6]

	data = ds.calculateParams(attack_step,attack_name,affected_element,affected_element_ip)
	risk = ds.calculateRisk(data)
	"""
	data[i] = AK, CK0, BK, RS0, priority_IDS, IDS_name
	"""

def decideAffectedElement(attack_name):
	
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

	return attack_dict[attack_name]