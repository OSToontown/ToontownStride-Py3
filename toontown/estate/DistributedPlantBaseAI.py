from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedLawnDecorAI import DistributedLawnDecorAI

class DistributedPlantBaseAI(DistributedLawnDecorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPlantBaseAI")

    def setTypeIndex(self, index):
        pass

    def setWaterLevel(self, water):
        pass

    def setGrowthLevel(self, growth):
        pass

    def waterPlant(self):
        pass

    def waterPlantDone(self):
        pass
