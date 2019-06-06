#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Usage: see monicontrol.py
# Einstellungen für Steuerung-Monitoring System Kornkraft.

OpeningTime = 60			# Sekunde. Zeit um Fenster zu offnen

# if the sensor contains only  4 characters, then it is i2c sensor
# otherwise 1-wire 
# The values of the sensors ids are specific for each sensor. 
# See 1-wire or i2c documentation, how to get them 

sensor_inside_id =  '28-0417a3040eff' #  
					# '28-020a92454cb5'

sensor_outside_id = '0x44' # use 0x prefix at i2c address of a sensor
# if the sensor contains only  4 characters, then it is i2c sensor otherwise 1-wire


RelayK1ControlPin =  23			# GPIO-Pin Nummer für Steuerung von Lüfter


LoggingInterval = 10			# Sekunde. Zeitinterval zwischen Messungen, Sekunden 
fileprefix = "kk002_"			# Präfix von Datei. Alle Dateien starten mit diese Präfix.
SaveInterval = "%d"     		# "%d" save every new day, "%H" save every new Hour

TdifferenceOn = 3.0			# Kelvin. Schalten die Lüftung an, wenn Außentemperatur - Innentemperatur > TdifferenceOn 
TdifferenceOff = 1.0			# Kelvin. Schaltet diel Lüftung aus, wenn Außentemperatur - Innentemperatur < TdifferenceOff
					# Default Wert ist 1 oder grosser, weil Prezision von Fühler ist +-0.5 

Tmin = 14.0 #ab 27.05.2016		# °C Steuerung wird betätigt nur wenn Innen Temperatur ist grosser als Tmin

MinOffTime = 5				# Minutes. Minimal Zeit zwischen Ende von Lüftung und Start von volgende Lüftung.  
							# um häufige An- Aus-schaltungen zu vermeiden. 

MaxHumidity = 80.0			# Luften, wenn Feuchtigkeit unter MaxHumidity ist 

# because of insekts, we set in settings file normally 
# the ventilation between StartTime and EndTime every day

StartTime = 0 # h
EndTime = 24 #h bis 7 Uhr einschlisslich, dh bis 7:59 # 5
 
internettype = 1 			# Art von vervendete internet: 1 - Ethernet 2 - WiFi 3 - MobileBroadband
FTPfolder = "monicontrol" 		# Name von Ordner Ohne "/" am Ende und am Anfang.
description = "Controlled ventillation system for Korn Kraft " # Beschreibung
ftpserveraddr  = "xxx.xx.xx.xx"	#  IP oder URL von ftp server für Datenerfassung
ftpbenutzer="kornkraft" 		# Benutzername
ftppasswort="xxx" 			# password
UploadRate=3600 			# Sekunden Daten werden jede UploadRate Sekunden hochgeladen.

emailsto = ["muster01@gmail.com", "muster02@web.de"] 
emailfrom = 'from@server.de'
mailserver = 'mail.server.de'
passwmail = 'xxx'

webfolder = '/var/www/html/air-coco/datapics/'  # to move the visualised data to the web folder
outputfolder = '/home/pi/Steuerung-Monitoring/data/'
#path to the folder to save the measurements data.
#The data will be saved in the current folder, if the
#argument is not specified. 
#User requested to change the output folder to the external USB memory:
#'/media/pi/INTENSO/'  
