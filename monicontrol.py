#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
The main script, making use of the MoniControl class

Usage:

This script can be started in command line from any folder 
or in another script. 
The full path to the script should be given, if needed. 

Example of usage:

sudo python /home/pi/Steuerung-Monitoring/monicontrol.py /home/pi/Steuerung-Monitoring/data/ 1>  /home/pi/tmp_logger_out.txt 2> /home/pi/tmp_logger_err.txt &	

User requested to change the output folder to the external USB memory:
sudo python /home/pi/Steuerung-Monitoring/monicontrol.py /media/pi/INTENSO/ 1>  /media/pi/INTENSO/tmp_logger_out.txt 2> /media/pi/INTENSO/tmp_logger_err.txt &	


The one, optional argument, here /home/pi/Steuerung-Monitoring/data/
is the path to the folder to save the measurements data.
The data will be saved in the current folder, if the
argument is not specified. 

It is also reasonable to redirect the console output into some file, 
here /home/pi/tmp_logger_out.txt and to redirect error output, 
here  to /home/pi/tmp_logger_err.txt 
Note: the file with the settings must be stored in the same folder 
as this main python script (monicontrol.py).





"""

from datetime import date, timedelta
from monicontrolclass import *  			# monicontrol logger-controller class
import signal 							# to process kill signal and exit correctly
import time, datetime, sys, os 			# import system and date time functions
import traceback

moniCont = MoniControl("settingsMC.py") # the object of the class MoniControl is initialized

# To exit politely (after kill -15 or after ctrl+C):
def signal_term_handler(signal, frame): 
	print 'got SIGTERM'	
	moniCont.clean_and_exit()

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
		# It is good to clean_up, close windows, switch of ventilator and stop control in case of exceptions.
		# but it is good to know, what is the exception and make so, that it does not appear or processed!
		# message to administrator could be nice!!!
		var = traceback.format_exc()
		print (var)
		print("Oops!",sys.exc_info()[0],"occured.")
		moniCont.clean_and_exit()
		# OTHER WAY OF EXCEPTION HANDLING IS NOT GOOD: AFTER ANY EXCEPTION 
		# ONE NEEDS TO SWITCH OFF
		# OTHERWISE POWERFUL VENTILLATORS WILL CAN DO WRONG JOB

##=======================================================================
