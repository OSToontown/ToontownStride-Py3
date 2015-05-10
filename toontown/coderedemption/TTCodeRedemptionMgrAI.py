from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.catalog import CatalogAccessoryItem
from toontown.catalog import CatalogClothingItem
from toontown.catalog import CatalogNametagItem
from toontown.catalog import CatalogChatItem
from toontown.catalog import CatalogEmoteItem
from toontown.catalog import CatalogGardenItem
from toontown.catalog import CatalogGardenStarterItem
from toontown.catalog import CatalogMouldingItem
from toontown.catalog import CatalogRentalItem
from toontown.catalog import CatalogFurnitureItem
from toontown.catalog import CatalogAnimatedFurnitureItem
from toontown.catalog import CatalogFlooringItem
from toontown.catalog import CatalogPetTrickItem
from toontown.catalog import CatalogWainscotingItem
from toontown.catalog import CatalogToonStatueItem
from toontown.catalog import CatalogWallpaperItem
from toontown.catalog import CatalogWindowItem
from toontown.toonbase import ToontownGlobals
from datetime import datetime, timedelta
import time

"""
Code example:

'codeName': {
    'items': [
        CatalogTypeItem.CatalogTypeItem(arguments)
    ],
    'expirationDate': datetime(2020, 1, 30),
    'month': 1,
    'day': 30,
    'year': 2000'
}

Expiration date, month, day and year are optional fields.

If you for some reason are not familiar with arrays or lists, you
only include the comma if there are multiple arguments.
"""

class TTCodeRedemptionMgrAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("TTCodeRedemptionMgrAI")
    codes = {
        'weed': {
            'items': [
                CatalogClothingItem.CatalogClothingItem(1821, 0)
            ],
            'month': 4,
            'day': 20
        },
        'gardening': {
            'items': [
                CatalogGardenStarterItem.CatalogGardenStarterItem()
            ]
        },
        'sillymeter': {
            'items': [
                CatalogClothingItem.CatalogClothingItem(1753, 0)
            ]
        }
    }

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)

    def getMailboxCount(self, items):
        count = 0

        for item in items:
            if item.getDeliveryTime() > 0:
                count += 1

        return count

    def redeemCode(self, code):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)

        if not av:
            return

        code = code.lower()

        if code in self.codes:
            if av.isCodeRedeemed(code):
                self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [4])
                print ('%s tried to redeem already redeemed code %s' % (avId, code))
                return

            codeInfo = self.codes[code]
            date = datetime.now()

            if ('year' in codeInfo and date.year is not codeInfo['year']) and date.year > codeInfo['year'] or ('expirationDate' in codeInfo and codeInfo['expirationDate'] - date < timedelta(hours = 1)):
                self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [2])
                print ('%s attempted to redeem code %s but it was expired!' % (avId, code))
                return
            elif ('year' in codeInfo and date.year is not codeInfo['year']) and date.year < codeInfo['year'] or ('month' in codeInfo and date.month is not codeInfo['month']) or ('day' in codeInfo and date.day is not codeInfo['day']):
                self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [5])
                print ("%s attempted to redeem code %s but it wasn't usable yet!" % (avId, code))
                return
            
            av.redeemCode(code)
            self.requestCodeRedeem(avId, av, codeInfo['items'])
            print ('%s successfully redeemed %s' % (avId, code))
        else:
            self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [1])
            print ('%s tried to redeem non-existant code %s' % (avId, code))
            

    def requestCodeRedeem(self, avId, av, items):
        count = self.getMailboxCount(items)

        if len(av.onOrder) + count > 5 or len(av.mailboxContents) + len(av.onOrder) + count >= ToontownGlobals.MaxMailboxContents:
            self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [3])
            return

        for item in items:
            if item in av.onOrder:
                continue

            item.deliveryDate = int(time.time() / 60) + 0.01
            av.onOrder.append(item)

        av.b_setDeliverySchedule(av.onOrder)
        self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [0])
        print ('%s is being sent %s from redeemed code' % (avId, items))
