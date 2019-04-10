#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# usage: 

# sudo python /home/pi/Steuerung-Monitoring/initialiseSQL.py /home/pi/Steuerung-Monitoring/

# The default username is 'root' and by default there is no password.
# So, no problem to initialize the database, since monicontrol - server 
# works under root rights

# The Web-layer works however under restricted rights and the user runner
# is created specially for this layer. 

# This script checks wether the database exists.
# if not, then it creates it and fills its Table Parameters with the 
# Parameternames and values taken from settingsMC.py file. 
# there are also some test functions

# Below are sql requests to configure mysql database manually using e.g. 
# commandline mysql client:

#show databases;
#drop user runner;
#drop database AirCoCo;


#CREATE DATABASE AirCoCo;
#use AirCoCo 
#CREATE TABLE Parameters(Id INT PRIMARY KEY AUTO_INCREMENT, ParameterName CHAR(255), ParameterValue CHAR(255));
#INSERT INTO AirCoCo.Parameters(ParameterName, ParameterValue) 
#VALUES
#('abc','15'),
#('def','16');
#CREATE USER 'runner' IDENTIFIED BY 'runner123';"
#GRANT ALL PRIVILEGES ON AirCoCo.* TO 'runner';"
#select * from AirCoCo.Parameters order by id desc limit 50; 

import imp  					# to read the variables from py files
import MySQLdb
import sys, os
from SQLParameters import *

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


def push_settings_into_SQL(SQL, settingsfullfname):
	P = imp.load_source('settings', settingsfullfname) # read Parameters
	list_of_param = P.__dict__.keys() # list of all the members of the class
	list_of_values = P.__dict__.values() # list of all the members of the class

	command = "INSERT INTO %s.%s (ParameterName,ParameterValue) VALUES "% (SQL.Database, SQL.Table)
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

# ======================================================================
# Here, the automated SQL Request to create Database: 
def create_database(SQL, settingsfullfname):
	# works only if it does not exist
	try:
		con = MySQLdb.connect(SQL.Server, SQL.User, SQL.Passwd, SQL.Database)
		cur = con.cursor()
		command = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME='%s';"%SQL.Database
		#command = "select * from Datenerfassung.uploads;"		
		cur.execute(command)
		# fetch all of the rows from the query
		data = cur.fetchall()
		con.close()
		if (len(data)>0):
			# database exists.
			pass
	except:
		# Database does not exist create it:
		command = "CREATE DATABASE " + SQL.Database + ";"
		print(command)
		con = MySQLdb.connect(SQL.Server, SQL.User, SQL.Passwd)
		cur = con.cursor()
		cur.execute(command)
		command = "CREATE TABLE " + SQL.Database + ".Parameters(Id INT PRIMARY KEY AUTO_INCREMENT, ParameterName CHAR(255), ParameterValue CHAR(255));"
		cur.execute(command)		
		command = "CREATE USER 'runner' IDENTIFIED BY 'runner123';" # to be used in web		
		cur.execute(command)
		command = "GRANT ALL PRIVILEGES ON " + SQL.Database + ".* TO 'runner';"
		cur.execute(command)
		con.close()
		
		push_settings_into_SQL(SQL, settingsfullfname)

	print("===============")

SQL = SQLPar()
settingsfullfname = "settingsMC.py"

if (len(sys.argv)==2):
	opath  = sys.argv[1]	
else:
	opath = os.getcwd() + "/"

settingsfullfname = opath + settingsfullfname

#SQL_test(SQL)
#settings_test(settingsfullfname)
create_database(SQL, settingsfullfname)



