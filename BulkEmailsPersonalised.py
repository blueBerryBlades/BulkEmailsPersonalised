#!/usr/bin/env python

import json
import smtplib
from datetime import datetime
from email.mime.text import MIMEText

#file with recipient details
#details should be saved as a list of dictionaries
#each dictionary, one per recipient, should have the keys: 'name', 'email, 'deets'

file = 'filename'
recList = []
report = ''
sndr = 'sender@email'
pwrd = 'password'
host = 'your-email.host'
port = portNumber


#get recipient details from file

f = open(file,'r')
recList = json.load(f)
f.close()

#logon to server and send test message and update report

while True:
    try:
        server = smtplib.SMTP(host, port)
        server.starttls()
        server.login(sndr, pwrd)
        print('login successful')
        now = str(datetime.now())
        report = report + 'Login successful at: %s \n' %now
    
        #uncomment and edit following 6 lines to send test email
        #recr = 'test@email'
        #msg = 'message'
        #server.sendmail(sndr, recr, msg)
        #print('test msg send successful')
        #now = str(datetime.now())
        #report = report + 'Test message sent at: %s \n' %now
        break
    except:
        print('Login failed.  Trying again.')
        now = str(datetime.now())
        report = report + 'Login failed at: %s \n' %now
        
#iterate through list of recipients
        
for item in recList:

    #declare variables for each recipient
    #convert to string from unicode
    recr = str(item['email'])
    name = str(item['name'])
    deet = str(item['deets'])

    #construct message
    body = """Dear %s,
\nConstructed this way the email can include personal %s.
\nFurther action or information in message body.
\nKind regards,
\nWhomever
""" %(name, deet)

    msg = MIMEText(body.encode('utf-8'), 'plain', 'utf-8')
    msg['To'] = recr
    msg['From'] = sndr
    msg['Subject'] = 'An important message for %s.' %name

    #send email  and update report with success/failure
    try:
        server.sendmail(sndr, recr, msg.as_string())
        now = str(datetime.now())
        text = 'Message sent to %s at: %s \n' %(now, recr)
        report = report + text
    except:
        now = str(datetime.now())
        text = 'Message not sent to %s at: %s \n' %(now, recr)
        report = report + text

#quit server after attempting all items in list and update report
server.close()
print('Server session terminated')
now = str(datetime.now())
report = report + 'Server session terminated at: %s \n' %now
      
#save report details to text file

f = open('report.txt','w')
f.write(report)
f.close()
print('Report ready for viewing.')

#lines with print() can be commented out
#if no progress information is required
#while program is running

#if dictionaries contained further fields
#the message content could easily be further personalised
#by creating and using more variables at start of for loop

#after customising .py file
#chmod 755 (or otherwise make executable)
#make sure file with recipient details is in same directory
#or include full path to file in filename


























