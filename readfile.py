#!/usr/bin/python

logPath = '/var/log/syslog'
data = ''
def parseInfo():
	with open(logPath,'r') as log:
		temp = log.readlines()
		lines = len(temp)
		print lines
		print temp[lines-1]

parseInfo()