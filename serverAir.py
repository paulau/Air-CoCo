#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
This class provides initialisation of the class, which starts its own thread 
and works as server responding on the requests of clients and returning 
the data of moniControl class or performing control operations of monicontrol 
class

Communication with the external clients via socket.
The code is based on  examples in Client-Server folder.
The server class uses the class MoniControl 
"""

import socket, threading, os, sys

class ServerAirCoCo(threading.Thread):
	# constructor. Initialise Sensor
	def __init__(self, mc):
		self.mc = mc

		# This method starts thread, which listens to certain port at 
		# current address, to provide responces to the client software 
		# about the state of ventilatin.
		# Optionally, the server could be used to reset parameters of 
		# ventilation
		
		threading.Thread.__init__(self)
		self.threadID = 1
		self.name = "Thread-1"
		self.HOST = 'localhost'  # ' ' Symbolic name, meaning all available interfaces
		self.PORT = 40012 		# 8888 Arbitrary non-privileged port
		self.backlog = 10		# max number of connections. only one. check 0
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print('	Socket created')
		#Bind socket to local host and port
		try:
			self.s.bind((self.HOST, self.PORT))
		except socket.error as msg:
			print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
			#sys.exit()
			os._exit(0)
		print('	Socket bind complete')
		#Start listening on socket
		self.s.listen(self.backlog)
		print('	Socket now listening')
		self.cond = 1
		self.server_responce_message = "Hallo I am your server"
		self.start()
		print("	Server initialisation")


	def run(self):
		print("	Starting " + self.name)
		#now keep talking with the client
		while self.cond:
			#wait to accept a connection - blocking call
			conn, addr = self.s.accept()
			buf = conn.recv(64)
			#print 'Connected with ' + addr[0] + ':' + str(addr[1])
			#print 'Received: ' + buf
			if (addr[0]=='127.0.0.1'): # accept commands only from local host (wevserver)
				if buf=='GetData': 
					try:
						# One needs now to send message back!
						# with some data
						server_responce_message = self.mc.set_server_responce_message()
						conn.send(server_responce_message)
					except ValueError:
						print("Not a float")
						
				if buf=='Flush': 
					# This command will be sent to this ventillation server
					# to visualise the current measurements data 
					# The required operation here is just 
					# flush of the buffer into the current ouptput file:
					self.mc.visualise_data('current.png')

				if buf=='Reboot': 
					excommand = 'sudo reboot'
					os.system(excommand) # reboot to have new parameters working

				if buf=='Stop': 
					self.mc.auto =0
					print("		Automatic regim off")
					self.mc.stop_ventilation()
					print("		Stop ventilation done")
					try:
						self.mc.send_notification("Control is switched off via Stop request to server from user")
						print("		Email is sent")
					except:
						print("		Email is not sent")
						pass
					self.clean()
					print("		Clean is done. Exit:")
					os._exit(0)
					#sys.exit()

				if buf=='GetDeviceName': 
					try:
						server_responce_message = self.mc.get_device_name()
						conn.send(server_responce_message)
					except ValueError:
						print("GetDeviceName ERROR")

				if buf=='Auto': 
					self.mc.auto = 1;
					print('Auto')
					
				if buf=='Manually':
					self.mc.auto = 0;
					print('Manually')

				if buf=='StartVentilation':
					if (self.mc.auto==0):
						self.mc.start_ventilation();
						print('StartVentilation')

				if buf=='StopVentilation':
					if (self.mc.auto==0):
						self.mc.stop_ventilation();
						print('StopVentilation')


			conn.close()
			
		print("Exiting " + self.name)

		
	def clean(self):
		self.cond = 0 # set condition to stop thread loop
		# send message "Stop" 
		try:
			clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			clientsocket.connect((self.HOST, self.PORT))
			clientsocket.send("Stop")
		except:
			pass

