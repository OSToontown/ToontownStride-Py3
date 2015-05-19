from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedLawnDecorAI import DistributedLawnDecorAI

class DistributedStatuaryAI(DistributedLawnDecorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedStatuaryAI")

    def __init__(self, air, species):
        self.air = air
        self.species = species
        self.typeIndex = 0
        self.water = 0
        self.growth = 0

    def setTypeIndex(self, index):
        self.typeIndex = index

    def setWaterLevel(self, water):
        self.water = water

    def setGrowthLevel(self, growth):
        self.growth = growth
