from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedPlantBaseAI import DistributedPlantBaseAI
import GardenGlobals

class DistributedGagTreeAI(DistributedPlantBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedGagTreeAI")

    def __init__(self, air):
        DistributedPlantBaseAI.__init__(self, air)
        self.air = air
        self.wilted = 0

    def announceGenerate(self):
        DistributedPlantBaseAI.announceGenerate(self)

    def delete(self):
        DistributedPlantBaseAI.delete(self)

    def disable(self):
        DistributedPlantBaseAI.disable(self)

    def setWilted(self, wilted):
        self.wilted = wilted

    def getWilted(self):
        return self.wilted

    def requestHarvest(self, doId):
        av = simbase.air.doId2do.get(doId)
        harvested = 0
        track, level = GardenGlobals.getTreeTrackAndLevel(self.typeIndex)
        while av.inventory.addItem(track, level) > 0 and harvested < 10:
            harvested += 1
        self.sendUpdate('setMovie', [GardenGlobals.MOVIE_HARVEST, doId])
