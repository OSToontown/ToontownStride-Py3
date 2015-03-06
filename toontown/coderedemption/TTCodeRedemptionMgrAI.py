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
            'items': [
                CatalogClothingItem.CatalogClothingItem(1821, 0)
            ],
            'month': 4,
            'day': 20
        }
    }

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)

    def getMailboxCount(items):
        count = 0

        for item in items:
            if item.getDeliveryTime() < 1:
                count += 1

        return count
                
    def redeemCode(self, context, code):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)

        if not av:
            return

        if code in self.codes:
            if av.isCodeRedeemed(code):
                self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, 3, 4])
                return

            codeInfo = self.codes[code]
            date = datetime.now()

            if ('month' in codeInfo and date.month is not codeInfo['month']) or ('day' in codeInfo and date.day is not codeInfo['day']):
                self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, 2, 0])
                return

            av.redeemCode(code)
            self.requestCodeRedeem(context, avId, av, codeInfo['items'])
        else:
            self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, 1, 0])
        
    def requestCodeRedeem(self, context, avId, av, items):
        if item in av.onOrder:
            self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, 3, 2])
            return

        if item.reachedPurchaseLimit(av):
            self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, 3, 3])
            return

        count = getMailboxCount(items)

        if len(av.onOrder) + count > 5 or len(av.mailboxContents) + len(av.onOrder) + count >= ToontownGlobals.MaxMailboxContents:
            self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, 3, 1])
            return

        for item in items:
            item.deliveryDate = int(time.time() / 60) + 0.01
            av.onOrder.append(item)

        av.b_setDeliverySchedule(av.onOrder)
        self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, 0, 0])