from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from direct.distributed.DistributedObjectAI import DistributedObjectAI
import random

class DistributedLeaderBoardAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedLeaderBoardAI")

    def __init__(self, air, displays):
        DistributedObjectAI.__init__(self, air)
        self.displays = displays
        self.display = (0, 0, [])
        self.posHpr = (0, 0, 0, 0, 0, 0)
    
    def generateWithRequired(self, zoneId):
        DistributedObjectAI.generateWithRequired(self, zoneId)
        self.setup()
    
    def delete(self):
        DistributedObjectAI.delete(self)
        taskMgr.remove(self.switchTask)
    
    def setup(self):
        self.currentId = 0
        self.switchDisplay()
        self.switchTask = taskMgr.doMethodLater(15, self.switchDisplay, 'leaderboardSwitchTask-%s' % random.random())
    
    def switchDisplay(self, task=None):
        race = self.displays[self.currentId]
        
        self.display = (race[0], race[1], [])
        self.currentId += 1
        
        if self.currentId >= len(self.displays):
            self.currentId = 0

        self.sendUpdate('setDisplay', [self.display[0], self.display[1], self.display[2]])
        return Task.again
    
    def setPosHpr(self, x, y, z, h, p, r):
        self.posHpr = (x, y, z, h, p, r)

    def getPosHpr(self):
        return self.posHpr
    
    def getDisplay(self):
        return self.display