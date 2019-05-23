from src.mailer import Mailer
from src.mailSender import MailSender
import os

class NewtonMailer(Mailer):

    def __init__(self):
        super().__init__()
        self._store=12
        self._storeName='Newton'
        self._recipients=os.environ['newtonEmailList']

    @property
    def store(self):
        return self._store

    @property
    def storeName(self):
        return self._storeName

    @property
    def recipients(self):
        return self._recipients

    def mail(self):
        mailSender = MailSender(self._mailSender, self._mailSenderPassword, self._recipients, self._subject, self._msg)
        mailSender.send()
