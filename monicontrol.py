#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
The main script, performing measurements of parameters, control of ventilation
and communication with clients (programs, eg Web). 

Usage:

This script can be started in command line from any folder 
or from another script. The full path to the script should be given, if needed. 

Example of usage:

sudo python /home/pi/Steuerung-Monitoring/monicontrol.py settingsMC.py 1>  /home/pi/tmp_logger_out.txt 2> /home/pi/tmp_logger_err.txt &

sudo python /home/pi/Steuerung-Monitoring/monicontrol.py settingsMC-Laden.py 1>  /home/pi/tmp_logger_out.txt 2> /home/pi/tmp_logger_err.txt &

or short in terminal in the folder with scripts:
sudo python monicontrol.py settingsRHTCO2.py 

sudo python /home/pi/Air/monicontrol.py settingsRHTCO2.py 1>  /home/pi/tmp_logger_out.txt 2> /home/pi/tmp_logger_err.txt &

The one, optional argument, here settingsMC.py or settingsRHTCO2.py  
is the file with settings.

Depending on the settingsfilename, the corresponding configuration of 
hardware will be chosen: 
settingsMC.py			Ventillation at low temperatures in the night. 
						To cool the building down. Version with wind rain automation
settingsMC-Laden.py		--.-- Version with humidity sensor. Without window opening. 
settingsRHTCO2.py		-Air ventilation on the base of CO2 concentration. 
						for high quality air for people.

It is also reasonable to redirect the console output into some file, 
here /home/pi/tmp_logger_out.txt and to redirect error output, 
here  to /home/pi/tmp_logger_err.txt 
Note: the file with the settings must be stored in the same folder 
as this main python script (monicontrol.py).

"""

from datetime import date, timedelta
import signal 							# to process kill signal and exit correctly
import time, datetime, sys, os 			# import system and date time functions
import traceback
from serverAir import *

# settings file name is given as first and only one argument of the script
# otherwise, the default settings filename is specified:
if (len(sys.argv)==2):
	settingsfname  = sys.argv[1]
else:
	settingsfname = "settingsMC.py"

# choose accordingly  monicontrol logger-controller class, 
# create and initialize the object:
if (settingsfname == "settingsMC.py"):
	from monicontrolclassA import *  
	moniCont = MoniControlA(settingsfname)

if (settingsfname == "settingsMC-Laden.py"):
	from monicontrolclassB import *
	moniCont = MoniControlB(settingsfname)

if (settingsfname == "settingsRHTCO2.py"):
	from monicontrolclassC import *
	moniCont = MoniControlC(settingsfname)

serverAirMoniCont = ServerAirCoCo(moniCont) # the object of the class ServerMoniControl is initialized

# To exit politely (after kill -15 or after ctrl+C):
def signal_term_handler(signal, frame): 
	print 'got SIGTERM'	
	moniCont.clean_and_exit()
	serverAirMoniCont.clean()

signal.signal(signal.SIGTERM, signal_term_handler) # initialise Sigterm  

PrevMeasurementTime = datetime.datetime.today() # artificially set to now just to start. 

while True:
	try:
		t1 = datetime.datetime.today()     # to define the duration of all operations before "sleep"
		moniCont.get_data() 
		moniCont.save_data()        
		moniCont.control_ventilation()     # to control LED to tell to user, that light is bad or good		

		# to generate condition to switch output to the new file:
		Prevt = int(PrevMeasurementTime.strftime(moniCont.P.SaveInterval))
		t = int(moniCont.MeasurementTime.strftime(moniCont.P.SaveInterval))
		
		PrevMeasurementTime = moniCont.MeasurementTime
		if (Prevt!=t): # new file each hour or day etc
			moniCont.switch_output_file()
		
		t2 = datetime.datetime.today()# to define the duration of all operations before "sleep"

		dt = t2 - t1 						# this time is needed to make all operations. 
		fdt  = dt.seconds + dt.microseconds / 1000000.0 # transform to floating point with microseconds precision
		waittime = moniCont.P.LoggingInterval*1.0 - fdt 

		# we need to wait less, than LoggingInterval to start new measurement, 
		# because some time was needed to perform all operations:
		if (waittime>0):
			time.sleep(waittime) # sleep watitime 
	except:
		# oops! Exceptions happen!
		#  * switch off ventilator 
		#  * close phisical windows
		#  * information about exception is written to the stdout
		#  * email message to administrator is sent
		#  * stop program, otherwise it wil sent emails every 10 sec
		moniCont.auto = 0
		msgpart = traceback.format_exc()
		emsg = msgpart + " exception "  + str(sys.exc_info()[0])
		print(emsg)
		serverAirMoniCont.clean()
		moniCont.stop_ventilation()
		sys.stdout.flush()			# make output to file
		moniCont.send_notification(emsg)
		sys.exit()
		
		# OTHER WAY OF EXCEPTION HANDLING IS NOT GOOD: AFTER ANY EXCEPTION 
		# ONE NEEDS TO SWITCH OFF
		# OTHERWISE POWERFUL VENTILLATORS WILL CAN DO WRONG JOB

##=======================================================================
