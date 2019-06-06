#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Client to control TestServer

Usage: 
python /home/pi/TestClient.py
 
'''

import socket
import sys

PORT = 40012
HOST = 'localhost'
message = 'GetData' #'Stop'
# get power of ventilator as argument of pthis python script
try:		
	
	# Connect to server and send value of power to set in Ventilator:
	# it will be only done if float value is sent as argument 
	# otherwise do nothing
	clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientsocket.connect((HOST, PORT))
	clientsocket.send(str(message))
	server_responce = clientsocket.recv(256)
	print(server_responce)
	
	clientsocket.close()
except ValueError:
	print ("Error")


