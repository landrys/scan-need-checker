from src.myMySql.myMySql import MyMySql
from src.mailSender import MailSender
import json
import os
import io
from matplotlib import pyplot as plt

class PercentUnscannedReport():

    _report=""
    _data=[]
    _xaxis=["14", "13", "11", "8"]
    _figs=[]
    _msgs=[]

    #_lazyScannerFinderQueryTemplate = "select (select count(*) from latest_scan_ac ls join item_location_scan_ac ils on ils.id=ls.item_location_scan join location l on ils.scan_location=l.id join serialized s on s.id=ils.serialized where l.top_level_id={} and s.customer_id is null and s.sale_line_id is null and s.lc_deleted is null and  ils.timestamp < date_add(now(), interval -{} day) ) / (select count(*) from latest_scan_ac ls join item_location_scan_ac ils on ils.id=ls.item_location_scan join location l on ils.scan_location=l.id join serialized s on s.id=ils.serialized where l.top_level_id={} and s.customer_id is null and s.sale_line_id is null and s.lc_deleted is null ) as fractionUnscanned"
    _lazyScannerFinderQueryTemplate = "select (select count(*) from latest_scan_ac ls join item_location_scan_ac ils on ils.id=ls.item_location_scan join location l on ils.scan_location=l.id join ascend_serialized s on s.id=ils.serialized where l.top_level_id={} and s.customer is null and s.deleted=0 and  ils.timestamp < date_add(now(), interval -{} day) ) / (select count(*) from latest_scan_ac ls join item_location_scan_ac ils on ils.id=ls.item_location_scan join location l on ils.scan_location=l.id join ascend_serialized s on s.id=ils.serialized where l.top_level_id={} and s.customer is null  and s.deleted =0 ) as fractionUnscanned"
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
        with open('src/private') as json_file:
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
            #self._report += str("\n")
            self._msgs.append(self._report)
            self._report=""
        else:
            self._report += str("Going {} days back the {} store has {}% of its bikes unscanned.\n".format(daysBack, store, percentUnscanned))



    def plotIt(self, store):
        plt.close()
        print(self._data)
        plt.bar(self._xaxis, self._data)
        plt.xlabel('Days Back')
        plt.ylabel('Percent Unscanned')
        plt.title('{} Unscanned Bikes Report'.format(store))
        plt.ylim(0,100)
        fig = io.BytesIO()
        plt.savefig(fig, format = 'png')
        fig.seek(0)
        self._figs.append(fig)





    def report(self):
        mysqlObj = MyMySql(self._host, self._user, self._password, self._database)
        for key  in self._stores:
            i=1
            self._data.clear()
            for daysBack in self._daysBack:
                self._lazyScannerFinderQuery=self._lazyScannerFinderQueryTemplate.format(self._stores[key], daysBack, self._stores[key])
                result = mysqlObj.fetch(self._lazyScannerFinderQuery)
                fractionUnscanned = result[0][0]
                self.buildReport(key, daysBack, fractionUnscanned*100, i)
                self._data.append(fractionUnscanned*100)
                i = i + 1
            fig = self.plotIt(key)

        mailSender = MailSender(self._mailSender, self._mailSenderPassword,\
                os.environ['reportEmailList'], "Unscanned Bikes Report", self._msgs,\
                self._figs)
        mailSender.send()
        self._figs.clear()

if __name__ == "__main__":
    pu = percentUnscannedReport()
    pu.report()

