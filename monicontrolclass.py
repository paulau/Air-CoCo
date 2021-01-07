#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Description:
	This file contains the implementation of the adstract class, to be used
	for monitoring and control algorithm. Also, the base functionality 
	which is equal for different children classes. But sure, can be also 
	different and overloaded.
"""

import RPi.GPIO as GPIO			# GPIO functions
import time, datetime, sys, os  # system  and time functions
import imp							# to read the variables from py files
from datetime import date, timedelta
import glob
#from getsettingsfromSQL import *
from sensorAir import *
import MySQLdb
from SQLParameters import *




class MoniControlBase:
	# constructor. Initialise things  (allocate memory)
	# has one argument, the name of the settings file.
	def __init__(self, settingsfname):

		# define the path to the main script, which uses the MoniControl class
		# to get settings file from the same path:
		self.script_path = os.path.dirname(os.path.abspath(__file__))

		#sqlinit of all tables is needed
		#CREATE TABLE Datenerfassung.uploads(Id INT PRIMARY KEY AUTO_INCREMENT, FullFileNameToUpload VARCHAR(255), FTPUser VARCHAR(30), FTPPassword VARCHAR(30),  FTPFolderToUpload VARCHAR(255));
		#GRANT ALL PRIVILEGES ON Datenerfassung.* TO 'logger'; 
		#exit;

		# FAST regime to think about. ???
		# if FAST then system will not Save into files or into usual Datenerfassung.RHTCO2
		# it will store into FAST table instead. 

		if (settingsfname.find('.')!=-1 ):
			self.ini_parameters(settingsfname)
			#if filename is given, then read parameters from file
			#else (if SQL Identification word is given), then read from sql
		else:
			time.sleep(10) 
			#wait nearly 1 min till mysql server is started
			self.ini_parameters_mysql(settingsfname)
			


		# set the current folder, if the outputfolder for output files is not specified
		# in settings fiele:
		if hasattr(self.P, 'outputfolder'):
			self.opath  = self.P.outputfolder
		else:
			self.opath = os.getcwd() + "/"

		self.initialise_ventilation_devices()
		self.initialise_control_variables()
		self.initialise_output()
		# the following codeline is just to initialise variable for the case
		# if it is needed immediately for requests to the server
		self.OString = "01.01.2000 00:00:00	00.00	00.00	0	0	0"
		self.auto = 1
		print("	Base Constructor Done")

	def ini_parameters(self, settingsfname):
		# *********** Parameters Initialisation. ***********************
		# *********** From command line and from settings*.py **********

		# initialise all parameters from the settings class.
		settingsfullfname = self.script_path + "/" + settingsfname
		self.P = imp.load_source('settings', settingsfullfname) # read Parameters
		print("	Parameters Initialisation from file:" + settingsfullfname + " complete")
		
		# Some Parameters are needed anyway. If they are not defined, one needs to define them
		# default Settings:
		
		if (not hasattr(self.P, 'SaveInterval')):
			self.P.SaveInterval = "%d" # save each day if nothing is specified  #%M  %H

		
		#  ****** THE OBJECT self.P CONTAINS NOW ALL PARAMETRS *********
		#  **************** OF THE settings*.py file *******************
		#  *************************************************************

	def ini_parameters_mysql(self, settingsname): 
		print("	parametrs from sql will now be initialised")
		
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
			pydictionary[data[i][1]] = data[i][2] # generally, all variables are strings, but:
			try:  # it can be float
				pydictionary[data[i][1]] = float(data[i][2])
			except:
				pass 
				
			try:  # it can be int
				pydictionary[data[i][1]] = int(data[i][2])
			except:
				pass 
				
			try:  # it can be expression
				pydictionary[data[i][1]] = eval(data[i][2])
			except:
				pass 

		PP = type("PP", (), pydictionary)
		self.P = PP() # ParametersFromSQL(settingsname)		
		print("	parametrs from sql are initialised")
		#  ****** THE OBJECT self.P CONTAINS NOW ALL PARAMETRS *********

	def initialise_ventilation_devices(self):
		pass 
		
	def initialise_control_variables(self):
		# ****************  Control variables:  ************************
		# The following two variables are used in control_ventilation 
		# method of the current class. See additional explanations of 
		# the followung variables there. 
		self.jonok = 0  # the number of measurements, for which the switch on condition is satisfied. 
		self.joffok = 0 # the number of measurements, for which the switch off condition is satisfied. 

		# To avoid fast switch on - off(close-open windows), we require, that 
		# the new ventilation must not be started earlier than in self.P.MinOffTime
		# minutes after previous "close_windows"
		
		self.MinOffTimeDateTime = timedelta(minutes=self.P.MinOffTime) # just tipe conversion!!!
		self.lastSwitchOffTime = datetime.datetime.today() - self.MinOffTimeDateTime 
		
		print("	initialise_control_variables of Base class")
		 
		# we artificially set self.lastSwitchOffTime back on self.MinOffTimeDateTime
		# to allow switch on praktically immediately after new start
		# default state is ventillator off. 
		# **************************************************************

	def initialise_output(self):
		# open first file with current time encoded in filename.
		NowTime = datetime.datetime.today()
		self.fileextension = ".std" # ".txt" # std (sensor text data) 10.01.2018
									# to avoid 1000s of txt file on filesystem.
									# it can make the search of info more fiddicult
		
		self.fname  = self.P.fileprefix + NowTime.strftime("%Y_%m_%d_%H_%M") + self.fileextension # ".txt" # _%M
		self.f = open(self.opath + self.fname,'a')
		print("	Output file" + self.opath + self.fname + " is open")

	# get values of physical parameters. 
	# Just interface here for children classes
	# must be redefined in child classes:
	# see for abstract class https://www.python-course.eu/python3_abstract_classes.php
	def get_data(self):
		#pass
		self.sensor_in.get_data()
		self.sensor_out.get_data()
		self.t_inside = self.sensor_in.t		# get temperature inside
		self.t_outside = self.sensor_out.t		# get temperature outside
		self.MeasurementTime = datetime.datetime.today() # get time now
		

	def clean_and_exit(self):
		self.f.close()
		
		#if (hasattr(self.P, 'uploadstable')):# if defined uploadstable, the use it instead of 
		#								# prefixes of files to set information about files
		#	try:
		#		SQLsendFName(self.P.SQLserver, self.P.SQLuser, self.P.SQLpw, 'uploads', self.opath + self.fname, self.P.ftpbenutzer, self.P.ftppasswort, self.P.FTPfolder)
		#	except:
		#		pass

		
		self.stop_ventilation()
		GPIO.cleanup()
		sys.stdout.flush()
		#sys.exit(0)
		os._exit(0)


	def stop_ventilation(self):
		GPIO.output(self.P.RelayK1ControlPin, self.RelaySwitchOff) # switch off voltage from ventillator
		self.StateOfVentillator = 0 # just information bit, which shows the state of ventillation. 
									# must be always set at change of ventilation
									# 1 - on, 0 - off 
	def start_ventilation(self):
		GPIO.output(self.P.RelayK1ControlPin, self.RelaySwitchOn) # switch off voltage from ventillator
		self.StateOfVentillator = 1 # just information bit, which shows the state of ventillation. 
									# must be always set at change of ventilation
									# 1 - on, 0 - off 

	
	def save_data(self):
		pass
		
	def control_ventilation(self):
		pass

	# to prevent the loss of data, the data are writen into new file
	# after some timeinterval e.g. every day or hour etc.
	# depending on parameter  P.SaveInterval   %d %M  %H

	def switch_output_file(self):
		self.visualise_data()
		self.f.close()
		
		## if (hasattr(self.P, 'uploadstable')):
		# if defined uploadstable, then we use it 
		# (send record with filename into uploadstable)
		# instead of current_ prefix of files to set information about files
		## 	try:
		## 		SQLsendFName(self.P.SQLserver, self.P.SQLuser, self.P.SQLpw, 'uploads', self.opath + self.fname, self.P.ftpbenutzer, self.P.ftppasswort, self.P.FTPfolder)
		## 	except:
		## 		pass
		
		self.fname  = self.P.fileprefix + self.MeasurementTime.strftime("%Y_%m_%d_%H_%M") + self.fileextension # ".txt" # _%M
		self.f = open(self.opath + self.fname, 'w')

	# the same script will be used for vsualisation now and for visualisation 
	# in the end of each day:
	def visualise_data(self, targetpicfname = ''):
		if hasattr(self.P, 'webfolder'):
			self.f.flush()
			# visualise data:
			excommand  = 'python ' + self.script_path + '/visu.py' +  ' ' + self.opath + ' ' + self.fname
			os.system(excommand)
			print(excommand)
			# move visualisation files to web folder:
			fnamedata = self.opath + self.fname
			fnamepic = fnamedata.replace("std", "png")
			
			if (len(targetpicfname) < 2) :
				excommand = 'mv ' + fnamepic + " " + self.P.webfolder
			else: 
				excommand = 'mv ' + fnamepic + " " + self.P.webfolder + targetpicfname
				
			os.system(excommand)
			print(excommand)

			## move visualisation files to web folder and give new name current.png:
			#pngname = self.fname.replace('.txt', '.png')
			#excommand = 'mv ' + self.opath + pngname + ' ' + self.P.webfolder + 'current.png'
			

	def send_notification(self, emsg):
		if hasattr(self.P, 'emailsto'):
			from sndemail import *
			import socket
			esbj = 'Mitteilung von: ' + socket.gethostname()
			
			for emailto in self.P.emailsto:
				sndemail(emailto, self.P.emailfrom, self.P.mailserver, self.P.passwmail, esbj, emsg)

	def set_server_responce_message(self):
		# this method must be actually adjusted in child classes for corresponding use
		return "Must be redefined in child class"
	
	# see comments near GetDeviceName function in ventserver of daodeviceserver.php
	def get_device_name(self):
		return self.__class__.__name__;
		#"each child class must redefine this text as its own name";
	

def set_bit(intvalue, bit, boolval):
	if boolval:
		returnvalue = intvalue | (1<<bit)
	else:
		returnvalue = intvalue & ~(1<<bit)
		
	return returnvalue
