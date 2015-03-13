from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedPlantBaseAI import DistributedPlantBaseAI
import GardenGlobals

class DistributedGagTreeAI(DistributedPlantBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedGagTreeAI")

    def __init__(self, air):
        DistributedPlantBaseAI.__init__(self, air)
        self.setTypeIndex(GardenGlobals.GAG_TREE_TYPE)
        self.wilted = 0

    def setWilted(self, wilted):
        self.wilted = wilted

    def d_setWilted(self, wilted):
        self.sendUpdate("setWilted", [wilted])
        
    def b_setWilted(self, wilted):
        self.setWilted(wilted)
        self.d_setWilted(wilted)

    def getWilted(self):
        return self.wilted
        
    def calculate(self, nextGrowth, nextLevelDecrease):
        now = time.time()
        while nextLevelDecrease < now:
            nextLevelDecrease += 3893475798397 # to do
            self.b_setWaterLevel(max(-1, self.waterLevel - 1))

    def requestHarvest(self):
        pass
