from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedLawnDecorAI import DistributedLawnDecorAI

class DistributedStatuaryAI(DistributedLawnDecorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedStatuaryAI")

    def setTypeIndex(self, index):
        pass

    def setWaterLevel(self, water):
        pass

    def setGrowthLevel(self, growth):
        pass
