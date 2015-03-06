from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.catalog import CatalogClothingItem
from toontown.toonbase import ToontownGlobals
from datetime import datetime
import time

class TTCodeRedemptionMgrAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("TTCodeRedemptionMgrAI")
    codes = {
        'weed': {
            'item': CatalogClothingItem.CatalogClothingItem(1821, 0),
            'month': 4,
            'day': 20
        }
    }

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)

    def redeemCode(self, context, code):
        avId = self.air.getAvatarIdFromSender()

        if code in self.codes:
            codeInfo = self.codes[code]
            date = datetime.now()

            if ('month' in codeInfo and date.month is not codeInfo['month']) or ('day' in codeInfo and date.day is not codeInfo['day']):
                self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, 2, 0])
                return

            self.requestCodeRedeem(context, codeInfo['item'])
        else:
            self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, 1, 0])
        
    def requestCodeRedeem(self, context, item):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)

        if not av:
            return

        if len(av.onOrder) > 5:
            self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, 4, 4])
            return

        if len(av.mailboxContents) + len(av.onOrder) >= ToontownGlobals.MaxMailboxContents:
            self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, 4, 3])
            return

        if item in av.onOrder or item.reachedPurchaseLimit(av):
            self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, 4, 13])
            return

        item.deliveryDate = int(time.time() / 60) + 0.01
        av.onOrder.append(item)
        av.b_setDeliverySchedule(av.onOrder)
        self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, 0, 0])