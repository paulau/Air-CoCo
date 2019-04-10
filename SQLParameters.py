#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#the default username is 'root' and by default there is no password.
class SQLPar():
	def __init__(self):
		self.Server = 'localhost'
		self.User = 'root'
		self.Passwd = ''
		self.Database = 'AirCoCo'
		self.Table = 'Parameters'
