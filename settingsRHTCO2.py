#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Parameters of Sensors and relays:

CO2_ADDR = 0x60  # Attention! Very specific setting for one or two reconfigured sensors.
DHTDataPin=8
GPIOVoltagePin=25
RelayK1ControlPin = 18  # #SignalControlPin = 21 
VentControlPin = 21 # Additionnally to signal (red ligt), the switch on off
					# of a ventillator is added

# Parameters of control:

MinOffTime = 5		# Minutes. Minimal Zeit zwischen Ende von Lüftung und Start von volgende Lüftung.  
					# um häufige An- Aus-schaltungen zu vermeiden. 
#An average concentration of CO2 in outdoor air is 400ppm Year 2018.
CO2Limit = 1200 # 1000 ppm means IDA 3 Lower range of moderate quality
CO2LimitOff = 1000 # IDA 1 
# CO2 concentration in excess above the outdoor air:
# IDA1  <= 400    High Quality
# IDA2  400-600   Average Quality
# IDA3  600-1000  moderate quality
# IDA4  >1000     low quality
# __________________
# DIN EN 13779

#Logging parameters:

LoggingInterval = 1
SaveInterval = "%d" #  "%M" "%d" save every new day, "%H" save every new Hour
fileprefix = "messung001_"
outputfolder = '/home/pi/Steuerung-Monitoring/data/'				# to save the measurementsdata


# Parameters of central server:
FTPfolder = "I23"
ftpserveraddr="139.13.179.47"
ftpbenutzer="jadehs"
ftppasswort=""
UploadRate=86400


# SQL Parameters:
# ifSQLuser is defined, then mySQL will be used
SQLuser = "logger"
SQLpw = "logger112358"
tabelle = "RHTCO2"
SQLserver = "localhost"
# uploadstable = "uploads"  # not configured for CO2-ampel home
FAST = True


webfolder = '/var/www/RHTCO2pics/'  # to move the visualised data to the web folder
# if this variable is defined, then the measurementsdata will be initialised 
#and moved into web folder. One needs accordingly to create such a folder

#Email Parameters:

emailsto = ['xxx@xxx.com']  
emailfrom = 'raspberry@xxx.de'
mailserver = 'xxx.de'
passwmail = 'xxx'


# settings for visualisation:
window=False
outfile="RHTCO2.png"
VisualisationInterval=10
y1min=10
y1max=80
#y2min=0
#y2max=3000
dpivalue=96 #150
tex = False
ymax =  1400
d1 = '2018-09-24 17:00' 
d2 = '2018-09-25 17:00'

# incorporate into code, where necessary:
#import datetime
#xd1 = datetime.datetime.strptime(d1, '%Y-%m-%d %H:%M') #  %H:%M

# Other Parameters:
internettype = 2 # 1 - Ethernet 2 - WiFi 3 - MobileBroadband
description = "ModelC" #
