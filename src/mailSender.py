from smtplib import SMTP_SSL as SMTP #SSL connection
from smtplib import SMTPException
from smtplib import SMTPHeloError
from smtplib import SMTPAuthenticationError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class MailSender():


    def __init__(self, mailSender, mailSenderPassword, recipients, subject, message) -> None:
        self._msg = MIMEMultipart()
        self._sender = mailSender
        self._password = mailSenderPassword
        self._receivers = recipients.split(',')
        self._msg['To'] = recipients
        self._msg['Subject'] = subject
        self._message = message
        self._msg.attach(MIMEText(message))

    def send(self):
        ServerConnect = False
        try:
            smtp_server = SMTP('smtp.gmail.com','465')
            smtp_server.login(self._sender, self._password)
            ServerConnect = True
        except SMTPHeloError as e:
            print ("Server did not reply")
        except SMTPAuthenticationError as e:
            print ("Incorrect username/password combination" + e)
        except SMTPException as e:
            print ("Authentication failed")
        if ServerConnect == True:
            try:
                print(self._receivers)
                smtp_server.sendmail(self._sender, self._receivers, self._msg.as_string())
                print ("Successfully sent email")
            except SMTPException as e:
                print ("Error: unable to send email", e)
            finally:
                smtp_server.close()
