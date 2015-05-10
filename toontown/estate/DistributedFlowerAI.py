from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedPlantBaseAI import DistributedPlantBaseAI

class DistributedFlowerAI(DistributedPlantBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedFlowerAI")

    def setTypeIndex(self, index):
        pass

    def setVariety(self, variety):
        pass
