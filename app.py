import sys
import imaplib
import email
from email.header import decode_header
import getpass
import re



def connect(user, pwd, server='imap.gmail.com'):
	conn = imaplib.IMAP4_SSL(server)

	try:
		conn.login(user, pwd)
	except Exception as err:
		print("Failed to login")
		print(err)		
		sys.exit(1)
	
	return conn



if __name__ == "__main__":
	username = input("Full email address: ")
	password = getpass.getpass()

	mail_conn = connect(username, password)

	status, messages = mail_conn.select("INBOX")

	N=3

	messages = int(messages[0])

	for i in range(messages, messages-N, -1):
		res, msg = mail_conn.fetch(str(i), "(RFC822)")
		for response in msg:
			if isinstance(response, tuple):
				msg = email.message_from_bytes(response[1])
				subject, encoding = decode_header(msg["Subject"])[0]

				if isinstance(subject, bytes):                	
					subject = subject.decode(encoding)

				From, encoding = decode_header(msg.get("From"))[0]

				if isinstance(From, bytes):
					From = From.decode(encoding)

				print("Subject:", subject)
				print("From:", From)