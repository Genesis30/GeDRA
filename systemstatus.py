#!/usr/bin/python

import os, sys, time
import ds
import systemdatabase as systemdb

#############################
# Monitoring the syslog directory & file
#############################
directoryPath = '/home/carlos/Desktop/'
syslogPath = '/home/carlos/Desktop/asd'

#############################
#	Function "init"
#		Calculates base status of risk of the system
#		
#############################
def init():
	pass

#############################
#	Function "evaluateIncident"
#		
#		
#############################
def showStatus():
	pass

#############################
#	Function "decideAffectedElement"
#		Provided an attack name, it compares with a defined dictionary and returns
#		the affected parts of the system.
#############################
def updateElement(element_name, affected_element_id, risk):

	db = systemdb.systemDatabase()
	temp = db.addToTable('prueba1',affected_element, affected_element_id,'risk="'+risk+'"')

	# dbName, tableName, data, ident, part_name