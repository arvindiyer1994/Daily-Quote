import smtplib
from randomAccessReader import RandomAccessReader
import random
import time
import sqlite3

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

#Email Variables
SMTP_SERVER = 'smtp.gmail.com' #Email Server (don't change!)
SMTP_PORT = 587 #Server Port (don't change!)
GMAIL_USERNAME = '' #Set this to match your gmail account
GMAIL_PASSWORD = ''  #change this to match your gmail password
N = 75967

class Emailer:
    def sendmail(self, recipient, subject, content,image):

        #Create Headers
        #headers = ["From: " + GMAIL_USERNAME, "Subject: " + subject, "To: " + recipient,
        #           "MIME-Version: 1.0", "Content-Type: text/html"]
        #headers = "\r\n".join(headers)
        emailData = MIMEMultipart()
        emailData['Subject'] = subject
        emailData['To'] = recipient
        emailData['From'] = GMAIL_USERNAME

        #Attach our text data  
        emailData.attach(MIMEText(content))

        #Create our Image Data from the defined image
        imageData = MIMEImage(open(image, 'rb').read(), 'jpg') 
        imageData.add_header('Content-Disposition', 'attachment; filename="image.jpg"')
        emailData.attach(imageData)

        #Connect to Gmail Server
        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        session.ehlo()
        session.starttls()
        session.ehlo()

        #Login to Gmail
        session.login(GMAIL_USERNAME, GMAIL_PASSWORD)

        #Send Email & Exit
        #session.sendmail(GMAIL_USERNAME, recipient, headers + "\r\n\r\n" + content)
        session.sendmail(GMAIL_USERNAME, recipient, emailData.as_string())
	session.quit

sender = Emailer()



###################################################################################################################################
#                                                  Email to send                                                                  #
###################################################################################################################################
sendTo = '' # The email you want to send the email to
emailSubject = "Daily Motivational Quotes"


###################################################################################################################################
#                                            Pick random number form quotes                                                       #
###################################################################################################################################
random_number = random.randint(1,N)
conn = sqlite3.connect('quotes.db')
cursor = conn.execute("SELECT  * from QUOTES where id="+str(random_number)+";")

for row in cursor:
	mailcontent = row[1] + " " + row[2] + " " +row[3]
conn.close()

print(mailcontent)

#Sends an email to the "sendTo" address with the specified "emailSubject" as the subject and "emailContent" as the email content.
sender.sendmail(sendTo, emailSubject, mailcontent,image)
print('Email sent')
