'''
Created on Dec 19, 2010

@author: ppa
'''
from ultrafinance.processChain.baseModule import BaseModule

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import json, smtplib

import logging
LOG = logging.getLogger(__name__)

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

class EmailOutputer(BaseModule):
    ''' Default feeder '''
    def __init__(self):
        ''' constructor '''
        super(EmailOutputer, self).__init__()

    def execute(self, input):
        ''' do output'''
        super(EmailOutputer, self).execute(input)
        print 'sending email'
        mail("des@gmail.com", json.dumps(input))
        return None