'''
Created on Dec 19, 2010

@author: ppa
'''
import smtplib
from outputer.BaseOutputer import BaseOutputer
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import json

gmail_user = "your@gmail.com"
gmail_pwd = "your_password"

def mail(to, text):
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = to
    msg['Subject'] = 'Ultra-Finance'

    msg.attach(MIMEText(text))
    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()

class EmailOutputer(BaseOutputer):
    ''' Default feeder '''
    def before(self):
        ''' init output '''
        print 'before output'
        
    def after(self):
        ''' close output '''
        print 'after output'
        
    def run(self, data):
        ''' do output'''
        print 'sending email'
        mail("des@gmail.com", json.dumps(data))
        return True