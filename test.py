#!/usr/bin/python

import os, sys

from PIL import Image
#
#	Por defecto se usa el programa 'xv'. 
#	Si no se tiene instalado se puede usar 
#	"Eye of Gnome" (por defecto presente en Ubuntu).
#	Necesario hacer un alias:
#		"sudo ln -s /usr/bin/eog /usr/bin/xv"
#
im = Image.open("pruebaIm.jpg")
im.show()
print (im.format, im.size, im.mode)

"""
def addToTable(dbName, tableName, data, ident, part_name):

	sqlCheckData = 'SELECT * FROM ' + tableName + ' WHERE id="' + ident + '";'
	cursor.execute(sqlCheckData)
	row = str(cursor.fetchone())
	print '+++++++'
	print row
	if row == 'None':
		if part_name == 'hardware':
			sqlInsertIntoTable = 'INSERT INTO ' + tableName + ' VALUES ('+data+');'
		else:
			print 'Metiendo software'
			sqlInsertIntoTable = 'INSERT INTO ' + tableName + ' VALUES ('+data+');'
			print '*********'
			print sqlInsertIntoTable
			print '*********'
		
		cursor.execute(sqlInsertIntoTable)
		con.commit()

		print 'Successfully inserted data. Query: %s' % sqlInsertIntoTable
	else:
		pass


con = mdb.connect('localhost', 'root', 'mysqlpass')
cursor = con.cursor()


sqlUseDB = 'USE prueba1;'

cursor.execute(sqlUseDB)

addToTable('prueba1','ftp_client','"s81","None","None","None"','s81','software')
"""