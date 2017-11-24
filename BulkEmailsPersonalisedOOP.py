import json
import smtplib
import getpass
from datetime import datetime
from email.mime.text import MIMEText

#TODO: add check details if login not successful

class BulkEmailsPersonalisedOOP():

    def __init__(self):
        
        self.deetsFile = ''
        self.sender = ''
        self.password = ''
        self.recList = []
        self.host = ''
        self.port = 0
        self.reportText = ''
        self.reportFile = ''

        print("Bulk emails - personalised\n")
        self.getFiles()
        self.getList()
        self.getLoginDeets()
        self.logonAndSend()
        self.reportSave()
    

    #get file details and confirm input with user before continuing
        
    def getFiles(self):
        while True:
            filename = input("Enter the name of the recipient text file (include full path if in different directory):")
            reportName = input("Enter the name for report text file (include full path if in different directory):")

            print("\nRecipient details file: " + filename)
            print("Report file name: " + reportName)
            conf = str(input("Is this correct? y/n: \n")).strip().upper()
            if conf == 'Y':
                self.deetsFile = filename
                self.reportFile = reportName
                break
            elif conf == 'N':
                 continue
            else:
                print("Invalid selection.")
 
        
    #get host and port, sender email and password
            
    def getLoginDeets(self):
        while True: 
            host = input("Enter host: ")
            port = input("Enter port: ")
            try:
                int(port)
            except:
                print("Exception: Port number must be an integer.")
                port = input("Enter port: ")
            sender = input("Enter the sender email address: ")
            password = getpass.getpass("Enter password: \n")
            
            print("Host: " + host)
            print("Port: " + str(port))
            print("From email: " + sender)
            conf = input("Are these details correct? y/n: \n").strip().upper()

            if conf == 'Y':
                self.host = host
                self.port = int(port)
                self.sender = sender
                self.password = password
                break
            elif conf == 'N':
                continue
            else:
                print("Invalid selection.\n")



    #get recipient details from file and save to iterable list

    def getList(self):
        f = open(self.deetsFile,'r')
        self.recList = json.load(f)
        f.close()

        
    #repeatedly attempt login until successful, add failed and successful login attempts to report
    #check details with user if login unsuccessful
        
    def logonAndSend(self):

        host = self.host
        port = self.port
        sndr = self.sender
        pwrd = self.password
        report = ''
        
        print("Attempting to connect to server...\n")
        while True:
            try:
                server = smtplib.SMTP(host, port)
                server.starttls()
                server.login(sndr, pwrd)
                print('login successful')
                now = str(datetime.now())
                report = report + 'Login successful at: %s \n' %now
                break
            except:
                print('Login failed.')
                now = str(datetime.now())
                report = report + 'Login failed at: %s \n' %now
                                    
        
    #iterate through list of recipients, customising message details for each and sending email
    #update report for each email sent/not sent
                        
        for item in self.recList:
            
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
                text = 'Message sent to %s at: %s \n' %(recr, now)
                report = report + text
                
            except:
                now = str(datetime.now())
                text = 'Message not sent to %s at: %s \n' %(recr, now)
                report = report + text
                
        #quit server after attempting all items in list and update report
        server.close()
        print('Server session terminated')
        now = str(datetime.now())
        report = report + 'Server session terminated at: %s \n' %now

        self.reportText = self.reportText + report

          
    #save report details to text file
        
    def reportSave(self):
        filename = self.reportFile
        text = self.reportText
        
        f = open(filename,'w')
        f.write(text)
        f.close()
        print('Report ready for viewing.')
        

if __name__ == '__main__':
    run = BulkEmailsPersonalisedOOP()

