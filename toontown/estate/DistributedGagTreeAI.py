from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedPlantBaseAI import DistributedPlantBaseAI

class DistributedGagTreeAI(DistributedPlantBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedGagTreeAI")

    def __init__(self, air, gagTrack, gagLevel):
        self.air = air
        self.track = gagTrack
        self.level = level
        self.wilted = 0

    def setWilted(self, wilted):
        self.wilted = wilted

    def requestHarvest(self):
        pass
