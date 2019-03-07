#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Description:

	This file contains the implementation of the  MoniControl class, which: 
		*	performs measuraments (temperatures, state of wind-rain, time)
		*	saves the data of measurement
		*	performs control of relays, based on the measurements data.
		*	(optional) listens to certain ports and returns the requested 
			data to external clients


The MoniControl class: 

	class MoniControl():    
		def __init__(self):       # Constructor. Initialises the object. Sensors, GPIO, Save files etc. 	
		def get_data(self):       # get the values of temperatures from sensors
		def clean_and_exit(self): # close files, close GPIO etc
		def open_windows(self):
		def close_windows(self):
		def save_data(self):
		def control_ventilation(self):
		def switch_output_file(self):	
	
"""

import RPi.GPIO as GPIO			# GPIO functions
import time, datetime, sys, os  # system  and time functions
import imp  					# to read the variables from py files
from datetime import date, timedelta
import glob


class MoniControl():
	# constructor. Initialise things  (allocate memory)
	# has one argument, the name of the settings file.
	def __init__(self, settingsfname):
		
		self.ini_parameters(settingsfname)
		self.initialise_temperature_sensors()
		self.initialise_ventilation_devices()
		self.initialise_control_variables()
		self.initialise_wind_rain_monitoring()
		self.initialise_output()
		#self.initialise_server()
		
		print("	Constructor Done")

	def initialise_server(self):
		# This method starts thread, which listens to certain port at 
		# current address, to provide responces to the client software 
		# about the state of ventilatio.
		# Optionally, the server could be used to reset parameters of 
		# ventilation
		print ("	Server initialisation")


	def ini_parameters(self, settingsfname):
		# *********** Parameters Initialisation. ***********************
		# *********** From command line and from settings*.py **********
		# check wether output path is given as argument. 
		# set the current folder, if the argument is not specified:
		if (len(sys.argv)==2):
			self.opath  = sys.argv[1]	
		else:
			self.opath = os.getcwd() + "/"
		
		# define the path to the main script, which uses the MoniControl class
		# to get settings file from the same path:
		script_path = os.path.dirname(os.path.abspath(__file__))	
	
		# initialise all parameters from the settings class.
		settingsfullfname = script_path + "/" + settingsfname
		settingsfullfname = script_path + "/" + settingsfname

		self.P = imp.load_source('settings', settingsfullfname) # read Parameters
		
		print ("	Parameters Initialisation from file:" + settingsfullfname + " complite")
		
		#  ****** THE OBJECT self.P CONTAINS NOW ALL PARAMETRS *********
		#  **************** OF THE settings*.py file *******************
		#  *************************************************************


	def initialise_temperature_sensors(self):
		#  *****************   Sensors Initialisation ******************
		# ids are specified in the configuration files 
		# attention. the ini_parameters must be called befor the call 
		# of this function
		self.sensor_inside_id = self.P.sensor_inside_id     
		self.sensor_outside_id = self.P.sensor_outside_id   
 
		# Initialize the 1-wire 
		os.system('modprobe w1-gpio')  # Turns on the 1-wire GPIO module
		os.system('modprobe w1-therm') # Turns on the 1-wire temperature module
 
		# Finds the correct device file that holds the temperature data
		base_dir = '/sys/bus/w1/devices/'
		device_folder_sensor_inside = base_dir + self.sensor_inside_id 
		self.device_file_sensor_inside = device_folder_sensor_inside + '/w1_slave'

		device_folder_sensor_outside = base_dir + self.sensor_outside_id
		self.device_file_sensor_outside = device_folder_sensor_outside + '/w1_slave'

		print("	Sensors Initialisation complete")
		#  *************************************************************

	def initialise_ventilation_devices(self):
		# **************************************************************
		# initialise GPIO to control relays and to monitor state of pins. 
		GPIO.setmode(GPIO.BCM)  
		# Attention: some Relay moduls switch Relays on when voltage is Low, then use:
		self.RelaySwitchOn = GPIO.LOW
		self.RelaySwitchOff  = GPIO.HIGH
		# some Relay moduls switch Relays on when voltage is High, then use 
		#self.RelaySwitchOn = GPIO.HIGH
		#self.RelaySwitchOff = GPIO.LOW
		
		
		# Set the following GPIO pins as output pins:
		GPIO.setup(self.P.RelayK1ControlPin, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)
		GPIO.setup(self.P.RelayK2ControlPin, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)
		GPIO.setup(self.P.RelayK3ControlPin, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)

		# default state: ventillation off.
		GPIO.output(self.P.RelayK1ControlPin, self.RelaySwitchOff) # switch off ventillator		
		self.StateOfVentillator = 0 # 1 - on, 0 - off 
		# close phisical windows:
		self.close_windows() 
		# (i.e. no opening no closing phase is active after this operation)

		print("	GPIO for controlling Relay initialisation complete")
		# **************************************************************

	def initialise_wind_rain_monitoring(self):
		
		# ***************** Wind rain initialisation *******************
		# State read settings: 
		# The pin1 will be set as output pin and the state is set to 1 
		# The pin1 is connected via relay to pin2.
		# The relay is controlled via 220V of wind rain "phase"
		# The state of the pin2 is accordingly the state of wind rain automatic
		
		GPIO.setup(self.P.pin1, GPIO.OUT)
		GPIO.output(self.P.pin1, GPIO.HIGH) # 
		GPIO.setup(self.P.pin2, GPIO.IN, pull_up_down=GPIO.PUD_OFF) # Lesemodus
		print("	Wind Automation monitoring pins initialisation complete")
		# **************************************************************

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
		 
		# we artificially set self.lastSwitchOffTime back on self.MinOffTimeDateTime
		# to allow switch on praktically immediately after new start
		# default state is ventillator off. 

		# **************************************************************

	def initialise_output(self):
		# open first file with current time encoded in filename.
		NowTime = datetime.datetime.today()
		fname  = self.P.fileprefix + NowTime.strftime("%Y_%m_%d_%H_%M") + ".txt" # _%M
		self.f = open(self.opath + fname,'a') 

		print("	Output file" + self.opath + fname + " is open")


	# A function that reads the data of the temperature sensors. We need it, 
	# while sometimes, the need to reread the data is needed, to get complete data.
	def read_temp_raw(self):		

		f_inside = open(self.device_file_sensor_inside, 'r') # opens the temperature device file sensor inside				
		lines1 = f_inside.readlines() # Returns the text		
		f_inside.close()
		
		f_outside = open(self.device_file_sensor_outside, 'r') # Opens the temperature device file sensor 2
		lines2 = f_outside.readlines() # Returns the text
		f_outside.close()
		
		return lines1, lines2
	
	# get values of temperatures inside and outside from sensors, 
	# the state of windrain automation, the time of measurements. 
	def get_data(self):
		#reads the sensors data

		lines1, lines2 = self.read_temp_raw() # Read the temperatures from 'device files'

		# Convert the value of the sensor into a temperature 
		# While the first line does not contain 'YES', wait for 0.2s
		# and then read the device file again.
		while ((lines1[0].strip()[-3:] != 'YES')&(lines2[0].strip()[-3:] != 'YES')):
			time.sleep(0.2)
			lines1, lines2 = self.read_temp_raw()
 
		# Look for the position of the '=' in the second line of the
		# device file.
		equals_pos1 = lines1[1].find('t=')
		equals_pos2 = lines2[1].find('t=')

		# If the '=' is found, convert the rest of the line after the
		# '=' into degrees Celsius, then degrees Fahrenheit
		if ((equals_pos1 != -1) & (equals_pos2 != -1)):
			temp_string1 = lines1[1][equals_pos1+2:]
			self.t_inside = float(temp_string1) / 1000.0
			temp_string2 = lines2[1][equals_pos2+2:]
			self.t_outside = float(temp_string2) / 1000.0
			# temp_f = temp_c * 9.0 / 5.0 + 32.0

		# get the state of wind rain automation. 
		self.windRainState  = GPIO.input(self.P.pin2)	#GPIO.wait_for_edge(SCL, GPIO.RISING) # RISING BOTH	
			
		self.MeasurementTime = datetime.datetime.today() # time now


	def clean_and_exit(self):
		self.f.close()
		GPIO.output(self.P.RelayK1ControlPin, self.RelaySwitchOff) # switch off voltage from ventillator
		self.close_windows() 
		GPIO.output(self.P.RelayK2ControlPin, self.RelaySwitchOff) # switch to manual control		
		GPIO.output(self.P.RelayK3ControlPin, self.RelaySwitchOff) # 
		# self.free_server()
		GPIO.cleanup()	
		sys.stdout.flush()
		self.cleaned = 1
		sys.exit(0)

	def open_windows(self):
		print('Open Windows')
		GPIO.output(self.P.RelayK2ControlPin, self.RelaySwitchOn) # switch to automatic control
		GPIO.output(self.P.RelayK3ControlPin, self.RelaySwitchOn) # switch to opening phase
		time.sleep(self.P.OpeningTime) # wait till Windows are opened
		GPIO.output(self.P.RelayK2ControlPin, self.RelaySwitchOff) # switch to manual control
		GPIO.output(self.P.RelayK3ControlPin, self.RelaySwitchOff) # default state switch off of relay 3

	def close_windows(self):
		print('Close Windows')
		GPIO.output(self.P.RelayK2ControlPin, self.RelaySwitchOn)	# switch to automatic control
		GPIO.output(self.P.RelayK3ControlPin, self.RelaySwitchOff)	# switch to closing phase
		time.sleep(self.P.OpeningTime+10)							# wait till Windows are closed 
		GPIO.output(self.P.RelayK2ControlPin, self.RelaySwitchOff)	# switch to manual control
	
	def save_data(self):
		# Form string with date time, the values of temperatures inside, outside, the state of wind rain automation and the state of ventilator:
		OString = self.MeasurementTime.strftime("%d.%m.%Y %H:%M:%S")		
		# error can appear actually here during transformation from "None" to real value :
		OString= OString  + "	" +  "{:.2f}".format(self.t_inside) + "	" + "{:.2f}".format(self.t_outside) + "	" +  "{:.0f}".format(self.windRainState) + "	" + str(self.StateOfVentillator) + "\n"  # comment last summand if used with print	
		print(OString)
		self.f.write(OString) # output to file
		#f.flush()  #could be "reason" of demage of MicroSDs.  Comment it. No need to see current value in file immediately

	def control_ventilation(self):
		# since reading of data using long cable can cause errors sometimes, 
		# one needs to ignore this errors
		# To do it we will require, that condition is fulfilled at least several times
		# counted by counters joffok and jonok, they are set to zeroes in 
		# constructor initially
		
		# because of insekts, we set in settings file normally 
		# the ventilation between StartTime and EndTime every day
		
		# "hour" of the time of measurements:
		
		tm = int(self.MeasurementTime.strftime("%H")) #%H %M  
		
		# The following conditions must be satisfied, to open windows 
		# and start ventilation:
		
		mainOnCondition = (self.t_inside - self.t_outside) > self.P.TdifferenceOn 
		# the difference of temperatures outside and inside reached the desired value. 
		# to start ventilation only, if it makes sence. 
		
		tMinCondition = self.t_inside > self.P.Tmin
		# The temperature inside is higher, than some reasonable for people Tmin value
		
		timeCondition = ((tm>=self.P.StartTime)&(tm<=self.P.EndTime))
		# the ventilation only in certain time interval nights, to prevent insects problem
		
		#  Check of the Wind Rain must be added.
		windRainCondition = self.windRainState

		# check, that the last switch off was not too short time ago:
		Now = datetime.datetime.today()
		minOffTimeCondition = (Now-self.lastSwitchOffTime)>self.MinOffTimeDateTime
		
		# add to switchon counter, if all conditions are satisfied:
		if ( mainOnCondition & timeCondition & tMinCondition & minOffTimeCondition):
			self.jonok = self.jonok + 1
			self.joffok = 0  # start to count again
		
		# The following conditions must be satisfied, to switch off 
		# ventilation:
		
		mainOffCondition = (self.t_inside - self.t_outside)<self.P.TdifferenceOff		
		# the difference of temperatures is less than TdifferenceOff

		# add to switchoff counter, if all conditions are satisfied:
		if (mainOffCondition | (not tMinCondition) | (not timeCondition)): 
			self.joffok = self.joffok + 1
			self.jonok = 0  # start to count again
		
		if ((self.jonok>5)&(windRainCondition)):  # 5 measuraments, condition to switch on is satisfied. 						
							# then 'switch on' ventilation
			if (self.StateOfVentillator==0):
				self.open_windows()
				GPIO.output(self.P.RelayK1ControlPin, self.RelaySwitchOn) # switch on ventillation
				self.StateOfVentillator = 1
			jonok = 0 
		
		
		# switch off of ventilator must be done immidiately as soon as 
		# wind or rain was detected!
		if ((self.joffok>5)|(not windRainCondition)): # 5 measuraments, condition to switch off is satisfied. 
			if (self.StateOfVentillator==1): # i.e. now is switch off event
											 # switch off make sense only if ventillator was on
				GPIO.output(self.P.RelayK1ControlPin, self.RelaySwitchOff) # switch off voltage of ventillator(s)
				self.close_windows()
				self.lastSwitchOffTime = datetime.datetime.today()
				self.StateOfVentillator = 0
			self.joffok = 0 
		

	# to prevent the loss of data, the data are writen into new file
	# after some timeinterval e.g. every day or hour etc.
	def switch_output_file(self):
		self.f.close()
		fname  = self.P.fileprefix + self.MeasurementTime.strftime("%Y_%m_%d_%H_%M") + ".txt" # _%M				
		self.f = open(self.opath + fname, 'w')
