from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedPlantBaseAI import DistributedPlantBaseAI

class DistributedGagTreeAI(DistributedPlantBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedGagTreeAI")

    def setWilted(self, wilted):
        pass

    def requestHarvest(self):
        pass
