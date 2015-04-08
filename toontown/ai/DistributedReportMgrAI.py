from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.uberdog.ClientServicesManagerUD import executeHttpRequestAndLog
import ReportGlobals, threading

class DistributedReportMgrAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedReportMgrAI")

    def __init__(self, air):
        DistributedObjectAI.DistributedObjectAI(self, air)
        self.reports = []
        self.interval = config.GetInt('report-interval', 600)
        self.scheduleReport()
    
    def scheduleReport(self):
        threading.Timer(self.interval, self.sendAllReports)
    
    def sendReport(self, avId, category):
        if not ReportGlobals.isValidCategoryName(category) or not len(str(avId)) == 9:
            return
        
        reporterId = self.air.getAvatarIdFromSender()
        reporter = self.air.doId2do.get(reporterId)
        
        if not reporter or reporter.isReported(avId):
            return
        
        timestamp = int(round(time.time() * 1000))
        self.reports.append('%s|%s|%s|%s' % (timestamp, reporterId, avId, category))
    
    def sendAllReports(self):
        if not self.reports or config.GetString('accountdb-type', 'developer') != 'remote'::
            return
        
        executeHttpRequestAndLog('report', reports=','.join(self.reports))
        self.reports = []
        self.scheduleReport()