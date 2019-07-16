from src.mailer import Mailer
from src.mailSender import MailSender
from src.myMySql.myMySql import MyMySql
import json
import os

class ScanNeedChecker():

    _lazyScannerFinderQueryTemplate = "select (select count(*) from latest_scan_ac ls join item_location_scan_ac ils on ils.id=ls.item_location_scan join location l on ils.scan_location=l.id join ascend_serialized s on s.id=ils.serialized where l.top_level_id={} and s.customer is null  and s.deleted=0 and  ils.timestamp < date_add(now(), interval -{} day) ) / (select count(*) from latest_scan_ac ls join item_location_scan_ac ils on ils.id=ls.item_location_scan join location l on ils.scan_location=l.id join ascend_serialized s on s.id=ils.serialized where l.top_level_id={} and s.customer is null and s.deleted =0 ) as fractionUnscanned"
    _lazyScannerFinderQuery = ""

    _daysBack = [14, 13, 11, 8]

    def __init__(self, mailer: Mailer) -> None:

        """
        Usually, the Context accepts a mailer through the constructor, but
        also provides a setter to change it at runtime.
        """

        self._mailer = mailer
        self._lazyScannerFinderQuery = ""

        with open('src/private') as json_file:
            data = json.load(json_file)
            self._host = os.environ['host']
            self._user = data['user']
            self._password = data['password']
            self._database = data['database']
            self._mailSender = data['mailSender']
            self._mailSenderPassword = data['mailSenderPassword']

        self._mailer.mailSender = self._mailSender
        self._mailer.mailSenderPassword = self._mailSenderPassword

    @property
    def mailer(self) -> Mailer:
        """
        The Context maintains a reference to one of the Mailer objects. The
        Context does not know the concrete class of a mailer. It should work
        with all strategies via the Mailer interface.
        """

        return self._mailer

    @mailer.setter
    def mailer(self, mailer: Mailer) -> None:
        """
        Usually, the Context allows replacing a Mailer object at runtime.
        """
        self._mailer = mailer
        self._mailer.mailSender = self._mailSender
        self._mailer.mailSenderPassword = self._mailSenderPassword


    def alert(self, daysBack, percentUnscanned):
        self._mailer.percentUnscanned = percentUnscanned
        self._mailer.daysBack = daysBack
        self._mailer.setMessage()
        self._mailer.mail()

    def check(self):

        """
        The Context delegates some work to the Mailer object instead of
        implementing multiple versions of the algorithm on its own.
        """
        """ Here include logic to query the DB and check if this store needs to do scans.
        Grab stuff from json file
        https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
        """
        mysqlObj = MyMySql(self._host, self._user, self._password, self._database)
        for daysBack in self._daysBack:
             self._lazyScannerFinderQuery=self._lazyScannerFinderQueryTemplate.format(self._mailer.store,daysBack,self._mailer.store)
             result = mysqlObj.fetch(self._lazyScannerFinderQuery)
             fractionUnscanned = result[0][0]
             if fractionUnscanned < 0.75:
                 next
             else:
                 self.alert(daysBack, fractionUnscanned*100)
                 break
