from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedStatuaryAI import DistributedStatuaryAI

class DistributedChangingStatuaryAI(DistributedStatuaryAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedChangingStatuaryAI")

    def __init__(self, air):
        DistributedStatuaryAI.__init__(self, air)
        self.air = air
        self.growthLevel = -1

    def setGrowthLevel(self, growthLevel):
        self.growthLevel = growthLevel

    def getGrowthLevel(self):
        return self.growthLevel
