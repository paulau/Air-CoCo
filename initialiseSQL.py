#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#the default username is 'root' and by default there is no password.

# This script checks wether the database AirCoCo exists.
# if not, then it creates it and fills its Table Parameters with the 
# Parameternames and values taken from settingsMC.py file. 
# there are also some test functions

#Beloe are sql requests to configure mysql database manually


#show databases;
#CREATE DATABASE AirCoCo;
#use AirCoCo 
#CREATE TABLE Parameters(Id INT PRIMARY KEY AUTO_INCREMENT, ParameterName CHAR(255), ParameterValue CHAR(255));
#INSERT INTO AirCoCo.Parameters(ParameterName, ParameterValue) 
#VALUES
#('abc','15'),
#('def','16');
#select * from AirCoCo.Parameters order by id desc limit 10; 

import imp  					# to read the variables from py files
import MySQLdb

#the default username is 'root' and by default there is no password.
class SQLPar():
	def __init__(self):
		Server = 'localhost'	
		User = 'root'
		Passwd = ''
		Database = 'AirCoCo'
		Table = 'Parameters'

SQL = SQLPar()

settingsfullfname = "settingsMC.py"

def exequte_sql_request(SQL, command):
	con = MySQLdb.connect(SQL.Server,SQL.User,SQL.Passwd,SQL.Database)
	with con:
		cur = con.cursor()
		cur.execute(command)
		cur.close()
		con.commit()
	con.close()

def SQL_test(SQL):
	command = "INSERT INTO %s.%s (ParameterName,ParameterValue) VALUES (%s,%s)"% (SQL.Database, SQL.Table, '"Test1"', '"Test1Value"')
	print(command)
	exequte_sql_request(SQL, command)	
	print(" ")
	print("=============================================================")

def settings_test(settingsfullfname):
	P = imp.load_source('settings', settingsfullfname) # read Parameters
	list_of_param = P.__dict__.keys() # list of all the members of the class
	list_of_values = P.__dict__.values() # list of all the members of the class
	
	i=0
	while (i<len(list_of_param)):
		if ((list_of_param[i][0:2]) <> '__'): # eliminate sppecial members, which are not ours
			print(list_of_param[i] + " " + str(list_of_values[i]))
		i = i + 1
	print(" ")
	print("=============================================================")


def check_if_mysql_database_and_table_exists(SQL):
	try:
		con = MySQLdb.connect(SQLServer, SQLUser, SQLPasswd, SQLDatabase)
		cur = con.cursor()
		command = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME='%s';"%SQLDatabase
		#command = "select * from Datenerfassung.uploads;"		
		cur.execute(command)
		# fetch all of the rows from the query
		data = cur.fetchall()
		if (len(data)>0):
			# database exists.
			
			
	except:
		# Database does not exist create it:
		command = "CREATE DATABASE AirCoCo;"
		
	print(len(data))
	print("===============")

def push_settings_into_SQL(SQL, settingsfullfname):
	P = imp.load_source('settings', settingsfullfname) # read Parameters
	list_of_param = P.__dict__.keys() # list of all the members of the class
	list_of_values = P.__dict__.values() # list of all the members of the class

	command = "INSERT INTO %s.%s (ParameterName,ParameterValue) VALUES "% (SQLDatabase, SQLTable)
	i=0
	while (i<len(list_of_param)):
		if ((list_of_param[i][0:2]) <> '__'): # eliminate sppecial members, which are not ours
			pars = "('" + list_of_param[i] + "', '" + str(list_of_values[i]) + "')"
			if (i<len(list_of_param)-1):
				pars = pars +","
			else:
				pars = pars +";"
					
			print(list_of_param[i] + " " + str(list_of_values[i])) 
			command = command + pars
		i = i + 1
    #print("")
	#print(command)

	exequte_sql_request(SQL, command)
	
	print(" ")
	print("=============================================================")


SQL_test(SQL)
#settings_test(settingsfullfname)
#push_settings_into_SQL(SQLServer, SQLUser, SQLPasswd, SQLDatabase, SQLTable, settingsfullfname)
#check_if_mysql_database_and_table_exists(SQLServer, SQLUser, SQLPasswd, SQLDatabase, SQLTable)

# ======================================================================

# Here, the automated SQL Request to create Database: 


