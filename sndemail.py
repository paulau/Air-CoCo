#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Python script um info email zu schicken
"""
from smtplib import SMTP
import datetime
from email.mime.text import MIMEText  # Import the email modules we'll need

def sndemail(emailto, emailfrom, mailserver, passwmail, esbj, emsg):

	debuglevel = 0
	smtp = SMTP()
	smtp.set_debuglevel(debuglevel)
	print('mailserver : ' + mailserver)
	smtp.connect(mailserver, 587)
	smtp.login(emailfrom, passwmail)
	date = datetime.datetime.now().strftime( "%d/%m/%Y %H:%M" )
	msg = MIMEText("Raspberry Restart\n" + date + "\n" + "\n" + emsg)
	msg['Subject'] = esbj
	msg['From'] = emailfrom
	msg['To'] = emailto
	
	print(emailfrom)
	print([emailto])
	print(msg.as_string())
	
	smtp.sendmail(emailfrom, [emailto], msg.as_string())
	smtp.quit()
