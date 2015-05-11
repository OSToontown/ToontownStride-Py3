from toontown.toonbase import ToontownGlobals
import LaffRestockGlobals, DistributedNPCToonBaseAI

class DistributedNPCLaffRestockAI(DistributedNPCToonBaseAI.DistributedNPCToonBaseAI):

    def restock(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)

        if not av:
            return

        laff = av.getMaxHp() - av.getHp()

        if laff <= 0:
            self.sendUpdateToAvatarId(avId, 'restockResult', [LaffRestockGlobals.NO_LAFF, 0])
            return

        cost = laff * ToontownGlobals.CostPerLaffRestock

        if cost > av.getTotalMoney():
            self.sendUpdateToAvatarId(avId, 'restockResult', [LaffRestockGlobals.NO_MONEY, cost])
            return

        av.takeMoney(cost)
        av.b_setHp(av.getMaxHp())
        self.sendUpdateToAvatarId(avId, 'restockResult', [LaffRestockGlobals.SUCCESS, 0])
