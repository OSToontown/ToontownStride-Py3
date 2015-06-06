from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedLeaderBoardAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedLeaderBoardAI")

    def __init__(self, air, name):
        DistributedObjectAI.__init__(self, air)
        self.posHpr = (0, 0, 0, 0, 0, 0)
        self.name = name
    
    def setPosHpr(self, x, y, z, h, p, r):
        self.posHpr = (x, y, z, h, p, r)

    def getPosHpr(self):
        return self.posHpr

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setDisplay(self, todo0):
        pass
    
    def subscribeTo(self, todo0):
        print 'subscribed to %s' % (todo0,)