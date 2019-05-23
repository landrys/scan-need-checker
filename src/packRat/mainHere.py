"""
from natickMailer import NatickMailer
from bostonMailer import BostonMailer
from lazyScannerChecker import LazyScannerChecker
"""
from src.myMySql.myMySql import MyMySql
import json

class MyMain:

    def __init__(self) -> None:

        with open('src/private') as json_file:
            data = json.load(json_file)
            self._host = data['host']
            self._user = data['user']
            self._password = data['password']
            self._database = data['database']



    def run(self):
        print("I'm off and running")
        print(self._host)

        mysqlObj = MyMySql(self._host, self._user, self._password, self._database)
        result = mysqlObj.fetch("select count(*) from product")
        print (result[0][0])


        """
        scanCheck = LazyScannerChecker(BostonMailer())
        scanCheck.check()
        scanCheck.mailer = NatickMailer()
        scanCheck.check()
        """
