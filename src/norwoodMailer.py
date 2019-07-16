from src.mailer import Mailer
from src.mailSender import MailSender
import os

class NorwoodMailer(Mailer):

    def __init__(self):
        super().__init__()
        self._store=7
        self._storeName='Norwood'
        self._recipients=os.environ['norwoodEmailList']

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
        mailSender = MailSender(self._mailSender, self._mailSenderPassword,\
                self._recipients, self._subject, self._msg)
        mailSender.send()
