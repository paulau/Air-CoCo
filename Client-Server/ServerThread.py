#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Usage of the class:

# do it potentially in constructor of the MoniControl:
thread1 = ServerThread(1, "Thread-1")  # Create new thread
thread1.start()  # Start new Threads

# do it potentially every time, when state was updatet:
thread1.set_server_responce_message("string responce")
# not too efficient. But ok. Better could be update message only on request
# of clients

# do it on clean
thread1.clean()
"""

import socket, threading, sys

class ServerThread (threading.Thread): # we inherite Thread!
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name      
		self.HOST = 'localhost'  # ' ' Symbolic name, meaning all available interfaces
		self.PORT = 40012 		# 8888 Arbitrary non-privileged port
		self.backlog = 10		# max number of connections. only one. check 0
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print 'Socket created'
		#Bind socket to local host and port
		try:
			self.s.bind((self.HOST, self.PORT))
		except socket.error as msg:
			print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
			sys.exit()
		print 'Socket bind complete'
		#Start listening on socket
		self.s.listen(self.backlog)
		print 'Socket now listening'
		self.cond = 1
		
		self.server_responce_message = "Hallo I am your server"

	def run(self):
		print "Starting " + self.name
		#now keep talking with the client
		while self.cond:
			#wait to accept a connection - blocking call
			conn, addr = self.s.accept()
			buf = conn.recv(64)
			print 'Connected with ' + addr[0] + ':' + str(addr[1])
			print 'Received: ' + buf
			if buf=='GetData': 
				try:
					print(buf)
					# One needs now to send message back!
					# with some data
					conn.send(self.server_responce_message)
				except ValueError:
					print "Not a float"
		
			conn.close()
		
			if buf=='Stop': 
				self.s.close()

		print "Exiting " + self.name 
		
	
	def set_server_responce_message(self,message):
		self.server_responce_message = message

	def clean(self):
		self.cond = 0 # set condition to stop thread loop
		# send message "Stop" 
		try:
			clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			clientsocket.connect((self.HOST, self.PORT))
			clientsocket.send("Stop")
		except:
			pass
