import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os

def send(sender, password, recipient, subject, text, attachment_filename = False, attachment_content = False):
	
	try:
		if attachment_filename != False:
			message = MIMEMultipart()
		
			message['From'] = sender
			message['To'] = recipient
			message['Subject'] = subject
		
			message.attach(MIMEText(text))
		
			part = MIMEBase('application', 'octet-stream')
			part.set_payload(attachment_content)
			Encoders.encode_base64(part)
			part.add_header('Content-Disposition', 'attachment; filename="%s"' % attachment_filename)
			message.attachment(part)
			
			data = message.as_string()
			
		else:
			data = 'From: %s\nTo: %s\nSubject: %s\n\n%s' % (sender, recipient, subject, text)
	
		mail_server = smtplib.SMTP('smtp.gmail.com', 587)
		mail_server.ehlo()
		mail_server.starttls()
		mail_server.ehlo()
		mail_server.login(sender, password)
		mail_server.sendmail(sender, recipient, data)
		mail_server.close()
		
		return True
	except:
		return False