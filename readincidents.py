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
	calculateParams(params)
	print 'Incident processed @ %s.' % time.ctime()
	print 'Status of the system updated.'


class MyHandler(FileSystemEventHandler):
	def on_modified(self,event):
		if event.src_path == syslogPath:
			checkSystem()

def readLogFile(incidentTime):
	
	params = rf.parseInfo(incidentTime)
	return params

def calculateParams(params):
	print params
	pass
	"""
	data = ds.calculateParams(params)
	risk = ds.calculateRisk(data)

	if(mail==True):
		sendMail(risk)
	else:
		writeLog(risk)

	"""