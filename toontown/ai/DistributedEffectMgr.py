from direct.distributed.DistributedObject import DistributedObject
from otp.speedchat import SpeedChatGlobals
import HolidayGlobals

class DistributedEffectMgr(DistributedObject):

    def delete(self):
        self.ignoreAll()
        DistributedObject.delete(self)

    def setHoliday(self, holiday):
        self.holiday = holiday
        print 'holiday is %s' % self.holiday
        self.accept(SpeedChatGlobals.SCStaticTextMsgEvent, self.__saidPhrase)

    def __saidPhrase(self, phraseId):
        if not self.cr.newsManager.isHolidayRunning(self.holiday):
            return

        holidayInfo = HolidayGlobals.getHoliday(self.holiday)

        if 'speedchatIndex' not in holidayInfo or phraseId != holidayInfo['speedchatIndex']:
            return

        self.sendUpdate('addEffect')
        self.cr.newsManager.broadcastHoliday(holidayInfo, 'effectMessage')