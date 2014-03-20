#!/usr/bin/python

import os, sys

def validateData(tmp):
	# String magic
	campos = tmp.split(',')
	columnas = ''
	valores = ''
	for i in range(len(campos)):
		h = campos[i].split(':')
		columnas += ',' + h[0]
		valores += ',"' + h[1].lstrip() +'"'

	col = columnas.lstrip(',')	
	val = valores.lstrip(',')
	validated = [col,val]
	return validated
	# --------------

dbName = str(raw_input("Enter the name of the system: "))
partName = str(raw_input("Is it hardware or software?: "))
tableName = str(raw_input("Enter the name of the element type: "))

tmp = str(raw_input("Enter the data to add ['FieldName1: new_value , FieldName2: new_value']: "))

campos = validateData(tmp)

sqlInsertIntoTable = ' INSERT INTO ' + tableName + ' ('+campos[0]+') VALUES ('+campos[1]+');'
print sqlInsertIntoTable

# Campo1: a, Campo2: b, Campo3: c