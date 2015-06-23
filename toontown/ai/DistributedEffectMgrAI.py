from direct.distributed.DistributedObjectAI import DistributedObjectAI
import HolidayGlobals

class DistributedEffectMgrAI(DistributedObjectAI):

    def __init__(self, air, holiday, effectId):
        DistributedObjectAI.__init__(self, air)
        self.holiday = holiday
        self.effectId = effectId

    def getHoliday(self):
        return self.holiday

    def addEffect(self):
        if not self.air.newsManager.isHolidayRunning(self.holiday):
            return

        av = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not av:
            return

        holiday = HolidayGlobals.getHoliday(self.holiday)
        expireTime = int(HolidayGlobals.getUnixTime(HolidayGlobals.getEndDate(holiday)) / 60)

        av.b_setCheesyEffect(self.effectId, 0, expireTime)