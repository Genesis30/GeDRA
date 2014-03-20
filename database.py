#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys

#############################
#	Function "validateFile"
#		Checks if there is a provided file, and asks for it otherwise. 
#		"model_file" stores the path value.
#############################
def createDB(dbName):
	sqlCheckDB = 'SHOW DATABASES LIKE "'+dbName+'";'
	cursor.execute(sqlCheckDB)
	row = str(cursor.fetchone())

	if row == 'None':
		sqlCreateDB = 'CREATE DATABASE ' + dbName + ';'
		cursor.execute(sqlCreateDB)
		print 'Database "%s" successfully created.' % dbName
	else:
		print 'Database "%s" already exists. Keep going.' % dbName
	
#############################
#	Function "validateFile"
#		Checks if there is a provided file, and asks for it otherwise. 
#		"model_file" stores the path value.
#############################
def createPartTable(dbName, tableName):
	sqlUseDB = 'USE ' + dbName + ';' 
	cursor.execute(sqlUseDB)

	sqlCheckTable = 'SELECT * FROM information_schema.tables WHERE table_name = "' + tableName + '";'
	cursor.execute(sqlCheckTable)
	row = str(cursor.fetchone())
	
	if row == 'None': 
		sqlCreateTable = 'CREATE TABLE ' + tableName + '(name varchar(30) PRIMARY KEY);'
		cursor.execute(sqlCreateTable)
		print 'Table "%s" successfully created.' % tableName
	else:
		print 'Table "%s" already exists.' % tableName

#############################
#	Function "validateFile"
#		Checks if there is a provided file, and asks for it otherwise. 
#		"model_file" stores the path value.
#############################
def createElementTable(dbName, tableName, part_name):
	sqlUseDB = 'USE ' + dbName + ';' 
	cursor.execute(sqlUseDB)

	sqlCheckTable = 'SELECT * FROM information_schema.tables WHERE table_name = "'+tableName+'"'
	cursor.execute(sqlCheckTable)
	row = str(cursor.fetchone())

	if row == 'None':
		if part_name == 'hardware':
			sqlCreateTable = 'CREATE TABLE ' + tableName + '(id varchar(10) PRIMARY KEY, firmware varchar(20), specifications varchar(20), specific_software varchar(20),rating varchar(20),comments varchar(20));'
		else:
			sqlCreateTable = 'CREATE TABLE ' + tableName + '(id varchar(10) PRIMARY KEY, name varchar(20), version varchar(20), auto_update varchar(20));'
		
		cursor.execute(sqlCreateTable)
		print 'Table "%s" successfully created.' % tableName
	else:
		print 'Table "%s" already exists.' % tableName

#############################
#	Function "validateFile"
#		Checks if there is a provided file, and asks for it otherwise. 
#		"model_file" stores the path value.
#############################
def addToTable(dbName, tableName, data, ident, part_name):

	sqlCheckData = 'SELECT * FROM ' + tableName + 'WHERE id="' + ident + '";'
	#	
	#	POR COMPLETAR
	#

	if part_name == 'hardware':
		sqlInsertIntoTable = 'INSERT INTO ' + tableName + ' (id,firmware,specifications,specific_software,rating,comments) VALUES ('+data+');'
	else:
		sqlInsertIntoTable = 'INSERT INTO ' + tableName + ' (id,name,version,auto_update) VALUES ('+data+');'
	
	cursor.execute(sqlInsertIntoTable)
	print 'Successfully inserted data.'

#############################
#	Function "updateDatabase"
#		Given the data to populate the database, it proceeds to do so. Prompts the user 
#		for information.
#############################
def updateDatabase():
	dbName = str(raw_input("Enter the name of the system: "))
	partName = str(raw_input("Is it hardware or software?: "))
	tableName = str(raw_input("Enter the name of the element type: "))

	tmp = str(raw_input("Enter the data to add ['FieldName1: new_value , FieldName2: new_value']: "))
		
	campos = validateData(tmp)

	sqlInsertIntoTable = ' INSERT INTO ' + tableName + ' ('+campos[0]+') VALUES ('+campos[1]+');'
	sqlUseDB = 'USE ' + dbName + ';'

	cursor.execute(sqlUseDB)
	cursor.execute(sqlInsertIntoTable)


#############################
#	Function "validateData"
#		Given the data, returns it with the correct formatting
#
#		@param tmp : the string to format
#		@return validated: the string formatted
#############################
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

con = mdb.connect('localhost', 'root', 'mysqlpass')
cursor = con.cursor()