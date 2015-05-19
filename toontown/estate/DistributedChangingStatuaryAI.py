from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedStatuaryAI import DistributedStatuaryAI

class DistributedChangingStatuaryAI(DistributedStatuaryAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedChangingStatuaryAI")

    def __init__(self, air, species):
        self.air = air
        self.species = species

    def setGrowthLevel(self, growth):
        self.growth = growth
