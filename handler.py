from src.main import Main
from src.percentUnscannedReport import PercentUnscannedReport
import json

def main(event, context):
    print(str(event))
#    if str(event['report']).lower() == "true":
    if event['report']:
        pu = PercentUnscannedReport()
        pu.report()
    else:
        main = Main()
        main.run()

#if __name__ == "__main__":
#    main('WTF', '')
