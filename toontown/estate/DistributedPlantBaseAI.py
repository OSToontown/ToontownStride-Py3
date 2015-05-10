from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedLawnDecorAI import DistributedLawnDecorAI

class DistributedPlantBaseAI(DistributedLawnDecorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPlantBaseAI")

    def __init__(self, air):
        self.air = air
        self.typeIndex = 0
        self.water = 0
        self.growth = 0

    def setTypeIndex(self, index):
        self.typeIndex = index

    def setWaterLevel(self, water):
        self.water = water

    def setGrowthLevel(self, growth):
        self.growth = growth

    def waterPlant(self):
        pass

    def waterPlantDone(self):
        pass
