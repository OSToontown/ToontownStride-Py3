from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedLawnDecorAI import DistributedLawnDecorAI
from DistributedToonStatuaryAI import DistributedToonStatuaryAI
from DistributedStatuaryAI import DistributedStatuaryAI
from DistributedGagTreeAI import DistributedGagTreeAI
from DistributedFlowerAI import DistributedFlowerAI
import GardenGlobals
import datetime

slots2plots = {
    0: GardenGlobals.plots0,
    1: GardenGlobals.plots1,
    2: GardenGlobals.plots2,
    3: GardenGlobals.plots3,
    4: GardenGlobals.plots4,
    5: GardenGlobals.plots5
}

class DistributedGardenPlotAI(DistributedLawnDecorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedGardenPlotAI")

    def __init__(self, air):
        DistributedLawnDecorAI.__init__(self, air)
        self.air = air
        self.planted = None

    def announceGenerate(self):
        DistributedLawnDecorAI.announceGenerate(self)

    def delete(self):
        DistributedLawnDecorAI.delete(self)

    def disable(self):
        DistributedLawnDecorAI.disable(self)

    def finishPlanting(self, avId):
        self.planted.generateWithRequired(self.zoneId)
        self.addData()
        self.sendUpdate('plantedItem', [self.planted.doId])
        self.planted.sendUpdate('setMovie', [GardenGlobals.MOVIE_FINISHPLANTING, avId])

    def finishRemoving(self, avId):
        self.removeData()
        self.planted.removeNode()
        self.planted.delete()
        simbase.air.removeObject(self.planted.doId)
        self.planted = None
        self.sendUpdate('setMovie', [GardenGlobals.MOVIE_FINISHREMOVING, avId])

    def addData(self):
        estate = simbase.air.doId2do.get(self.getEstate())
        plantedAt = int(datetime.datetime.now().strftime('%Y%m%d%H%M')) # TODO: Possibly store this in mongodb/cPickle instead.
        if isinstance(self.planted, DistributedFlowerAI):
            data = [
                self.getPlot(),
                GardenGlobals.FLOWER_TYPE,
                self.planted.getTypeIndex(),
                self.planted.getVariety(),
                self.planted.getWaterLevel(),
                self.planted.getGrowthLevel(),
                0,
                plantedAt,
                plantedAt
            ]
        elif isinstance(self.planted, DistributedGagTreeAI):
            data = [
                self.getPlot(),
                GardenGlobals.GAG_TREE_TYPE,
                self.planted.getTypeIndex(),
                0,
                self.planted.getWaterLevel(),
                self.planted.getGrowthLevel(),
                0,
                plantedAt,
                plantedAt
            ]
        elif isinstance(self.planted, DistributedToonStatuaryAI):
            data = [
                self.getPlot(),
                GardenGlobals.TOON_STATUARY_TYPE,
                self.planted.getTypeIndex(),
                0,
                self.planted.getWaterLevel(),
                self.planted.getGrowthLevel(),
                self.planted.getOptional(),
                plantedAt,
                plantedAt
            ]
        elif isinstance(self.planted, DistributedStatuaryAI):
            data = [
                self.getPlot(),
                GardenGlobals.STATUARY_TYPE,
                self.planted.getTypeIndex(),
                0,
                self.planted.getWaterLevel(),
                self.planted.getGrowthLevel(),
                0,
                plantedAt,
                plantedAt
            ]
        else:
            return
        estate.items[self.getOwnerIndex()].append(tuple(data))
        estate.updateItems()

    def removeData(self):
        estate = simbase.air.doId2do.get(self.getEstate())
        dataIndex = -1
        for n, item in enumerate(estate.items[self.getOwnerIndex()]):
            if item[0] == self.getPlot():
                dataIndex = n
        if dataIndex >= 0:
            del estate.items[self.getOwnerIndex()][dataIndex]
            estate.updateItems()

    def plantFlower(self, species, variety, toon):
        #free for now
        #av = simbase.air.doId2do.get(toon)
        #av.takeMoney(GardenGlobals.getNumBeansRequired(species, variety))
        self.planted = DistributedFlowerAI(self.air)
        self.planted.setEstate(self.getEstate())
        self.planted.setOwnerPlot(self.doId)
        self.planted.setPlot(self.getPlot())
        self.planted.setHeading(self.getHeading())
        self.planted.setPosition(*self.getPosition())
        self.planted.setOwnerIndex(self.getOwnerIndex())
        self.planted.setWaterLevel(0)
        self.planted.setGrowthLevel(0)
        self.planted.setTypeIndex(species)
        self.planted.setVariety(variety)
        self.sendUpdate('setMovie', [GardenGlobals.MOVIE_PLANT, toon])

    def plantGagTree(self, track, level, toon):
        #free for now
        #av = simbase.air.doId2do.get(toon)
        #av.inventory.useItem(track, level)
        #av.d_setInventory(av.inventory.makeNetString())
        self.planted = DistributedGagTreeAI(self.air)
        self.planted.setEstate(self.getEstate())
        self.planted.setOwnerPlot(self.doId)
        self.planted.setPlot(self.getPlot())
        self.planted.setHeading(self.getHeading())
        self.planted.setPosition(*self.getPosition())
        self.planted.setOwnerIndex(self.getOwnerIndex())
        self.planted.setTypeIndex(GardenGlobals.getTreeTypeIndex(track, level))
        self.planted.setWaterLevel(0)
        self.planted.setGrowthLevel(0)
        self.sendUpdate('setMovie', [GardenGlobals.MOVIE_PLANT, toon])

    def plantStatuary(self, species, toon):
        #free for now
        #av = simbase.air.doId2do.get(toon)
        #av.takeMoney(GardenGlobals.getNumBeansRequired(species, 0))
        self.planted = DistributedStatuaryAI(self.air)
        self.planted.setEstate(self.getEstate())
        self.planted.setOwnerPlot(self.doId)
        self.planted.setPlot(self.getPlot())
        self.planted.setHeading(self.getHeading())
        self.planted.setPosition(*self.getPosition())
        self.planted.setOwnerIndex(self.getOwnerIndex())
        self.planted.setTypeIndex(species)
        self.planted.setWaterLevel(0)
        self.planted.setGrowthLevel(0)
        self.sendUpdate('setMovie', [GardenGlobals.MOVIE_PLANT, toon])

    def plantToonStatuary(self, species, dnaCode, toon):
        #free for now
        #av = simbase.air.doId2do.get(toon)
        #av.takeMoney(GardenGlobals.getNumBeansRequired(species, 0))
        self.planted = DistributedToonStatuaryAI(self.air)
        self.planted.setEstate(self.getEstate())
        self.planted.setOwnerPlot(self.doId)
        self.planted.setPlot(self.getPlot())
        self.planted.setHeading(self.getHeading())
        self.planted.setPosition(*self.getPosition())
        self.planted.setOwnerIndex(self.getOwnerIndex())
        self.planted.setTypeIndex(species)
        self.planted.setWaterLevel(0)
        self.planted.setGrowthLevel(0)
        self.planted.setOptional(dnaCode)
        self.sendUpdate('setMovie', [GardenGlobals.MOVIE_PLANT, toon])

    def plantNothing(self, burntBeans, toon):
        # TODO: Fix exploit.
        av = simbase.air.doId2do.get(toon)
        av.takeMoney(burntBeans)
        self.planted = None
