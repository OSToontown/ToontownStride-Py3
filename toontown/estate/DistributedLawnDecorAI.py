from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedNodeAI import DistributedNodeAI

class DistributedLawnDecorAI(DistributedNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedLawnDecorAI")

    def __init__(self, air):
        self.air = air
        self.plot = None
        self.heading = 0
        self.pos = (0, 0, 0)
        self.ownerIndex = 0

    def setPlot(self, plot):
        self.plot = plot

    def setHeading(self, h):
        self.heading = h
        self.sendUpdate('setH', [h])

    def setPosition(self, x, y, z):
        self.pos = (x, y, z)
        self.sendUpdate('setPos', [x, y, z])

    def setOwnerIndex(self, index):
        self.ownerIndex = index

    def plotEntered(self):
        pass

    def removeItem(self):
        pass

    def setMovie(self, todo0, todo1):
        pass

    def movieDone(self):
        pass

    def interactionDenied(self, todo0):
        pass
