from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedPlantBaseAI import DistributedPlantBaseAI

class DistributedFlowerAI(DistributedPlantBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedFlowerAI")

    def __init__(self, air, species, variety):
        self.air = air
        self.species = species
        self.variety = variety
        self.typeIndex = None

    def setTypeIndex(self, index):
        self.typeIndex = index

    def setVariety(self, variety):
        self.variety = variety
