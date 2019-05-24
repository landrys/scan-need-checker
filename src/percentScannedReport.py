from myMySql.myMySql import MyMySql
import json
import os

class percentScannedReport():

    _report=""

    _lazyScannerFinderQueryTemplate = "select (select count(*) from latest_scan_ac ls join item_location_scan_ac ils on ils.id=ls.item_location_scan join location l on ils.scan_location=l.id join serialized s on s.id=ils.serialized where l.top_level_id={} and s.customer_id is null and s.sale_line_id is null and s.lc_deleted is null and  ils.timestamp < date_add(now(), interval -{} day) ) / (select count(*) from latest_scan_ac ls join item_location_scan_ac ils on ils.id=ls.item_location_scan join location l on ils.scan_location=l.id join serialized s on s.id=ils.serialized where l.top_level_id={} and s.customer_id is null and s.sale_line_id is null and s.lc_deleted is null ) as fractionUnscanned"
    _lazyScannerFinderQuery = ""

    _daysBack = [14, 13, 11, 8]
    _stores = {'Natick': 1,
            'Boston': 2,
            'Central': 4,
            'Westboro': 5,
            'Norwood': 7,
            'Braintree': 9,
            'Worcester':10,
            'Newton': 12
            }

    def __init__(self) -> None:
        with open('private') as json_file:
            data = json.load(json_file)
            self._host = os.environ['host']
            self._user = data['user']
            self._password = data['password']
            self._database = data['database']
            self._mailSender = data['mailSender']
            self._mailSenderPassword = data['mailSenderPassword']

    def buildReport(self, store, daysBack, percentUnscanned, i):
        #self._report.append("Going {} days back the {} store has {}% of its bikes unscanned.\n".format(daysBack, store, percentUnscanned))
        if ( i == 4 ):
            self._report += str("Going {} days back the {} store has {}% of its bikes unscanned.\n".format(daysBack, store, percentUnscanned))
            self._report += str("\n")
        else:
            self._report += str("Going {} days back the {} store has {}% of its bikes unscanned.\n".format(daysBack, store, percentUnscanned))



    def report(self):
        mysqlObj = MyMySql(self._host, self._user, self._password, self._database)
        for key  in self._stores:
            i=1
            for daysBack in self._daysBack:
                self._lazyScannerFinderQuery=self._lazyScannerFinderQueryTemplate.format(self._stores[key], daysBack, self._stores[key])
                result = mysqlObj.fetch(self._lazyScannerFinderQuery)
                fractionUnscanned = result[0][0]
                self.buildReport(key, daysBack, fractionUnscanned*100, i)
                i = i + 1
            i=1
        print(self._report)

if __name__ == "__main__":
    ps = percentScannedReport()
    ps.report()

