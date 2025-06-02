from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
from threading import Thread
import os

load_dotenv()

EMAIL = os.getenv("AUTOMAILER_EMAIL")
PASSW = os.getenv("AUTOMAILER_PASSW")

def sendMail(mailTo: str, content):
  Smtp = SMTP("smtp.gmail.com", 587)
  Smtp.ehlo()
  Smtp.starttls()
  Smtp.login(EMAIL, PASSW)
  Smtp.sendmail(EMAIL, mailTo, content)
  Smtp.close()

def htmlMailer(mailTo: str, subject: str, htmlRendered: str):
  messageMime = MIMEMultipart()
  messageMime["from"] = EMAIL
  messageMime["to"] = mailTo
  messageMime["subject"] = subject

  messageMime.attach(MIMEText(htmlRendered, "html"))
  Smtp = SMTP("smtp.gmail.com", 587)
  Smtp.ehlo()
  Smtp.starttls()
  Smtp.login(EMAIL, PASSW)
  Smtp.sendmail(EMAIL, mailTo, messageMime.as_string())

def threadedHtmlMailer(mailTo: str, subject: str, htmlRendered: str):
  th = Thread(target=htmlMailer, args=(mailTo, subject, htmlRendered))
  th.daemon = True
  th.start()
