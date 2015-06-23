from direct.distributed.DistributedObject import DistributedObject
from toontown.estate import Estate
from toontown.toonbase import ToontownGlobals
import HolidayGlobals

class NewsManager(DistributedObject):
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.invading = False
        self.activeHolidays = []
        base.localAvatar.inventory.setInvasionCreditMultiplier(1)
        base.cr.newsManager = self

    def delete(self):
        self.cr.newsManager = None
        DistributedObject.delete(self)

    def isHolidayRunning(self, id):
        return id in self.activeHolidays
    
    def startHolidays(self, ids):
        for id in ids:
            self.startHoliday(id, True)
    
    def getDecorationHolidayId(self):
        return []

    def broadcastHoliday(self, holiday, type):
        if type in holiday:
            base.localAvatar.setSystemMessage(0, holiday[type])
    
    def startHoliday(self, id, ongoing=False):
        if id in self.activeHolidays or id not in HolidayGlobals.Holidays:
            return

        holiday = HolidayGlobals.getHoliday(id)
        
        self.activeHolidays.append(id)
        self.broadcastHoliday(holiday, 'ongoingMessage' if ongoing else 'startMessage')
        self.startSpecialHoliday(id)

    def endHoliday(self, id):
        if id not in self.activeHolidays or id not in HolidayGlobals.Holidays:
            return

        holiday = HolidayGlobals.getHoliday(id)

        self.activeHolidays.remove(id)
        self.broadcastHoliday(holiday, 'endMessage')
        self.endSpecialHoliday(id)

    def startSpecialHoliday(self, id):
        if id == ToontownGlobals.LAUGHING_MAN:
            for toon in base.cr.toons.values():
                toon.generateLaughingMan()
        elif id == ToontownGlobals.APRIL_TOONS_WEEK:
            if isinstance(base.cr.playGame.getPlace(), Estate.Estate):
                base.localAvatar.startAprilToonsControls()

            base.localAvatar.chatMgr.chatInputSpeedChat.addAprilToonsMenu()
        elif id == ToontownGlobals.IDES_OF_MARCH:
            base.localAvatar.chatMgr.chatInputSpeedChat.addIdesOfMarchMenu()

    def endSpecialHoliday(self, id):
        if id == ToontownGlobals.LAUGHING_MAN:
            for toon in base.cr.toons.values():
                toon.swapToonHead(laughingMan=toon.getWantLaughingMan())
        elif id == ToontownGlobals.APRIL_TOONS_WEEK:
            if isinstance(base.cr.playGame.getPlace(), Estate.Estate):
                base.localAvatar.stopAprilToonsControls()

            base.localAvatar.chatMgr.chatInputSpeedChat.removeAprilToonsMenu()
        elif id == ToontownGlobals.IDES_OF_MARCH:
            base.localAvatar.chatMgr.chatInputSpeedChat.removeIdesOfMarchMenu()