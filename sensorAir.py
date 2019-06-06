#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
The collection of classes, providing initialisation of different sensors 
and measurement of parameters.

Assumed, that 1-wire and i2c-bus are switched on in raspi-config. Sensors 
are connected to according pins, see documentation og GPIO and id(address)
are passed to constructor as argument
"""

import time, os  # system  and time functions
import RPi.GPIO as GPIO			# GPIO functions

# DS18B20 temperature sensor 1-wire bus
class SensorDS18B20:
	# constructor. Initialise Sensor
	def __init__(self, sensor_id):
		# ids are specified in the configuration files and passed to 
		# constructor via calling program
		self.sensor_id = sensor_id
		self.t = None			
		# Initialize the 1-wire. It could be called twice, if the second 
		# instance of the  sensor is initialised, but i think it is not a problem. 
		# in case of problems, insert check, wehther 1 wire already 
		# initialised. 
		# may be move the following two commands into /etc/rc.local over
		os.system('modprobe w1-gpio')  # Turns on the 1-wire GPIO module
		os.system('modprobe w1-therm') # Turns on the 1-wire temperature module

		# Finds the correct device file that holds the temperature data
		base_dir = '/sys/bus/w1/devices/'
		device_folder = base_dir + sensor_id 
		self.device_file = device_folder + '/w1_slave'

	# A function that reads the data of the temperature sensor. 
	def read_temp_raw(self):
		f = open(self.device_file, 'r') # opens the temperature device file of the sensor
		lines1 = f.readlines() # Returns the text
		f.close()
		return lines1

	def get_data(self):
		#reads the sensors data
		lines1 = self.read_temp_raw() # Read the data from 'device file'
		# While the first line does not contain 'YES', wait for 0.2s
		# and then read the device file again.
		while (lines1[0].strip()[-3:] != 'YES'):
			time.sleep(0.2)
			lines1 = self.read_temp_raw()
		
		# Look for the position of the '=' in the second line of the
		# device file.
		equals_pos = lines1[1].find('t=')
	
		# If 't=' is found, the convert the rest of the line after into degrees Celsius
		if (equals_pos != -1):
			temp_string = lines1[1][equals_pos+2:]
			self.t = float(temp_string) / 1000.0

# Temperatur Humidity SHT31D sensor i2-c bus
class sensorSHT31D:
	def __init__(self, sensor_id):
		self.sensor_id = sensor_id
		self.t = None
		self.h = None
		import smbus
		self.bus = smbus.SMBus(1)


	def get_data(self):
		self.bus.write_i2c_block_data(int(self.sensor_id,16), 0x2C, [0x06])
		time.sleep(0.5)
		# Temp MSB, Temp LSB, Temp CRC, Luftfeuchte MSB, Luftfeuchte LSB, Luftfeuchte CRC
		data = self.bus.read_i2c_block_data(int(self.sensor_id,16), 0x00, 6)
		# Temperatur in Celsius
		temp = data[0] * 256 + data[1]
		self.t = -45 + (175 * temp / 65535.0) 
		# relative Luftfeuchte in %
		self.h = 100 * (data[3] * 256 + data[4]) / 65535.0


# K-30  CO2 sensor. i2-c bus. 
class SensorCO2:
	def __init__(self, sensor_id):
		from notsmb import notSMB		
		self.CO2_ADDR = sensor_id # int(sensor_id,16)
		self.bus = notSMB(1) # 1 for standard i2c bus of raspberry pi B         
		print("	CO2 Sensor initialised")
		
		#import smbus
		#self.bus = smbus.SMBus(1)
		#self.bus.write_i2c_block_data(self.CO2_ADDR, 0x2C, [0x06])
		#time.sleep(0.5)
		## Temp MSB, Temp LSB, Temp CRC, Luftfeuchte MSB, Luftfeuchte LSB, Luftfeuchte CRC
		#data = self.bus.read_i2c_block_data(int(self.sensor_id,16), 0x00, 6)

	def get_co2(self):
		self.co2Val = None  # before start getting this variable clean it
		while (self.co2Val==None): # try to get it until success
			try:
				# several attempts may be needed to read this sensor 
				# TRICKY SENSOR
				sum=-1 #Checksum
				while (sum!=0):

					resp = self.bus.i2c(self.CO2_ADDR,[0x22,0x00,0x08,0x2A],4) 
					time.sleep(0.1) # important to reduce frequency of error in checksum
					a = resp[0] + resp[1] + resp[2]
					if (a>255):
						a = a - 256
					# while resp[3] is not more than byte
					# one needs to check chechsumm within one byte range
					sum=a-resp[3]  # check summ must be zero

				#checksum simply MUST be zero here!
				#Checksum failure can be due to a number of factors,
				#fuzzy electrons, sensor busy, etc.
				
				self.co2Val = (resp[1]*256) + resp[2]                    
			except:
				self.co2Val = None  # in case of exception clean it 
				pass
		return self.co2Val

# DHT22 sensor
class SensorDHT:
	def __init__(self, GPIOVoltagePin, DHTDataPin):
		import Adafruit_DHT as dht
		self.dht = dht
		self.DHTDataPin = DHTDataPin
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)  
		# the sensor takes current from data pin, not from power pin. 
		# it may be a problem
		# switch on Voltage:
		GPIO.setup(GPIOVoltagePin, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)
		GPIO.output(GPIOVoltagePin, GPIO.HIGH) # switch on sensor
		print("	DHT Sensor initialised")

	def get_data(self):
		self.h = None  # before start getting this variable clean it
		self.t = None  # before start getting this variable clean it
		while ((self.h==None)|(self.t==None)): # try to get it until success
			try:
				self.h, self.t = self.dht.read_retry(self.dht.DHT22, self.DHTDataPin)
			except:
				self.h = None
				self.t = None                
				pass
				
		return self.h, self.t


#HYT-sensor
class SensorHYT:
	def __init__(self, GPIOVoltagePin):
		# ================================================================
		# if fedined address of HYT sensor then read it!!! 
		# if it is supposed to operate withut HYT, then comment it in 
		# settingsRHTCO2.py file
		pass
##                if (hasattr(self.P, 'HYT271address')):
##                    resp = self.bus.i2c(self.P.HYT271address,[],0) # Init HYT 221 for reading, ignore answer
##                    resp = self.bus.i2c(self.P.HYT271address,[] , 4) # # Read 4 bytes (even more) of data from HYT221
##                    # Now we have all data from sensor in the first 4 bytes of 'resp' Look for 
##                    # HYT221 doc to see how to extract temperature and humidity from bytes
##                    
##                    ##Calc humidity in rel.%
##                    hum = resp[0]<<8 | resp[1]
##                    hum = hum & 0x3FFF
##                    self.H = 100.0*hum/(2**14)
##                    
##                    # Calc temperature in °C
##                    resp[3] = resp[3] & 0x3F
##                    temp = resp[2] << 6 | resp[3]
##                    self.T = 165.0*temp/(2**14)-40
##
