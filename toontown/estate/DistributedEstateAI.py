from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.PyDatagramIterator import *
from direct.distributed.PyDatagram import *
from toontown.toonbase import ToontownGlobals
import HouseGlobals
import time
import random
from toontown.fishing.DistributedFishingPondAI import DistributedFishingPondAI
from toontown.fishing.DistributedFishingTargetAI import DistributedFishingTargetAI
from toontown.fishing.DistributedPondBingoManagerAI import DistributedPondBingoManagerAI
from toontown.fishing import FishingTargetGlobals
from toontown.safezone.DistributedFishingSpotAI import DistributedFishingSpotAI
from toontown.safezone.SZTreasurePlannerAI import SZTreasurePlannerAI
from toontown.safezone import TreasureGlobals
from DistributedGardenBoxAI import *
from DistributedGagTreeAI import *
from DistributedFlowerAI import *
import GardenGlobals
from DistributedCannonAI import *
from DistributedTargetAI import *
import CannonGlobals

NULL_PLANT = [0, -1, 0, -1, 0]
NULL_TREES = [NULL_PLANT] * 8
NULL_FLOWERS = [NULL_PLANT] * 10
NULL_STATUARY = 0

def unpackGardenSetter(f):
    def w(klass, data):
        if data:
            dg = PyDatagram(data)
            dgi = PyDatagramIterator(dg)
            def unpackPlant(_):
                return dgi.getUint32, dgi.getInt8(), dgi.getUint32(), dgi.getInt8(), dgi.getUint16()
            flowers = map(unpackPlant, range(10))
            trees = map(unpackPlant, range(8))
            st = dgi.getUint8()
            started = dgi.getBool()
        else:
            flowers = NULL_FLOWERS
            trees = NULL_TREES
            st = NULL_STATUARY
            started = 0
        return f(klass, started, flowers, trees, st)
    return w
    
def packGardenData(plants, statuary, started = True):
    dg = PyDatagram()
    for plant in plants:
        a, b, c, d, e = plant
        dg.addUint32(a)
        dg.addInt8(b)
        dg.addUint32(c)
        dg.addInt8(d)
        dg.addUint16(e)

    dg.addUint8(statuary)
    dg.addBool(started)
    return dg.getMessage()

class Garden:
    def __init__(self, avId):
        self.avId = avId
        self.treesData = NULL_TREES
        self.flowersData = NULL_FLOWERS
        self.statuaryIndex = NULL_STATUARY
        self.trees = []
        self.flowers = []
        self.statuary = None
        self.objects = []
        
    def destroy(self):
        del self.treesData
        del self.flowersData
        del self.statuaryIndex
        for tree in self.trees:
            tree.requestDelete()
        for flower in self.flowers:
            flower.requestDelete()
        for object in self.objects:
            object.requestDelete()
        if self.statuary:
            self.statuary.requestDelete()
        del self.trees
        del self.flowers
        del self.objects
        del self.statuary
        
    def create(self, estateMgr):
        if self.avId not in estateMgr.toons:
            estateMgr.notify.warning("Garden associated to unknown avatar %d, deleting..." % self.avId)
            print estateMgr.toons
            return False
        houseIndex = estateMgr.toons.index(self.avId)

        boxDefs = GardenGlobals.estateBoxes[houseIndex]
        for x, y, h, boxType in boxDefs:
            box = DistributedGardenBoxAI(estateMgr.air)
            box.setTypeIndex(boxType)
            box.setPos(x, y, 0)
            box.setH(h)
            box.setOwnerIndex(houseIndex)
            box.generate()#WithRequired(estateMgr.zoneId)
            self.objects.append(box)
                
        plots = GardenGlobals.estatePlots[houseIndex]
        treeIndex = 0
        for x, y, h, type in plots:
            if type == GardenGlobals.GAG_TREE_TYPE:
                planted, waterLevel, nextLevelDecrease, growthLevel, nextGrowth = self.treesData[treeIndex]
                if planted:
                    treeIndex += 1
                    tree = DistributedGagTreeAI(estateMgr.air)
                    tree.setPos(x, y, 0)
                    tree.setH(h)
                    tree.setOwnerIndex(houseIndex)
                    tree.setWaterLevel(waterLevel)
                    tree.setGrowthLevel(growthLevel)
                    tree.calculate(nextGrowth, nextLevelDecrease)
                    tree.generate()#WithRequired(estateMgr.zoneId)
                    self.trees.append(tree)

class GardenManager:
    def __init__(self, mgr):
        self.mgr = mgr
        self.gardens = {}
                    
    def handleSingleGarden(self, avId, data):
        g = Garden(avId)
        g.flowersData, g.treesData, g.statuaryIndex = data
        if not g.create(self.mgr):
            return
        self.gardens[avId] = g
        
    def placeGarden(self, avId):
        g = Garden(avId)
        g.create(self.mgr)
        self.gardens[avId] = g
        
    def destroy(self):
        for garden in self.gardens.values():
            garden.destroy()
        del self.gardens
            
    def getData(self, avId):
        g = self.gardens.get(avId)
        if not g:
            return packGardenData(NULL_FLOWERS + NULL_TREES, NULL_STATUARY, False)
        return packGardenData(g.flowersData + g.treesData, g.statuaryIndex)

class Rental:
    def __init__(self, estate):
        self.estate = estate
        self.objects = set()
        
    def destroy(self):
        del self.estate
        for object in self.objects:
            if not object.isDeleted():
                object.requestDelete()
                taskMgr.remove(object.uniqueName('delete'))
        self.objects = set()
        
class CannonRental(Rental):
    def generateObjects(self):
        target = DistributedTargetAI(self.estate.air)
        target.generateWithRequired(self.estate.zoneId)
        
        for drop in CannonGlobals.cannonDrops:
            cannon = DistributedCannonAI(self.estate.air)
            cannon.setEstateId(self.estate.doId)
            cannon.setTargetId(target.doId)
            cannon.setPosHpr(*drop)
            cannon.generateWithRequired(self.estate.zoneId)
            self.objects.add(cannon)
            
        self.generateTreasures()
        self.estate.b_setClouds(1)
        
    def destroy(self):
        self.estate.b_setClouds(0)
        Rental.destroy(self)
            
    def generateTreasures(self):
        doIds = []
        z = 35
        
        for i in xrange(20):
            x = random.randint(100, 300) - 200
            y = random.randint(100, 300) - 200
            treasure = DistributedTreasureAI.DistributedTreasureAI(self.estate.air, self, 9, x, y, z)
            treasure.generateWithRequired(self.estate.zoneId)
            self.objects.add(treasure)
            doIds.append(treasure.doId)
            
        self.estate.sendUpdate("setTreasureIds", [doIds])
        
    def grabAttempt(self, avId, treasureId):
        av = self.estate.air.doId2do.get(avId)
        if av == None:
            self.estate.air.writeServerEvent('suspicious', avId, 'TreasurePlannerAI.grabAttempt unknown avatar')
            self.estate.notify.warning('avid: %s does not exist' % avId)
            return
            
        treasure = self.estate.air.doId2do.get(treasureId)
        if self.validAvatar(av):
            treasure.d_setGrab(avId)
            self.deleteTreasureSoon(treasure)
            
        else:
            treasure.d_setReject()

    def deleteTreasureSoon(self, treasure):
        taskName = treasure.uniqueName('delete')
        taskMgr.doMethodLater(5, self.__deleteTreasureNow, taskName, extraArgs=(treasure, taskName))

    def __deleteTreasureNow(self, treasure, taskName):
        treasure.requestDelete()
        
    def validAvatar(self, av):
        if av.getMaxHp() == av.getHp():
            return 0
            
        av.toonUp(3)
        return 1
    
class DistributedEstateAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedEstateAI")
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.toons = [0, 0, 0, 0, 0, 0]
        self.items = [[], [], [], [], [], []]
        self.decorData = []
        self.estateType = 0 # NOT SURE IF THIS HAS ANY USE BUT THANKS DISNEY
        self.cloudType = 0
        self.dawnTime = 0
        self.lastEpochTimestamp = 0
        self.rentalTimestamp = 0
        self.houses = [None, None, None, None, None, None]
        self.rentalType = 0
        self.rentalHandle = None
        self.pond = None
        self.spots = []
        self.targets = []
        self.doId2do = {}
        self.owner = None
        self.gardenManager = GardenManager(self)
        self.__pendingGardens = {}
        
    def generate(self):
        DistributedObjectAI.generate(self)
        
        self.pond = DistributedFishingPondAI(simbase.air)
        self.pond.setArea(ToontownGlobals.MyEstate)
        self.pond.generateWithRequired(self.zoneId)
            
        for i in xrange(FishingTargetGlobals.getNumTargets(ToontownGlobals.MyEstate)):
            target = DistributedFishingTargetAI(self.air)
            target.setPondDoId(self.pond.getDoId())
            target.generateWithRequired(self.zoneId)
            self.targets.append(target)

        spot = DistributedFishingSpotAI(self.air)
        spot.setPondDoId(self.pond.getDoId())
        spot.setPosHpr(49.1029, -124.805, 0.344704, 90, 0, 0)
        spot.generateWithRequired(self.zoneId)
        self.spots.append(spot)

        spot = DistributedFishingSpotAI(self.air)
        spot.setPondDoId(self.pond.getDoId())
        spot.setPosHpr(46.5222, -134.739, 0.390713, 75, 0, 0)
        spot.generateWithRequired(self.zoneId)
        self.spots.append(spot)

        spot = DistributedFishingSpotAI(self.air)
        spot.setPondDoId(self.pond.getDoId())
        spot.setPosHpr(41.31, -144.559, 0.375978, 45, 0, 0)
        spot.generateWithRequired(self.zoneId)
        self.spots.append(spot)

        spot = DistributedFishingSpotAI(self.air)
        spot.setPondDoId(self.pond.getDoId())
        spot.setPosHpr(46.8254, -113.682, 0.46015, 135, 0, 0)
        spot.generateWithRequired(self.zoneId)
        self.spots.append(spot)

        self.createTreasurePlanner()

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)
        # Commented out because I had to reach estate to debug doors (Nacib)
        #for index, garden in self.__pendingGardens.items():
        #    started = garden[0]
        #    self.gardenManager.handleSingleGarden(self.toons[index], garden[1:])
        #    self.placeStarterGarden(self.toons[index])
        self.__pendingGardens = {}

    def destroy(self):
        for house in self.houses:
            if house:
                house.requestDelete()
        self.houses = []
        if self.pond:
            for spot in self.spots:
                spot.requestDelete()
            self.spots = []
            for target in self.targets:
                target.requestDelete()
            self.targets = []
            self.pond.requestDelete()
            self.pond = None
        self.gardenManager.destroy()
        if self.rentalHandle:
            self.rentalHandle.destroy()
            self.rentalHandle = None
        if self.treasurePlanner:
            self.treasurePlanner.stop()
        self.requestDelete()

    def addDistObj(self, distObj):
        self.doId2do[distObj.doId] = distObj

    def setClientReady(self):
        self.sendUpdate('setEstateReady', [])

    def setEstateType(self, type):
        self.estateType = type
        
    def d_setEstateType(self, type):
        self.sendUpdate('setEstateType', [type])
        
    def b_setEstateType(self, type):
        self.setEstateType(type)
        self.d_setEstateType(type)

    def getEstateType(self):
        return self.estateType

    def setClosestHouse(self, todo0):
        pass

    def setTreasureIds(self, todo0):
        pass
        
    def createTreasurePlanner(self):
        treasureType, healAmount, spawnPoints, spawnRate, maxTreasures = TreasureGlobals.SafeZoneTreasureSpawns[ToontownGlobals.MyEstate]
        self.treasurePlanner = SZTreasurePlannerAI(self.zoneId, treasureType, healAmount, spawnPoints, spawnRate, maxTreasures)
        self.treasurePlanner.start()

    def requestServerTime(self):
        avId = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(avId, 'setServerTime', [time.time() % HouseGlobals.DAY_NIGHT_PERIOD])

    def setServerTime(self, todo0):
        pass

    def setDawnTime(self, dawnTime):
        self.dawnTime = dawnTime
        
    def d_setDawnTime(self, dawnTime):
        self.sendUpdate('setDawnTime', [dawnTime])
        
    def b_setDawnTime(self, dawnTime):
        self.setDawnTime(dawnTime)
        self.d_setDawnTime(dawnTime)
        
    def getDawnTime(self):
        return self.dawnTime

    def setDecorData(self, decorData):
        self.decorData = decorData
        
    def d_setDecorData(self, decorData):
        self.sendUpdate('setDecorData', [decorData])
        
    def b_setDecorData(self, decorData):
        self.setDecorData(decorData)
        self.d_setDecorData(decorData)
        
    def getDecorData(self):
        return self.decorData

    def setLastEpochTimeStamp(self, last):
        self.lastEpochTimestamp = last
        
    def d_setLastEpochTimeStamp(self, last):
        self.sendUpdate('setLastEpochTimeStamp', [last])
        
    def b_setLastEpochTimeStamp(self, last):
        self.setLastEpochTimeStamp(last)
        self.d_setLastEpochTimeStamp(last)
        
    def getLastEpochTimeStamp(self):
        return self.lastEpochTimestamp

    def setRentalTimeStamp(self, rental):
        self.rentalTimestamp = rental
        
    def d_setRentalTimeStamp(self, rental):
        self.sendUpdate('setRentalTimeStamp', [rental])
        
    def b_setRentalTimeStamp(self, rental):
        self.setRentalTimeStamp(rental)
        self.d_setRentalTimeStamp(rental)
        
    def getRentalTimeStamp(self):
        return self.rentalTimestamp

    def b_setRentalType(self, type):
        self.d_setRentalType(type)
        self.setRentalType(type)
        
    def d_setRentalType(self, type):
        self.sendUpdate("setRentalType", [type])
        
    def setRentalType(self, type):
        expirestamp = self.getRentalTimeStamp()
        if expirestamp == 0:
            expire = 0
            
        else:
            expire = int(expirestamp - time.time())
            
        if expire < 0:
            self.rentalType = 0
            self.d_setRentalType(0)
            self.b_setRentalTimeStamp(0)
        
        else:
            if self.rentalType == type:
                return
                
            self.rentalType = type
            if self.rentalHandle:
                self.rentalHandle.destroy()
                self.rentalHandle = None
                
            if self.rentalType == ToontownGlobals.RentalCannon:
                self.rentalHandle = CannonRental(self)
                
            else:
                self.notify.warning('Unknown rental %s' % self.rentalType)
                return
                
            self.rentalHandle.generateObjects()
        
    def getRentalType(self):
        return self.rentalType
        
    def rentItem(self, rentType, duration):
        self.rentalType = rentType
        self.b_setRentalTimeStamp(time.time() + duration * 60)
        self.b_setRentalType(rentType)
    
    def setSlot0ToonId(self, id):
        self.toons[0] = id
        
    def d_setSlot0ToonId(self, id):
        self.sendUpdate('setSlot0ToonId', [id])
        
    def b_setSlot0ToonId(self, id):
        self.setSlot0ToonId(id)
        self.d_setSlot0ToonId(id)
        
    def getSlot0ToonId(self):
        return self.toons[0]

    def setSlot0Items(self, items):
        self.items[0] = items

    def d_setSlot0Items(self, items):
        self.sendUpdate('setSlot5Items', [items])
        
    def b_setSlot0Items(self, items):
        self.setSlot0Items(items)
        self.d_setSlot0Items(items)
        
    def getSlot0Items(self):
        return self.items[0]
        
    def setSlot1ToonId(self, id):
        self.toons[1] = id

    def d_setSlot1ToonId(self, id):
        self.sendUpdate('setSlot1ToonId', [id])
        
    def b_setSlot1ToonId(self, id):
        self.setSlot1ToonId(id)
        self.d_setSlot1ToonId(id)
        
    def getSlot1ToonId(self):
        return self.toons[1]
        
    def setSlot1Items(self, items):
        self.items[1] = items
        
    def d_setSlot1Items(self, items):
        self.sendUpdate('setSlot2Items', [items])
        
    def b_setSlot1Items(self, items):
        self.setSlot2Items(items)
        self.d_setSlot2Items(items)
        
    def getSlot1Items(self):
        return self.items[1]

    def setSlot2ToonId(self, id):
        self.toons[2] = id

    def d_setSlot2ToonId(self, id):
        self.sendUpdate('setSlot2ToonId', [id])
        
    def b_setSlot2ToonId(self, id):
        self.setSlot2ToonId(id)
        self.d_setSlot2ToonId(id)
        
    def getSlot2ToonId(self):
        return self.toons[2]

    def setSlot2Items(self, items):
        self.items[2] = items

    def d_setSlot2Items(self, items):
        self.sendUpdate('setSlot2Items', [items])
        
    def b_setSlot2Items(self, items):
        self.setSlot2Items(items)
        self.d_setSlot2Items(items)
        
    def getSlot2Items(self):
        return self.items[2]

    def setSlot3ToonId(self, id):
        self.toons[3] = id
        
    def d_setSlot3ToonId(self, id):
        self.sendUpdate('setSlot3ToonId', [id])
        
    def b_setSlot3ToonId(self, id):
        self.setSlot3ToonId(id)
        self.d_setSlot3ToonId(id)
        
    def getSlot3ToonId(self):
        return self.toons[3]

    def setSlot3Items(self, items):
        self.items[3] = items
        
    def d_setSlot3Items(self, items):
        self.sendUpdate('setSlot3Items', [items])
        
    def b_setSlot3Items(self, items):
        self.setSlot3Items(items)
        self.d_setSlot3Items(items)
        
    def getSlot3Items(self):
        return self.items[3]

    def setSlot4ToonId(self, id):
        self.toons[4] = id
        
    def d_setSlot4ToonId(self, id):
        self.sendUpdate('setSlot4ToonId', [id])
        
    def b_setSlot5ToonId(self, id):
        self.setSlot4ToonId(id)
        self.d_setSlot4ToonId(id)
        
    def getSlot4ToonId(self):
        return self.toons[4]

    def setSlot4Items(self, items):
        self.items[4] = items
        
    def d_setSlot4Items(self, items):
        self.sendUpdate('setSlot4Items', [items])
        
    def b_setSlot4Items(self, items):
        self.setSlot4Items(items)
        self.d_setSlot4Items(items)
        
    def getSlot4Items(self):
        return self.items[4]

    def setSlot5ToonId(self, id):
        self.toons[5] = id
        
    def d_setSlot5ToonId(self, id):
        self.sendUpdate('setSlot5ToonId', [id])
        
    def b_setSlot5ToonId(self, id):
        self.setSlot5ToonId(id)
        self.d_setSlot5ToonId(id)
        
    def getSlot5ToonId(self):
        return self.toons[5]

    def setSlot5Items(self, items):
        self.items[5] = items
        
    def d_setSlot5Items(self, items):
        self.sendUpdate('setSlot5Items', [items])
        
    def b_setSlot5Items(self, items):
        self.setSlot5Items(items)
        self.d_setSlot5Items(items)
        
    def getSlot5Items(self):
        return self.items[5]

    def setIdList(self, idList):
        for i in xrange(len(idList)):
            if i >= 6:
                return
            self.toons[i] = idList[i]
        
    def d_setIdList(self, idList):
        self.sendUpdate('setIdList', [idList])
    
    def b_setIdList(self, idList):
        self.setIdList(idList)
        self.d_setIdLst(idList)
        
    def completeFlowerSale(self, todo0):
        pass

    def awardedTrophy(self, todo0):
        pass

    def setClouds(self, clouds):
        self.cloudType = clouds
        
    def d_setClouds(self, clouds):
        self.sendUpdate('setClouds', [clouds])
        
    def b_setClouds(self, clouds):
        self.setClouds(clouds)
        self.d_setClouds(clouds)
        
    def getClouds(self):
        return self.cloudType

    def cannonsOver(self):
        pass

    def gameTableOver(self):
        pass

    def updateToons(self):
        self.d_setSlot0ToonId(self.toons[0])
        self.d_setSlot1ToonId(self.toons[1])
        self.d_setSlot2ToonId(self.toons[2])
        self.d_setSlot3ToonId(self.toons[3])
        self.d_setSlot4ToonId(self.toons[4])
        self.d_setSlot5ToonId(self.toons[5])
        self.sendUpdate('setIdList', [self.toons])

    def updateItems(self):
        self.d_setSlot0Items(self.items[0])
        self.d_setSlot1Items(self.items[1])
        self.d_setSlot2Items(self.items[2])
        self.d_setSlot3Items(self.items[3])
        self.d_setSlot4Items(self.items[4])
        self.d_setSlot5Items(self.items[5])

    @unpackGardenSetter
    def setSlot0Garden(self, started, flowers, trees, si):
        self.__pendingGardens[0] = (started, flowers, trees, si)
     
    @unpackGardenSetter
    def setSlot1Garden(self, started, flowers, trees, si):
        self.__pendingGardens[1] = (started, flowers, trees, si)
    
    @unpackGardenSetter
    def setSlot2Garden(self, started, flowers, trees, si):
        self.__pendingGardens[2] = (started, flowers, trees, si)
    
    @unpackGardenSetter    
    def setSlot3Garden(self, started, flowers, trees, si):
        self.__pendingGardens[3] = (started, flowers, trees, si)
     
    @unpackGardenSetter     
    def setSlot4Garden(self, started, flowers, trees, si):
        self.__pendingGardens[4] = (started, flowers, trees, si)
     
    @unpackGardenSetter
    def setSlot5Garden(self, started, flowers, trees, si):
        self.__pendingGardens[5] = (started, flowers, trees, si)

    def d_updateGarden(self, slot = None):
        self.notify.info('updateGarden %s' % slot)
        if slot is None:
            for i in xrange(6):
                self.d_updateGarden(i)
        else:
            data = self.gardenManager.getData(self.toons[slot])
            self.sendUpdate('setSlot%dGarden' % slot, [data])

    def placeStarterGarden(self, avId):
        av = self.air.doId2do.get(avId)
        if not av:
            return
        self.notify.info('placeStarterGarden %d' % avId)
        self.gardenManager.placeGarden(avId)
        self.d_updateGarden()
