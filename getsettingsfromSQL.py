#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import MySQLdb
from SQLParameters import *

class ParametersFromSQL():
	def __init__(self):
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
		
		pydictionary = {}
		for i in range(0,len(data)):
			pydictionary[data[i][1]] = data[i][2]
		
		self.TdifferenceOff         = float(pydictionary['TdifferenceOff'])
		self.internettype           = int(pydictionary['internettype'])
		self.fileprefix             = pydictionary['fileprefix']
		self.sensor_outside_id      = pydictionary['sensor_outside_id']
		self.ftppasswort            = pydictionary['ftppasswort']
		self.LoggingInterval        = float(pydictionary['LoggingInterval'])
		self.RelayK1ControlPin      = int(pydictionary['RelayK1ControlPin'])
		self.EndTime                = int(pydictionary['EndTime'])
		self.SaveInterval           = pydictionary['SaveInterval']
		self.GPIOcontactDataInside  = int(pydictionary['GPIOcontactDataInside'])
		self.Tmin                   = float(pydictionary['Tmin'])
		self.sensor_inside_id       = pydictionary['sensor_inside_id']
		self.OpeningTime            = int(pydictionary['OpeningTime'])
		self.UploadRate             = int(pydictionary['UploadRate'])
		self.RelayK2ControlPin      = int(pydictionary['RelayK2ControlPin'])
		self.ftpbenutzer            = pydictionary['ftpbenutzer']
		self.FTPfolder              = pydictionary['FTPfolder']
		self.description            = pydictionary['description']
		self.GPIOcontactDataOutside = int(pydictionary['GPIOcontactDataOutside'])
		self.TdifferenceOn          = float(pydictionary['TdifferenceOn'])
		self.ftpserveraddr          = pydictionary['ftpserveraddr']
		self.MinOffTime             = int(pydictionary['MinOffTime'])
		self.RelayK3ControlPin      = int(pydictionary['RelayK3ControlPin'])
		self.StartTime              = int(pydictionary['StartTime'])
		self.pin2                   = int(pydictionary['pin2'])
		self.pin1                   = int(pydictionary['pin1'])
