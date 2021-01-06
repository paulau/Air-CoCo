#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Description: Code for the system of building cooling  via night ventilation, based on:
wind rain sensor, 
opening closing windows, 
ventilator 
one DS18B20 
and one SHT31D
sensors
"""

from monicontrolclass import *  			# Base monicontrol logger-controller class



class MoniControlA(MoniControlBase):
	def __init__(self, settingsfname):
		MoniControlBase.__init__(self,settingsfname)  #let the constructor of parent class run
		self.initialise_wind_rain_monitoring()
		self.initialise_output_header()
		self.sensor_in = SensorDS18B20(self.P.sensor_inside_id)
		self.sensor_out = sensorSHT31D(self.P.sensor_outside_id)

		# "declare" variables for occasional use before definition e.g. via server
		self.OString = "01.01.2000 00:00:00	0.00	0.00	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0"

		self.t_inside = 0.0
		self.t_outside = 0.0
		self.windRainState = 1
		# self.StateOfVentillator  defined in  stopVentilation start ventilation only
		self.h_outside = 0.0
		self.auto = 1
		self.mainOnCondition = 1 
		self.humidityCondition = 1 
		self.tMinCondition = 1
		self.timeCondition = 1
		self.windRainCondition = 1
		self.minOffTimeCondition = 1
		self.mainOffCondition = 1
		self.jonok = 0
		self.joffok = 0
		
		#self.RelayK2State = 0   defined in  stopVentilation start ventilation only
		#self.RelayK3State = 0    defined in  stopVentilation start ventilation only

		self.val = 0b0000000000000000  # 16 bit int
		#'{:b}'.format(val)



	def initialise_ventilation_devices(self):
		# **************************************************************
		# initialise GPIO to control relays and to monitor state of pins. 
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)  
		# Attention: some Relay moduls switch Relays on when voltage is Low, then use:
		self.RelaySwitchOn = GPIO.LOW
		self.RelaySwitchOff  = GPIO.HIGH
		
		# some Relay moduls switch Relays on when voltage is High, then use 
		#self.RelaySwitchOn = GPIO.HIGH
		#self.RelaySwitchOff = GPIO.LOW

		# to open windows
		GPIO.setup(self.P.RelayK2ControlPin, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)
		GPIO.setup(self.P.RelayK3ControlPin, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)
		
		# Set the following GPIO pins as output pins:		
		GPIO.setup(self.P.RelayK1ControlPin, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)		
		self.stop_ventilation()  		# default state: ventillation off.		
		print("	GPIO for controlling Relay initialisation complete")
		# **************************************************************

	def initialise_output_header(self):
		# creates header file for the output files		
		# The methods save_data, set_server_responce_message initialise_output_header
		# must be adjusted sinchronously!!
		
		fheadername  = self.P.fileprefix + self.fileextension 
		fheader = open(self.opath + fheadername,'w')
		OString = "datetime"
		OString = OString + "	" + "tin"
		OString = OString + "	" + "tout"
		OString = OString + "	" + "WindRainState"
		OString = OString + "	" + "FanState"
		OString = OString + "	" + "houtside"
		OString = OString + "	" + "auto"
		OString = OString + "	" + "mainOnCondition"
		OString = OString + "	" + "tMinCondition"
		OString = OString + "	" + "timeCondition"
		OString = OString + "	" + "windRainCondition"
		OString = OString + "	" + "minOffTimeCondition"
		OString = OString + "	" + "mainOffCondition"
		OString = OString + "	" + "jonok"
		OString = OString + "	" + "joffok"
		OString = OString + "	" + "RelayK2State"
		OString = OString + "	" + "RelayK3State"
		OString = OString + "\n"  # comment last summand if used with print	
		fheader.write(OString) # output to file
		fheader.close()

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
		self.sensor_in.get_data()
		self.sensor_out.get_data()
		self.t_inside = self.sensor_in.t		# get temperature inside
		self.t_outside = self.sensor_out.t		# get temperature outside
		self.h_outside = self.sensor_out.h		# get humidity outside  ! may be undefined! check!
		self.MeasurementTime = datetime.datetime.today() # get time now
		self.windRainState = GPIO.input(self.P.pin2)	# get the state of wind rain automation. 



	def stop_ventilation(self):

		if (not hasattr(self,'StateOfVentillator')): 
			self.StateOfVentillator = 1
		
		if (self.StateOfVentillator==1): # stop ventilation makes sense only if ventillator is on 
			GPIO.output(self.P.RelayK1ControlPin, self.RelaySwitchOff) # switch off voltage from ventillator
			self.StateOfVentillator = 0 # just information bit, which shows the state of ventillation. 
										# must be always set at change of ventilation
										# 1 - on, 0 - off 
			self.close_windows()
			self.lastSwitchOffTime = datetime.datetime.today()
		
	def start_ventilation(self):

		if (not hasattr(self,'StateOfVentillator')): 
			self.StateOfVentillator = 0


		if (self.StateOfVentillator==0):
			self.open_windows()
			GPIO.output(self.P.RelayK1ControlPin, self.RelaySwitchOn) # switch off voltage from ventillator
			self.StateOfVentillator = 1 # just information bit, which shows the state of ventillation. 
									# must be always set at change of ventilation
									# 1 - on, 0 - off 

	def open_windows(self):
		print('	Open Windows')
		GPIO.output(self.P.RelayK2ControlPin, self.RelaySwitchOn) # switch to automatic control
		self.RelayK2State = 1
		GPIO.output(self.P.RelayK3ControlPin, self.RelaySwitchOn) # switch to opening phase
		self.RelayK3State = 1
		
		time.sleep(self.P.OpeningTime) # wait till Windows are opened
		GPIO.output(self.P.RelayK2ControlPin, self.RelaySwitchOff) # switch to manual control
		self.RelayK2State = 0
		GPIO.output(self.P.RelayK3ControlPin, self.RelaySwitchOff) # default state switch off of relay 3
		self.RelayK3State = 0
		
	def close_windows(self):
		print('	Close Windows')
		GPIO.output(self.P.RelayK2ControlPin, self.RelaySwitchOn)	# switch to automatic control
		self.RelayK2State = 1
		GPIO.output(self.P.RelayK3ControlPin, self.RelaySwitchOff)	# switch to closing phase
		self.RelayK3State = 0
		
		time.sleep(self.P.OpeningTime+10)							# wait till Windows are closed 
		GPIO.output(self.P.RelayK2ControlPin, self.RelaySwitchOff)	# switch to manual control
		self.RelayK2State = 0

	def save_data(self):
		# Form string with date time, the values of temperatures inside, outside, the state of wind rain automation and the state of ventilator:
		self.OString = self.MeasurementTime.strftime("%d.%m.%Y %H:%M:%S")		
		# error can appear actually here during transformation from "None" to real value :
		self.OString = self.OString + "	" + "{:.2f}".format(self.t_inside) 
		self.OString = self.OString + "	" + "{:.2f}".format(self.t_outside) 
		self.OString = self.OString + "	" + "{:.0f}".format(self.windRainState) 
		self.OString = self.OString + "	" + str(self.StateOfVentillator) 
		self.OString = self.OString + "	" + "{:.2f}".format(self.h_outside) 
		self.OString = self.OString + "	" + str(self.auto) 
		self.OString = self.OString + "	" + str(int(self.mainOnCondition)) 
		self.OString = self.OString + "	" + str(int(self.tMinCondition))
		self.OString = self.OString + "	" + str(int(self.timeCondition)) 
		self.OString = self.OString + "	" + str(int(self.windRainCondition))
		self.OString = self.OString + "	" + str(int(self.minOffTimeCondition))
		self.OString = self.OString + "	" + str(int(self.mainOffCondition))
		self.OString = self.OString + "	" + str(self.jonok)
		self.OString = self.OString + "	" + str(self.joffok)
		self.OString = self.OString + "	" + str(self.RelayK2State)
		self.OString = self.OString + "	" + str(self.RelayK3State)
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
			
			self.mainOnCondition = (self.t_inside - self.t_outside) > self.P.TdifferenceOn 
			# the difference of temperatures outside and inside reached the desired value. 
			# to start ventilation only, if it makes sence. 
			
			self.humidityCondition = self.h_outside < self.P.MaxHumidity
			
			self.tMinCondition = self.t_inside > self.P.Tmin
			# The temperature inside is higher, than some reasonable for people Tmin value
			
			self.timeCondition = ((tm>=self.P.StartTime)&(tm<=self.P.EndTime))
			# the ventilation only in certain time interval nights, to prevent insects problem
			
			#  Check of the Wind Rain must be added.
			self.windRainCondition = self.windRainState
	
			# check, that the last switch off was not too short time ago:
			Now = datetime.datetime.today()
			self.minOffTimeCondition = (Now-self.lastSwitchOffTime)>self.MinOffTimeDateTime
			
			# add to switchon counter, if all conditions are satisfied:
			if ( self.mainOnCondition & self.timeCondition & self.tMinCondition & self.minOffTimeCondition & self.humidityCondition):
				self.jonok = self.jonok + 1
				self.joffok = 0  # start to count again
			
			# The following conditions must be satisfied, to switch off 
			# ventilation:
			self.mainOffCondition = (self.t_inside - self.t_outside)<self.P.TdifferenceOff		
			# the difference of temperatures is less than TdifferenceOff
			
			# add to switchoff counter, if all conditions are satisfied:
			if (self.mainOffCondition | (not self.tMinCondition) | (not self.timeCondition) | (not self.humidityCondition)):
				self.joffok = self.joffok + 1
				self.jonok = 0  # start to count again
			
			if ((self.jonok>5)&(self.windRainCondition)):  # if 5 measuraments, condition to switch on is satisfied.
													  # then 'switch on' ventilation
				self.start_ventilation()
				self.jonok = 0 

			# switch off of ventilator must be done immidiately as soon as 
			# wind or rain was detected!
			if ((self.joffok>5)|(not self.windRainCondition)): # 5 measuraments, condition to switch off is satisfied. 
				self.stop_ventilation()
				self.joffok = 0 

	def set_server_responce_message(self):

		# change responce to json format
		# to avoid usage of the same variables from different threads
		# we stay at usage of Ostring and we extract the data from the str
		
		tmpstr = self.OString
		
		# json has shown drawbacks! too big! therefore made general! different format
		
		#jsonstr = '{'
		#jsonstr = jsonstr + '"datetime":"' + tmpstr.split('\t')[0] + '",'
		#jsonstr = jsonstr + '"tin":' + tmpstr.split('\t')[1] + ','
		#jsonstr = jsonstr + '"tout":' + tmpstr.split('\t')[2] + ','
		#jsonstr = jsonstr + '"WindRainState":' + tmpstr.split('\t')[3] + ','
		#jsonstr = jsonstr + '"FanState":' + str(self.StateOfVentillator) + ','
		#jsonstr = jsonstr + '"houtside":' + tmpstr.split('\t')[5] + ','
		#jsonstr = jsonstr + '"auto":' + tmpstr.split('\t')[6] + ','
		#jsonstr = jsonstr + '"mainOnCondition":' + tmpstr.split('\t')[7] + ','
		#jsonstr = jsonstr + '"tMinCondition":' + tmpstr.split('\t')[8] + ','
		#jsonstr = jsonstr + '"timeCondition":' + tmpstr.split('\t')[9] + ','
		#jsonstr = jsonstr + '"windRainCondition":' + tmpstr.split('\t')[10] + ','
		#jsonstr = jsonstr + '"minOffTimeCondition":' + tmpstr.split('\t')[11] + ','
		#jsonstr = jsonstr + '"mainOffCondition":' + tmpstr.split('\t')[12] + ','
		#jsonstr = jsonstr + '"jonok":' + tmpstr.split('\t')[13] + ','
		#jsonstr = jsonstr + '"joffok":' + tmpstr.split('\t')[14] + ','
		#jsonstr = jsonstr + '"RelayK2State":' + str(self.RelayK2State)+ ','
		#jsonstr = jsonstr + '"RelayK3State":' + str(self.RelayK3State)
		#jsonstr = jsonstr + '}'
		
		#return jsonstr

		StateStr = tmpstr.split('\t')[0] + '\t'				#  datettime
		StateStr = StateStr + tmpstr.split('\t')[1] +  '\t'	#tin 
		StateStr = StateStr + tmpstr.split('\t')[2] +  '\t'	#tout
		StateStr = StateStr + tmpstr.split('\t')[5] +  '\t'	#hout 
		StateStr = StateStr + tmpstr.split('\t')[13] + '\t' #jonok
		StateStr = StateStr + tmpstr.split('\t')[14] + '\t' #joffok
		   
		#self.val = set_bit(self.val, 0, bool(self.StateOfVentillator))		# 0 bit FanState  
		self.val = set_bit(self.val, 0, bool(int(tmpstr.split('\t')[4])))		# 0 bit FanState  
		self.val = set_bit(self.val, 1, bool(int(tmpstr.split('\t')[3])))	# 1 bit WindRainState  
		self.val = set_bit(self.val, 2, bool(int(tmpstr.split('\t')[6])))	# 2 bit auto
		self.val = set_bit(self.val, 3, bool(int(tmpstr.split('\t')[7])))	# 3 bit mainOnCondition
		self.val = set_bit(self.val, 4, bool(int(tmpstr.split('\t')[8])))	# 4 bit tMinCondition
		self.val = set_bit(self.val, 5, bool(int(tmpstr.split('\t')[9])))	# 5 bit timeCondition
		self.val = set_bit(self.val, 6, bool(int(tmpstr.split('\t')[10])))	# 6 bit windRainCondition
		self.val = set_bit(self.val, 7, bool(int(tmpstr.split('\t')[11])))	# 7 bit minOffTimeCondition
		self.val = set_bit(self.val, 8, bool(int(tmpstr.split('\t')[12])))	# 8 bit mainOffCondition
		#self.val = set_bit(self.val, 9, bool(self.RelayK2State))			# 9 bit  RelayK2State
		#self.val = set_bit(self.val, 10, bool(self.RelayK3State))			# 10 bit  RelayK3State
		self.val = set_bit(self.val, 9, bool(int(tmpstr.split('\t')[15])))	# 7 bit minOffTimeCondition
		self.val = set_bit(self.val, 10, bool(int(tmpstr.split('\t')[16])))	# 8 bit mainOffCondition
		


		StateStr = StateStr + str(self.val)  # set of bool values

		return StateStr
