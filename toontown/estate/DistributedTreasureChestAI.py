from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.fishing import FishGlobals
import TreasureChestGlobals

class DistributedTreasureChestAI(DistributedObjectAI):

    def completeSale(self, sell):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)

        if not av:
            return

        if sell:
            trophyResult = self.air.fishManager.creditFishTank(av)

            if trophyResult:
                self.sendUpdateToAvatarId(avId, 'completeSaleResult', [TreasureChestGlobals.TROPHY, len(av.fishCollection), FishGlobals.getTotalNumFish()])
            else:
                self.sendUpdateToAvatarId(avId, 'completeSaleResult', [TreasureChestGlobals.COMPLETE, 0, 0])
        else:
            self.sendUpdateToAvatarId(avId, 'completeSaleResult', [TreasureChestGlobals.NONE, 0, 0])
