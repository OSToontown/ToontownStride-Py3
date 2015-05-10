from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedLawnDecorAI import DistributedLawnDecorAI
import DistributedToonStatuaryAI
import DistributedStatuaryAI

class DistributedGardenPlotAI(DistributedLawnDecorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedGardenPlotAI")

    def __init__(self, air):
        self.air = air
        self.planted = None

    def plantFlower(self, species, variety):
        flower = DistributedFlowerAI.DistributedFlowerAI(self.air, species, variety)
        self.planted = flower

    def plantGagTree(self, gagTrack, gagLevel):
        tree = DistributedGagTreeAI.DistributedGagTreeAI(self.air, gagTrack, gagLevel)
        self.planted = tree

    def plantStatuary(self, species):
        statue = DistributedStatuaryAI.DistributedStatuaryAI(self.air, species)
        self.planted = statue

    def plantToonStatuary(self, species, dnaCode):
        statue = DistributedToonStatuaryAI.DistributedToonStatuaryAI(self.air, species, dnaCode)
        self.planted = statue

    def plantNothing(self, burntBeans):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do[avId]
        money = av.getMoney()
        av.setMoney(money - burntBeans)
        av.d_setMoney(money - burntBeans)
