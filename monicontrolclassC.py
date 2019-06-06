#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Description: Code for the system for logging, controlling, and CO2-Ampel, based on:
Temperature: K30 CO2 Sensor
Temperature and humidity: DHT22
Optionally: HYT
PWM modul and ventilator
"""

from monicontrolclass import *  			# Base monicontrol logger-controller class

# import only if SQL variables are defined.
#if (hasattr(self.P, 'SQLuser')):

# attention! must be installed!!!
# apt-get install python-mysqldb
#from SQLsendFName import SQLsendFName
#import MySQLdb



class MoniControlC(MoniControlBase):
	def __init__(self, settingsfname):
		MoniControlBase.__init__(self,settingsfname)  #let the constructor of parent class run
		self.initialise_output_header()

		if (hasattr(self.P, 'CO2_ADDR')):
			self.CO2_ADDR = self.P.CO2_ADDR
		else:
			self.CO2_ADDR = 0x68
			
		self.sensor_co2 = SensorCO2(self.CO2_ADDR)
		self.sensor_DHT = SensorDHT(self.P.GPIOVoltagePin, self.P.DHTDataPin)

		print("gpio set as out")
		if (hasattr(self.P, 'VentControlPin')):
			GPIO.setup(self.P.VentControlPin, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN) 
											# pull down to allways off if not active
		print("c constr done")

	def initialise_output_header(self):
		pass

	def initialise_ventilation_devices(self):
		# **************************************************************
		# initialise GPIO to control relays and to monitor state of pins. 
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)  
		# Attention: some Relay moduls switch Relays on when voltage is Low, then use:
		#self.RelaySwitchOn = GPIO.LOW
		#self.RelaySwitchOff  = GPIO.HIGH
		
		# some Relay moduls switch Relays on when voltage is High, then use 
		self.RelaySwitchOn = GPIO.HIGH
		self.RelaySwitchOff = GPIO.LOW
		# Set the following GPIO pins as output pins:
		GPIO.setup(self.P.RelayK1ControlPin, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)		
		self.stop_ventilation()  		# default state: ventillation off.
		print("	GPIO for controlling Relay initialisation complete")
		# **************************************************************


	def initialise_control_variables(self):
		MoniControlBase.initialise_control_variables(self)
		# ------------- if control setting is defined in settings file, --------
		# ------------------------- then use it! -------------------------------
		if (hasattr(self.P, 'RelayK1ControlPin')):
			#print("RelayK1ControlPin is initialized")
			GPIO.setup(self.P.RelayK1ControlPin, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)
			if (not hasattr(self.P, 'CO2Limit')):
				self.CO2Limit = 1200
			else: 
				self.CO2Limit = self.P.CO2Limit	
		
		
		
		self.controlscount = 0
		
		
		
		# note, that CO2LimitOff must be defined and less than CO2Limit 
		# to perform discrete (on -off ventilator) control of ventilation
		
		if (not hasattr(self.P, 'CO2LimitOff')):
			self.CO2LimitOff = 600
		else: 
			self.CO2LimitOff = self.P.CO2LimitOff	
				
		
		if (hasattr(self.P, 'CO2LimitOff')) & (hasattr(self.P, 'VentControlPin')):
			if (self.CO2LimitOff < self.CO2Limit):
				self.controlVentCondition = True
			else:
				self.controlVentCondition = False
				

	def get_data(self):
		self.MeasurementTime = datetime.datetime.today() # get time now
		self.h, self.t = self.sensor_DHT.get_data()
		self.co2Val = self.sensor_co2.get_co2()



	# ATTENTION !!! IT MUST BE CALLED ONLY AFTER GET DATA!!!!    :
	def save_data(self):
		# output to file will be done always    
		
		# Form string with date time, the values of temperatures, CO2, Humidity
		# and the state of ventilator:
		self.OString = self.MeasurementTime.strftime("%d.%m.%Y %H:%M:%S")		
		# error can appear actually here during transformation from "None" to real value :
		self.OString = self.OString + "	" + "{:.2f}".format(self.h) 
		self.OString = self.OString + "	" + "{:.2f}".format(self.t) 
		self.OString = self.OString + "	" + "{:.2f}".format(self.co2Val) 
		self.OString = self.OString + "	" + str(self.StateOfVentillator) 
		self.OString = self.OString + "\n"  # comment last summand if used with print	
		sys.stdout.write(self.OString) 
		self.f.write(self.OString) # output to file
		# ================================================================


	# Actually, control of ventilation should work a bit differently from the control of lights
	# for example, the ventilator switches on off too often
	# One needs to have additional Parameter CO2LimitOff
	def control_ventilation(self):
		self.control_lights()
		if self.auto:
			if self.controlVentCondition:
				if (self.co2Val>self.CO2Limit): 
					self.jonok = self.jonok + 1
				else:
					self.jonok = 0
				
				if (self.co2Val<self.CO2LimitOff): 
					self.joffok = self.joffok + 1
				else:
					self.joffok = 0
			
				if (self.jonok>3): # if it is confirmed several times                     
					self.start_ventilation()
			
				if (self.joffok>3): # if it is confirmed several times                     
					self.stop_ventilation()


	# ATTENTION !!! IT MUST BE CALLED ONLY AFTER GET DATA!!!!
	def control_lights(self):
		if (hasattr(self.P, 'RelayK1ControlPin')):
			if (self.co2Val>self.CO2Limit): 
				self.controlscount = self.controlscount + 1
			else:
				self.controlscount = 0
				
			if (self.controlscount>3): # if it is confirmed several times     
				GPIO.output(self.P.VentControlPin, GPIO.HIGH)
			else:
				GPIO.output(self.P.VentControlPin, GPIO.LOW)  # test, how it works

	def set_server_responce_message(self):
		# responce in json format
		# to avoid usage of the same variables from different threads
		# we stay at usage of Ostring and we extract the data from the str
		
		tmpstr = self.OString
		jsonstr = '{'
		jsonstr = jsonstr + '"datetime":"' + tmpstr.split('\t')[0] + '",'
		jsonstr = jsonstr + '"h":' + tmpstr.split('\t')[1] + ','
		jsonstr = jsonstr + '"t":' + tmpstr.split('\t')[2] + ','
		jsonstr = jsonstr + '"co2":' + tmpstr.split('\t')[3] + ','
		jsonstr = jsonstr + '"FanState":' + tmpstr.split('\t')[4] 
		jsonstr = jsonstr + '}'
		
		return jsonstr

