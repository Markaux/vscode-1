#coding: utf-8
import smtplib

def sendmsg(receivers, message):
    relay = 'application-qua.emea.smtp.cib.net'
    #relay = 'application.emea.smtp.cib.net'
    sender = 'middleware@natixis.com'

    try:
        smtpObj = smtplib.SMTP(relay)
        smtpObj.sendmail(sender, receivers, message)
        return "Successfully sent email"
    except smtplib.SMTPException:
        return "Error: unable to send email"


# ______ MAIN ______
receivers = ['marc.celerier@natixis.net']
message = """From: From Person <marc.celerier@natixis.net>
    To: To Person <marc.celerier@natixis.net>
    Subject: SMTP e-mail test

    This is a test e-mail message.
   """
print(sendmsg(receivers, message))
