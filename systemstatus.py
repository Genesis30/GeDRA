#!/usr/bin/python

import os, sys, time
import ds
import readfile as rf
import systemdatabase as systemdb

#Dict
system_risk_dict = {}

#############################
#	Function "init"
#		Calculates the initial values of risk
#		
#############################
def init():
	elements = rf.getElements()
	for element in elements:
		info = element.split(':')

		element_name = info[0]
		element_id = info[1]
		element_rating = info[2]

		temp = element_name + '-' + element_id
		params = [0,0,0,0,0,0,0,0]
		data = ds.calculateParams(params ,element_name , element_rating, 0)
		# system_risk_dict['element_name - element_id'] = element_risk
		system_risk_dict[temp] = ds.calculateRisk(data)
		updateElement(element_name, element_id, risk)
	print 'Initialized system risk.'

#############################
#	Function "showStatus"
#		
#		
#############################
def showStatus():
	os.system('cat /home/carlos/gedra/status')

#############################
#	Function "updateElement"
#		Provided an attack name, it compares with a defined dictionary and returns
#		the affected parts of the system.
#############################
def updateElement(element_name, affected_element_id, risk):
	temp = element_name + '-' + affected_element_id
	system_risk_dict[temp] = risk

	db = systemdb.systemDatabase()
	db.modifyDatabase(element_name, affected_element_id,'risk', risk)
	db.closeDatabase()

#############################
#	Function "reportStatus"
#		Updates the state of the system into de "status" file every 60 seconds
#############################
def reportStatus():
	user = os.getlogin()
	f =  open('/home/'+ user +'/gedra/status','w')
	data = 	'\nAutomatic report. Updated every 60 seconds.\n\n%s\n\n' % (system_risk_dict)
	f.write(data)
	f.close()