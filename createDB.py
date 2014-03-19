#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys

def createDB(dbName):
	sqlCreaDB = 'CREATE DATABASE ' + dbName + ';'
	cursor.execute(sqlCreaDB)
	print 'Creado %s con exito' % dbName
	
def createPartTable(dbName, tableName):
	sqlUsaDB = 'USE ' + dbName + ';' 

	sqlCreaTabla = 'CREATE TABLE ' + tableName + '(name varchar(30) PRIMARY KEY);'
	print sqlCreaTabla
	cursor.execute(sqlUsaDB)

	cursor.execute(sqlCreaTabla)
	print 'Creada tabla %s con exito' % tableName

def createElementTable(dbName, tableName):
	sqlUsaDB = 'USE ' + dbName + ';' 

	sqlCreaTabla = 'CREATE TABLE ' + tableName + '(name varchar(30) PRIMARY KEY);'
	print sqlCreaTabla
	cursor.execute(sqlUsaDB)

	cursor.execute(sqlCreaTabla)
	print 'Creada tabla %s con exito' % tableName

def addToTable(dbName, tableName, id, data):
	#print 'Add %s con exito' % data
	return

con = mdb.connect('localhost', 'root', 'mysqlpass')
cursor = con.cursor()
