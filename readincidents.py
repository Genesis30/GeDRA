#!/usr/bin/python

import os, sys, time
import readfile as rf
import ds
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

syslogPath = '/home/carlos/Desktop/asd'

def background():
	observer = Observer()
	syslogPath = '/home/carlos/Desktop'
	event_handler = MyHandler()
	observer.schedule(event_handler, path=syslogPath, recursive=False)
	observer.start()

	try:
		while (True):
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
	observer.join()

def checkSystem():
	print 'New incident detected @ %s. Processing.' % time.ctime()
	readLogFile()
	print 'Incident processed @ %s.' % time.ctime()
	print 'Status of the system updated.'


class MyHandler(FileSystemEventHandler):
	def on_modified(self,event):
		if event.src_path == syslogPath:
			checkSystem()

def checkChanges():
	event_handler = MyHandler()
	observer.schedule(event_handler, path=syslogPath, recursive=False)
	observer.start()

def readLogFile():
	print 'New risk of the affected target is 0.725. Check your mail/log for extra info.'
	pass
	"""
	# open file
	# read new line
	# classify event
	params = rf.parseInfo()

	data = ds.calculateParams(params)
	risk = ds.calculateRisk(data)

	if(mail==True):
		sendMail(risk)
	else:
		writeLog(risk)

	# call calculateParams
	# call calculate Risk
	# report if needed (mail, log)
	#
	#	alert_syslog: \
    #   <facility> <priority> <options>
	#
	#	  output alert_syslog: \
    #   [host=<hostname[:<port>],] \
    #   <facility> <priority> <options>
	#
	"""