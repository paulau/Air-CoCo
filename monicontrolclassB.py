#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Description: Code for the system based on:
one DS18B20 Temperature sensor
one SHT 31-D Temperature and  humidity sensor
Relay 
"""

from monicontrolclass import *  			# Base monicontrol logger-controller class

class MoniControlB(MoniControlBase):
	def __init__(self, settingsfname):		
		MoniControlBase.__init__(self,settingsfname)  #let the constructor of parent class run
		self.initialise_output_header()
		self.sensor_in = SensorDS18B20(self.P.sensor_inside_id)
		self.sensor_out = sensorSHT31D(self.P.sensor_outside_id)

	def initialise_output_header(self):
		# creates header file for the output files		
		# The methods save_data, set_server_responce_message initialise_output_header
		# must be adjusted sinchronously!!
		
		fheadername  = self.P.fileprefix + self.fileextension 
		fheader = open(self.opath + fheadername,'w')
		OString = "datetime"
		OString = OString + "	" + "tin"
		OString = OString + "	" + "tout"
		OString = OString + "	" + "FanState"
		OString = OString + "	" + "hout"
		OString = OString + "\n"  # comment last summand if used with print	
		fheader.write(OString) # output to file
		fheader.close()

	def get_data(self):
		self.sensor_in.get_data()
		self.sensor_out.get_data()
		self.t_inside = self.sensor_in.t		# get temperature inside
		self.t_outside = self.sensor_out.t		# get temperature outside
		self.MeasurementTime = datetime.datetime.today() # get time now
		self.h_outside = self.sensor_out.h		# get humidity outside  ! may be undefined! check!

	def save_data(self):
		# Form string with date time, the values of temperatures inside, outside, the state of wind rain automation and the state of ventilator:
		self.OString = self.MeasurementTime.strftime("%d.%m.%Y %H:%M:%S")		
		# error can appear actually here during transformation from "None" to real value :
		self.OString = self.OString + "	" + "{:.2f}".format(self.t_inside) 
		self.OString = self.OString + "	" + "{:.2f}".format(self.t_outside) 
		self.OString = self.OString + "	" + str(self.StateOfVentillator) 
		self.OString = self.OString + "	" + "{:.2f}".format(self.h_outside)
		self.OString = self.OString + "\n"  # comment last summand if used with print	
		sys.stdout.write(self.OString) 
		self.f.write(self.OString) # output to file

	def stop_ventilation(self):
		if (not hasattr(self,'StateOfVentillator')): 
			self.StateOfVentillator = 1
		
		if (self.StateOfVentillator==1): # stop ventilation makes sense only if ventillator is on 
			GPIO.output(self.P.RelayK1ControlPin, self.RelaySwitchOff) # switch off voltage from ventillator
			self.StateOfVentillator = 0 # just information bit, which shows the state of ventillation. 
										# must be always set at change of ventilation
										# 1 - on, 0 - off 
			self.lastSwitchOffTime = datetime.datetime.today()
		
	def start_ventilation(self):
		if (self.StateOfVentillator==0):
			GPIO.output(self.P.RelayK1ControlPin, self.RelaySwitchOn) # switch off voltage from ventillator
			self.StateOfVentillator = 1 # just information bit, which shows the state of ventillation. 
									# must be always set at change of ventilation
									# 1 - on, 0 - off 


	def set_server_responce_message(self):

		# change responce to json format
		# to avoid usage of the same variables from different threads
		# we stay at usage of Ostring and we extract the data from the str
		
		tmpstr = self.OString
		jsonstr = '{'
		jsonstr = jsonstr + '"datetime":"' + tmpstr.split('\t')[0] + '",'
		jsonstr = jsonstr + '"tin":' + tmpstr.split('\t')[1] + ','
		jsonstr = jsonstr + '"tout":' + tmpstr.split('\t')[2] + ','
		jsonstr = jsonstr + '"hout":' + tmpstr.split('\t')[3] + ','
		jsonstr = jsonstr + '"FanState":' + tmpstr.split('\t')[4] 
		jsonstr = jsonstr + '}'
		
		return jsonstr


	def control_ventilation(self):
		if (self.auto==1):
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
			
			# check, that the last switch off was not too short time ago:
			Now = datetime.datetime.today()
			minOffTimeCondition = (Now-self.lastSwitchOffTime)>self.MinOffTimeDateTime
			
			if hasattr(self, 'h_outside'):
				humCondition = (self.h_outside < self.P.MaxHumidity)
			else: 
				humCondition = True
			
			# add to switchon counter, if all conditions are satisfied:
			if ( mainOnCondition & timeCondition & tMinCondition & minOffTimeCondition & humCondition):
				self.jonok = self.jonok + 1
				self.joffok = 0  # start to count again
			
			# The following conditions must be satisfied, to switch off 
			# ventilation:			
			mainOffCondition = (self.t_inside - self.t_outside)<self.P.TdifferenceOff		
			# the difference of temperatures is less than TdifferenceOff
			
				
			# add to switchoff counter, if all conditions are satisfied:
			if (mainOffCondition | (not tMinCondition) | (not timeCondition) | (not humCondition)):
				self.joffok = self.joffok + 1
				self.jonok = 0  # start to count again
			
			if ((self.jonok>5)):  # 5 measuraments, condition to switch on is satisfied. 						
								# then 'switch on' ventilation
				self.start_ventilation()
				jonok = 0 
			
			
			# switch off of ventilator must be done immidiately as soon as 
			# wind or rain was detected!
			if ((self.joffok>5)): # 5 measuraments, condition to switch off is satisfied. 
				self.stop_ventilation()
				self.joffok = 0 


