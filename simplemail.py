import ssl
from smtplib import SMTP, SMTP_SSL
from getpass import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart




class SimpleMail:
	"""
	A simple class for sending emails over SMTP. Uses the smtplib library.
	Emails are sent encrypted via SSL or TLS.

	smtp_server  = address of the SMTP server; string
	from_address = the email address used to login to the SMTP server send emails; string
	(use_ssl)    = specifies if connection should be over SSL instead of TLS (default=False); bool
	(port)       = SMTP server port (default = 465/587 for SSL/TLS); integer
	(password)   = password for the SMTP server (default = ask for input on init.); string
	(verbose)    = enables verbose smtplib readout to console (default = False); bool
	(feedback)   = enables helpful console readouts for key events (default = True); bool
	"""

	def __init__(self, smtp_server, from_address, use_ssl=False, port=None, password=None, feedback=True, verbose=False):
		"""Initiates the SMTP connection"""
		if not password:
			password = getpass(prompt='Enter SMTP Password: ')

		self.from_address = from_address

		if use_ssl: #SSL
			if not port:
				port = 465
			self.mail_server = SMTP_SSL(smtp_server, port, context=ssl.create_default_context())
		else: #TLS
			if not port:
				port = 587
			self.mail_server = SMTP(smtp_server, port)

		self.feedback = feedback
		self.verbose = verbose
		if verbose:
			self.mail_server.set_debuglevel(1)

		try:
			if not use_ssl: #TLS
				self.mail_server.starttls(context=ssl.create_default_context())
			self.mail_server.login(self.from_address, password)
			if self.feedback:
				print("SMTP Connection Opened")
		except:
			print("Error logging in to SMTP Server")
			self.mail_server.quit()


	def __enter__(self):
		"""initiates the connection when using with"""
		return self


	def sendPlain(self, to_address=[], cc_address=[], bcc_address=[], from_name="", subject="", message=""):
		"""
		Simple method for sending emails in plain text. Returns TRUE if sent successfully, returns FALSE if there was an error.

		(to_address) = list of email addresses (strings) to send the email to (default = []); list
		(cc_address) = list of email addresses (strings) to Cc on the email (default = []); list
		(bcc_address) = list of email addresses (strings) to Bcc on the email (default = []); list
		(from_name) = Name that shows up in the "From" line in email (default = from_address); string
		***WARNING: lots of errors seem to be caused by defining a from name.***
		(subject) = string that shows in the email's subject line (default = None); string
		(message) = the plaintext body of the email; string
		"""

		if not from_name:
			from_name = self.from_address

		message = f"From: {from_name}\r\nTo: {','.join(to_address)}\r\nCC: {','.join(cc_address)}\r\nSubject: {subject}\r\n{message}"
		toaddr = to_address + cc_address + bcc_address

		try:
			self.mail_server.sendmail(from_name, toaddr, message)
			if self.feedback:
				print("Email Sent Successfully!")
			return True
		except:
			print("Error Sending Mail")
			if from_name != self.from_address:
				print('Try sending without "from_name" declared.')
			return False

	def sendFancy(self, to_address=[], cc_address=[], bcc_address=[], from_name="", reply_to="", subject="", message_html="", message_plain=""):
		"""
		Simple method for sending MIME (alternative) emails. Returns TRUE if sent successfully, returns FALSE if there was an error.
		The HTML message (message_html) and plaintext message (message_plain) should be alternate versions of eachother.
		The plaintext message will only be shown if the client doesn't support HTML or the HTML message can not be rendered.

		(to_address) = list of email addresses (strings) to send the email to (default = []); list
		(cc_address) = list of email addresses (strings) to Cc on the email (default = []); list
		(bcc_address) = list of email addresses (strings) to Bcc on the email (default = []); list
		(from_name) = Name that shows up in the "From" line in email (default = from_address); string
		***WARNING: lots of errors seem to be caused by defining a from name.***
		(reply_to) = specifies the reply-to email address. (default = from_address); string
		(subject) = string that shows in the email's subject line (default = None); string
		(message_html) = the default (html) body of the email; string (HTML format)
		(message_plain) = the alternative (plaintext) body of the email; string

		Addresses may be specified with or without a name:
		"john-example@example.com" or "John Example <john-example@example.com>"
		"""

		if not from_name:
			from_name = self.from_address
		
		message = MIMEMultipart()
		message["Subject"] = subject
		message["From"] = from_name
		message["To"] = ','.join(to_address)
		message["Cc"] = ','.join(cc_address)
		if reply_to:
			message["Reply-To"] = reply_to

		message_body = MIMEMultipart("alternative")
		if message_plain:
			message_body.attach(MIMEText(message_plain, "plain"))
		if message_html:
			message_body.attach(MIMEText(message_html, "html"))
		message.attach(message_body)

		toaddr = to_address + cc_address + bcc_address

		try:
			self.mail_server.sendmail(from_name, toaddr, message.as_string())
			if self.feedback:
				print("Email Sent Successfully!")
			return True
		except:
			print("Error Sending Mail")
			if from_name != self.from_address:
				print('Try sending without "from_name" declared.')
			return False

	def close(self):
		"""Closes out the SMTP server"""
		try:
			self.mail_server.quit()
			if self.feedback:
				print("SMTP Connection Closed")
		except:
			None

	def __exit__(self, exc_type, exc_value, traceback):
		"""Closes out the SMTP server on exit"""
		try:
			self.mail_server.quit()
			if self.feedback:
				print("SMTP Connection Closed")
		except:
			None




def main():
	# smtp_server = ""
	# from_address = ""


	# to_address = [""]
	# message_body = "This is the body of the message"
	# message_HTML = """\
	# <html>
	#   <body>
	#     <h1>Hi,<br>
	#        How are you?<br>
	#        <a href="http://www.google.com">Google</a> 
	#     </h1>
	#   </body>
	# </html>
	# """

	#with SimpleMail(smtp_server, from_address) as email:
		#email.sendPlain(subject="This is Plain", to_address=to_address, message=message_body)
		#email.sendFancy(subject="This is Fancy", bcc_address=to_address, message_plain=message_body, message_html=message_HTML, reply_to="testing@xyz.com")

	# email = SimpleMail(smtp_server, from_address)
	# email.sendPlain(to_address=to_address, subject="Test")
	# email.close()

if __name__ == '__main__':
	main()
