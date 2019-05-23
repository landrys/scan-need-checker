from src.natickMailer import NatickMailer
from src.bostonMailer import BostonMailer
from src.westboroMailer import WestboroMailer
from src.worcesterMailer import WorcesterMailer
from src.newtonMailer import NewtonMailer
from src.norwoodMailer import NorwoodMailer
from src.braintreeMailer import BraintreeMailer
from src.centralMailer import CentralMailer
from src.scanNeedChecker import ScanNeedChecker

class Main:

    def run(self):
        scanCheck = ScanNeedChecker(NatickMailer())
        scanCheck.check()
        scanCheck.mailer = BostonMailer()
        scanCheck.check()
        scanCheck.mailer = WestboroMailer()
        scanCheck.check()
        scanCheck.mailer = WorcesterMailer()
        scanCheck.check()
        scanCheck.mailer = NewtonMailer()
        scanCheck.check()
        scanCheck.mailer = BraintreeMailer()
        scanCheck.check()
        scanCheck.mailer = NorwoodMailer()
        scanCheck.check()
        scanCheck.mailer = CentralMailer()
        scanCheck.check()
        print("Done Checking.")



