#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Usage: see monicontrol.py
# Einstellungen für Steuerung-Monitoring System Kornkraft.

OpeningTime = 60			# Sekunde. Zeit um Fenster zu offnen

sensor_inside_id =  '28-020d9177a279'	# '28-0415a3e91eff'  # These values of the sensors ids are  specific for 
sensor_outside_id = '28-02099177d15c'	# '28-0415a40063ff' # each sensor. See 1-wire documentation, how to get them

RelayK1ControlPin =  16			# GPIO-Pin Nummer für Steuerung von Lüfter
RelayK2ControlPin =  20			# GPIO-Pin Nummer für Umschaltung von manuel auf auto Steuerung
RelayK3ControlPin =  21			# GPIO-Pin Nummer für Umschaltung zwischen Auf und Zu.


LoggingInterval = 10			# Sekunde. Zeitinterval zwischen Messungen, Sekunden 
fileprefix = "kk002_"			# Präfix von Datei. Alle Dateien starten mit diese Präfix.
SaveInterval = "%d"     		# "%d" save every new day, "%H" save every new Hour

TdifferenceOn = 3.0			# Kelvin. Schalten die Lüftung an, wenn Außentemperatur - Innentemperatur > TdifferenceOn 
TdifferenceOff = 1.0			# Kelvin. Schaltet diel Lüftung aus, wenn Außentemperatur - Innentemperatur < TdifferenceOff
					# Default Wert ist 1 oder grosser, weil Prezision von Fühler ist +-0.5 

Tmin = 14 #ab 27.05.2016		# °C Steuerung wird betätigt nur wenn Innen Temperatur ist grosser als Tmin

MinOffTime = 5				# Minutes. Minimal Zeit zwischen Ende von Lüftung und Start von volgende Lüftung.  
					# um häufige An- Aus-schaltungen zu vermeiden. 

# because of insekts, we set in settings file normally 
# the ventilation between StartTime and EndTime every day

StartTime = 0 # h
EndTime = 24 #h bis 7 Uhr einschlisslich, dh bis 7:59 # 5
 
# Wind rain state read settings.
# The pin1 will be set as output pin and the state is set to 1 
# The pin1 is connected via relay to pin2.
# The relay is controlled via 220V of wind rain "phase"
# The state of the pin2 is accordingly the state of wind rain automatic

pin1 = 19   			
pin2 = 26   


internettype = 1 			# Art von vervendete internet: 1 - Ethernet 2 - WiFi 3 - MobileBroadband
FTPfolder = "monicontrol" 		# Name von Ordner Ohne "/" am Ende und am Anfang.
description = "Controlled ventillation system for Korn Kraft " # Beschreibung
ftpserveraddr  = "xxx.xx.xx.xx"	#  IP oder URL von ftp server für Datenerfassung
ftpbenutzer="kornkraft" 		# Benutzername
ftppasswort="xxx" 			# password
UploadRate=3600 			# Sekunden Daten werden jede UploadRate Sekunden hochgeladen.

