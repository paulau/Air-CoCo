#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Description: Code for the system, based on:
wind rain sensor, 
opening closing windows, 
ventilator 
two DS18B20 sensors 
"""

from monicontrolclass import *  			# Base monicontrol logger-controller class

class MoniControlA(MoniControlBase):
	def __init__(self, settingsfname):
		super().__init__(settingsfname)  #let the constructor of parent class run
		#self.windrain = (hasattr(self.P, 'pin1') & hasattr(self.P, 'pin2')) & 
		#self.fensteroffener = (hasattr(self.P, 'RelayK2ControlPin') & hasattr(self.P, 'RelayK3ControlPin') )
		GPIO.setup(self.P.RelayK2ControlPin, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)
		GPIO.setup(self.P.RelayK3ControlPin, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)
		self.close_windows()  # close phisical windows:
		self.initialise_wind_rain_monitoring()
		self.initialise_output_header()
		self.sensor_in = SensorAirCoCo(self.P.sensor_inside_id)
		self.sensor_out = SensorAirCoCo(self.P.sensor_outside_id)


	def initialise_output_header(self):
		Save header! Data format!!!

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
		
	# get values of temperatures inside and outside from sensors, 
	# the state of windrain automation, the time of measurements. 
	def get_data(self):
get data of parent
		self.windRainState = GPIO.input(self.P.pin2)	# get the state of wind rain automation. 

	def stop_ventilation(self):
		if (self.StateOfVentillator==1): # stop ventilation makes sense only if ventillator is on 
			GPIO.output(self.P.RelayK1ControlPin, self.RelaySwitchOff) # switch off voltage from ventillator
			self.StateOfVentillator = 0 # just information bit, which shows the state of ventillation. 
										# must be always set at change of ventilation
										# 1 - on, 0 - off 
			self.close_windows()
			self.lastSwitchOffTime = datetime.datetime.today()
		
	def start_ventilation(self):
		if (self.StateOfVentillator==0):
			self.open_windows()
			GPIO.output(self.P.RelayK1ControlPin, self.RelaySwitchOn) # switch off voltage from ventillator
			self.StateOfVentillator = 1 # just information bit, which shows the state of ventillation. 
									# must be always set at change of ventilation
									# 1 - on, 0 - off 

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
		self.OString = self.MeasurementTime.strftime("%d.%m.%Y %H:%M:%S")		
		# error can appear actually here during transformation from "None" to real value :
		self.OString = self.OString + "	" + "{:.2f}".format(self.t_inside) 
		self.OString = self.OString + "	" + "{:.2f}".format(self.t_outside) 
		self.OString = self.OString + "	" + "{:.0f}".format(self.windRainState) 
		self.OString = self.OString + "	" + str(self.StateOfVentillator) 
		self.OString = self.OString + "\n"  # comment last summand if used with print	
		sys.stdout.write(self.OString) 
		self.f.write(self.OString) # output to file

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
			
			if ((self.jonok>5)&(windRainCondition)):  # if 5 measuraments, condition to switch on is satisfied.
													  # then 'switch on' ventilation
				self.start_ventilation()
				jonok = 0 

			# switch off of ventilator must be done immidiately as soon as 
			# wind or rain was detected!
			if ((self.joffok>5)|(not windRainCondition)): # 5 measuraments, condition to switch off is satisfied. 
				self.stop_ventilation()
				self.joffok = 0 

	def set_server_responce_message(self):

		# change responce to json format
		# to avoid usage of the same variables from different threads
		# we stay at usage of Ostring and we extract the data from the str
		
		tmpstr = self.OString
		jsonstr = '{'
		jsonstr = jsonstr + '"datetime":"' + tmpstr.split('\t')[0] + '",'
		jsonstr = jsonstr + '"tin":' + tmpstr.split('\t')[1] + ','
		jsonstr = jsonstr + '"tout":' + tmpstr.split('\t')[2] + ','
		jsonstr = jsonstr + '"WindRainState":' + tmpstr.split('\t')[3] + ','
		jsonstr = jsonstr + '"FanState":' + tmpstr.split('\t')[4] 
		jsonstr = jsonstr + '}'
		#"WindowOpenMotorState":1,
		#"WindowCloseMotorState":1

		return jsonstr
