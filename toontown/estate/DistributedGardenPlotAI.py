from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedLawnDecorAI import DistributedLawnDecorAI
import DistributedToonStatuaryAI
import DistributedStatuaryAI

class DistributedGardenPlotAI(DistributedLawnDecorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedGardenPlotAI")

    def plantFlower(self, species, variety):
        flower = DistributedFlowerAI.DistributedFlowerAI()

    def plantGagTree(self, gagTrack, gagLevel):
        tree = DistributedGagTreeAI.DistributedGagTreeAI()

    def plantStatuary(self, species):
        statue = DistributedStatuaryAI.DistributedStatuaryAI()

    def plantToonStatuary(self, species, dnaCode):
        statue = DistributedToonStatuaryAI.DistributedToonStatuaryAI()

    def plantNothing(self, burntBeans):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do[avId]
        money = av.getMoney()
        av.setMoney(money - burntBeans)
        av.d_setMoney(money - burntBeans)
