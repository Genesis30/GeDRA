#!/usr/bin/python

import os, sys

"""
mu = [[0]*2 for i in range(5)]
w  = [0]*5
mk = [[0]*2 for i in range(5)]
"""
mu = [[0.6,0.3],[0.55,0.40],[0.7,0.1],[0.9,0.05],[0.61,0.38]]
w = [0,1.3,1.22,0.3,1.4]
mk = [[0.0]*2 for i in range(5)]
PIDS0 = 2

print '----------------------'
print mu
print '----------------------'
print w
print '----------------------'
print mk
print '----------------------'

for i in range(5):
	for j in range(2):
		if j == 0:
			
			mk[i][j] = mu[i][j] / ( mu[i][j] + mu[i][j+1] + 1 - w[i] * PIDS0)
			print '*********'
			print mk[i][j]
			print '*********'
		else:
			
			mk[i][j] = mu[i][j] / ( mu[i][j] + mu[i][j-1] + 1 - w[i] * PIDS0)

print mk


"""
from PIL import Image

def createImage(systemName):
	imagesPath = str(os.getcwd()) + '/images/'
	print imagesPath

def loadImage():
	imagesList = []
	imagesPath = str(os.getcwd()) + '/images/'
	
	for image in os.listdir(imagesPath):
		temp = imagesPath + image
		imageName = Image.open(temp)
		imagesList.append(imageName)


loadImage()

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