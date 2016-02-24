#!/usr/bin/env python
import datetime

from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import smtplib
import sys

recipients = ['pixatintes@yahoo.es']
emaillist = [elem.strip().split(',') for elem in recipients]
msg = MIMEMultipart()
msg['Subject'] = str(sys.argv[1])
msg['From'] = 'pixatintes@gmail.com'
msg['Reply-to'] = 'pixatintes@gmail.com'
 
msg.preamble = 'Multipart massage.\n'
 
with open(str(sys.argv[2]), "rt") as in_file:
     values = in_file.read()

now = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M")

part = MIMEText("Bon dia, els resultats a" + str(now) + " son: \n" + str(values))
msg.attach(part)


part = MIMEApplication(open(str(sys.argv[2]),"rb").read())
part.add_header('Content-Disposition', 'attachment', filename=str(sys.argv[2]))
msg.attach(part)
 

server = smtplib.SMTP("smtp.gmail.com:587")
server.ehlo()
server.starttls()
server.login("pixatintes@gmail.com", "48papall0nes")
 
server.sendmail(msg['From'], emaillist , msg.as_string())
