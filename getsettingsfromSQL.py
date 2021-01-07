#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import MySQLdb
from SQLParameters import *

class ParametersFromSQL:
	def __init__(self, settingsname):
		SQL = SQLPar() # here are all sql settings
		con = MySQLdb.connect(SQL.Server, SQL.User, SQL.Passwd, SQL.Database)
		cur = con.cursor()
		command = "SELECT * FROM "+SQL.Database+".Parameters;"
		cur.execute(command)
		# fetch all of the rows from the query
		data = cur.fetchall()
		con.close()
		
		# database exists. 
		# first direct initialisation of all parameters. 
		# may be later better:
		#print pydictionary		
		
		self.pydictionary = {}
		for i in range(0,len(data)):
			self.pydictionary[data[i][1]] = data[i][2]
			
		if (settingsname=="settingsMCSQL"):
			self.set_system_A()
		if (settingsname=="settingsMC-LadenSQL"):
			self.set_system_B()
		if (settingsname=="settingsRHTCO2SQL"):
			self.set_system_C()
			
			
	def set_system_A(self):
		
		self.OpeningTime            = int(self.pydictionary['OpeningTime'])
		
		self.sensor_inside_id       = self.pydictionary['sensor_inside_id']
		self.sensor_outside_id      = self.pydictionary['sensor_outside_id']

		self.RelayK1ControlPin      = int(self.pydictionary['RelayK1ControlPin'])
		self.RelayK2ControlPin      = int(self.pydictionary['RelayK2ControlPin'])
		self.RelayK3ControlPin      = int(self.pydictionary['RelayK3ControlPin'])



		self.LoggingInterval        = float(self.pydictionary['LoggingInterval'])
		self.fileprefix             = self.pydictionary['fileprefix']
		self.SaveInterval           = self.pydictionary['SaveInterval']

		self.TdifferenceOn          = float(self.pydictionary['TdifferenceOn'])
		self.TdifferenceOff         = float(self.pydictionary['TdifferenceOff'])

		self.Tmin                   = float(self.pydictionary['Tmin'])
		self.MaxHumidity            = float(self.pydictionary['MaxHumidity'])


		self.MinOffTime             = int(self.pydictionary['MinOffTime'])
		self.StartTime              = int(self.pydictionary['StartTime'])
		self.EndTime                = int(self.pydictionary['EndTime'])

		self.pin1                   = int(self.pydictionary['pin1'])
		self.pin2                   = int(self.pydictionary['pin2'])

		self.internettype           = int(self.pydictionary['internettype'])
		self.FTPfolder              = self.pydictionary['FTPfolder']
		self.description            = self.pydictionary['description']

		self.ftpserveraddr          = self.pydictionary['ftpserveraddr']
		self.ftpbenutzer            = self.pydictionary['ftpbenutzer']
		self.ftppasswort            = self.pydictionary['ftppasswort']

		self.UploadRate             = int(self.pydictionary['UploadRate'])
		self.webfolder              = self.pydictionary['webfolder']
		self.outputfolder           = self.pydictionary['outputfolder']
		self.emailsto               = eval(self.pydictionary['emailsto'])
		self.emailfrom              = self.pydictionary['emailfrom']
		self.mailserver             = self.pydictionary['mailserver']
		self.passwmail              = self.pydictionary['passwmail']

	def set_system_B(self):
		# set of parameters for system B
		pass
		
	def set_system_C(self):
		# set of parameters for system C
		pass
		
