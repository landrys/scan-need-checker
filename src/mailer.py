from abc import ABC, abstractmethod
from datetime import date
from datetime import timedelta 

class Mailer(ABC):
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm.

    The Context uses this interface to call the algorithm defined by Concrete
    Strategies.
    """

    def __init__(self):
        self._msgTemplate = "{} has {} percent of its bikes last scan date older than {} days."
        self._subject = "Scan Expiration Hot Potato"
        self._mailSender = "landryseleven@crap.com"
        self._mailSenderPassword = "123456"
        self._daysBack = 0
        self._percentUnscanned = 0
        self._msg = ""
        self._lastScanDate = "01/01/99"
        self._lastScanDatePlus14 = "01/15/99"

    @property
    def mailSender(self):
        return self._mailSender

    @mailSender.setter
    def mailSender(self, mailSender):
        self._mailSender = mailSender

    @property
    def mailSenderPassword(self):
        return self._mailSenderPassword

    @mailSenderPassword.setter
    def mailSenderPassword(self, mailSenderPassword):
        self._mailSenderPassword = mailSenderPassword

    @property
    def percentUnscanned(self):
        return self._percentUnscanned

    @percentUnscanned.setter
    def percentUnscanned(self, percentUnscanned):
        self._percentUnscanned = percentUnscanned

    @property
    def daysBack(self):
        return self._daysBack

    @daysBack.setter
    def daysBack(self, daysBack):
        self._daysBack = daysBack
        self._setTheDates()

    def _setTheDates(self):
        self._lastScanDate = date.today() + timedelta(days=-self._daysBack)
        self._lastScanDatePlus14 = self._lastScanDate + timedelta(days=14)

    def setMessage(self):
        if self._daysBack == 8:
           self._msg = """
Hello!  Your store's last complete bike scan was on {} These scans will expire on {}.
Please scan your bikes before the expiration date!
"""
           self._msg = self._msg.format(self._lastScanDate, self._lastScanDatePlus14)

        elif self._daysBack == 11:
           self._msg = """
Hello!  Urgent action required to scan your bikes before the scans expire!
Your store's last complete bike scan was on {}
These scans will expire on {}.
"""
           self._msg = self._msg.format(self._lastScanDate, self._lastScanDatePlus14)

        elif self._daysBack == 13:
           self._msg = """
Your bike scans will expire tomorrow and Transferator won't know what to send you for stock anymore!
Please scan all your bikes today.
"""

        elif self._daysBack == 14:
           self._msg = """
Your bike scans are expired and you will not get any new stock transfers. 
Please scan bikes today so you get bikes for stock tomorrow.
"""
        self._msg = self._msg + self._storeName + ":{}:{}".format(self._percentUnscanned, self._daysBack)


    @abstractmethod
    def mail(self):
        pass


