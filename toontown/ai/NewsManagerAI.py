from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.task import Task
from datetime import datetime
from toontown.toonbase import ToontownGlobals
import HolidayGlobals

class NewsManagerAI(DistributedObjectAI):

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.activeHolidays = []
    
    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)
        self.__checkHolidays()
        self.checkTask = taskMgr.doMethodLater(15, self.__checkHolidays, 'holidayCheckTask')
        self.accept('avatarEntered', self.__handleAvatarEntered)
    
    def delete(self):
        DistributedObjectAI.delete(self)
        taskMgr.remove(self.checkTask)
    
    def __handleAvatarEntered(self, av):
        self.sendUpdateToAvatarId(av.getDoId(), 'setActiveHolidays', [self.activeHolidays])
    
    def getActiveHolidays(self):
        return self.activeHolidays
    
    def __checkHolidays(self, task=None):
        date = datetime.now()

        for id in HolidayGlobals.Holidays:
            holiday = HolidayGlobals.Holidays[id]
            running = self.isHolidayRunning(id)
            
            if ('weekDay' not in holiday or date.weekday() == holiday['weekDay']) and ('startMonth' not in holiday or holiday['startMonth'] <= date.month <= holiday['endMonth']) and ('startDay' not in holiday or holiday['startDay'] <= date.day <= holiday['endDay']):
                if not running:
                    self.startHoliday(id)
            elif running:
                self.endHoliday(id)

        return Task.again

    def isHolidayRunning(self, id):
        return id in self.activeHolidays

    def startHoliday(self, id):
        if id in self.activeHolidays or id not in HolidayGlobals.Holidays:
            return

        self.activeHolidays.append(id)
        self.startSpecialHoliday(id)
        self.sendUpdate('startHoliday', [id])
    
    def endHoliday(self, id):
        if id not in self.activeHolidays or id not in HolidayGlobals.Holidays:
            return

        self.activeHolidays.remove(id)
        self.endSpecialHoliday(id)
        self.sendUpdate('endHoliday', [id])
    
    def startSpecialHoliday(self, id):
        if id == ToontownGlobals.FISH_BINGO or id == ToontownGlobals.SILLY_SATURDAY:
            messenger.send('checkBingoState')

    def endSpecialHoliday(self, id):
        if id == ToontownGlobals.FISH_BINGO or id == ToontownGlobals.SILLY_SATURDAY:
            messenger.send('checkBingoState')