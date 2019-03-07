#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


'''
	Test Server.

The aim is just to test Sending information from client to server and back
via socket modul, implemented as thread, so that the functioning 
of the main program is not affected

This program works together with TestClient.py or TestClient.php  


Usage:
sudo python -u /home/pi/TestServer.py  1>  /home/pi/tmp_TestServer_out.txt  2> /home/pi/tmp_TestServer_err.txt &

See some docs:
http://www.binarytides.com/python-socket-server-code-example/
https://stackoverflow.com/questions/7749341/very-basic-python-client-socket-example
https://de.wikipedia.org/wiki/Port_(Protokoll) 
https://steelkiwi.com/blog/working-tcp-sockets/

'''
 
import sys, time, datetime
from ServerThread import *      

thread1 = ServerThread(1, "Thread-1")  # Create new thread
thread1.start()  # Start new Threads

try:
	i = 0
	while 1:
		NowTime = datetime.datetime.today()
		now_time_str =  NowTime.strftime("%Y.%m.%d %H:%M:%S")
		print("main loop " + now_time_str)
		
		thread1.set_server_responce_message("new time" + now_time_str)
		
		time.sleep(2)
		i = i + 1
except KeyboardInterrupt: 
	print "Exiting Main Thread"
	thread1.clean()

# possibly Ctrl+C event should be processed or kill -15
