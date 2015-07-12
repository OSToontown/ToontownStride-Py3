from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from toontown.estate.DistributedFurnitureItemAI import DistributedFurnitureItemAI
from PhoneGlobals import *

from toontown.toonbase import ToontownGlobals
from toontown.catalog import CatalogItem, CatalogInvalidItem
from toontown.catalog.CatalogItemList import CatalogItemList
from toontown.uberdog import TopToonsGlobals

import time

MAX_MAILBOX = 10
MAX_ON_ORDER = 10

class DistributedPhoneAI(DistributedFurnitureItemAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPhoneAI")
    
    def __init__(self, air, furnitureMgr, catalogItem):
        DistributedFurnitureItemAI.__init__(self, air, furnitureMgr, catalogItem)
        self.initialScale = (1, 1, 1)
        self.inUse = False
        self.currAvId = 0
    
    def calcHouseItems(self, avatar):
        houseId = avatar.houseId
        
        if not houseId:
            self.notify.warning('Avatar %s has no houseId associated.' % avatar.doId)
            return 0
            
        house = simbase.air.doId2do.get(houseId)
        if not house:
            self.notify.warning('House %s (for avatar %s) not instantiated.' % (houseId, avatar.doId))
            return 0
            
        mgr = house.interior.furnitureManager
        attic = (mgr.atticItems, mgr.atticWallpaper, mgr.atticWindows)
        numHouseItems = len(CatalogItemList(house.getInteriorItems(), store=CatalogItem.Customization | CatalogItem.Location))
        numAtticItems = sum(len(x) for x in attic)
        
        return numHouseItems + numAtticItems
        
    def setInitialScale(self, scale):
        self.initialScale = scale
    
    def getInitialScale(self):
        return self.initialScale

    def avatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        if self.inUse:
            self.ejectAvatar(avId)
            return
            
        av = self.air.doId2do.get(avId)
        if av:
            self.setInUse(avId)
            self.sendUpdateToAvatarId(avId, 'setLimits', [self.calcHouseItems(av)])
            self.d_setMovie(PHONE_MOVIE_PICKUP, avId)
            av.b_setCatalogNotify(0, av.mailboxNotify)
            
    def avatarExit(self):
        if not self.inUse:
            self.notify.warning('Requested avatarExit but phone isn\'t in use!')
            return
        avId = self.air.getAvatarIdFromSender()
        if avId != self.currAvId:
            self.notify.warning('Requested avatarExit from unknown avatar %s' %avId)
            return
        self.d_setMovie(PHONE_MOVIE_HANGUP, avId)
        taskMgr.doMethodLater(1, self.resetMovie, self.taskName('resetMovie'))
        self.setFree()
        
    def setFree(self):
        self.inUse = False
        self.currAvId = 0
        
    def setInUse(self, avId):
        self.inUse = True
        self.currAvId = avId
        
    def d_setMovie(self, movie, avId):
        self.sendUpdate('setMovie', args=[movie, avId, globalClockDelta.getRealNetworkTime(bits=32)])
        
    def ejectAvatar(self, avId):
        self.sendUpdateToAvatarId(avId, 'freeAvatar', [])
        
    def __getCaller(self):
        avId = self.air.getAvatarIdFromSender()
        if avId != self.currAvId:
            self.air.writeServerEvent('suspicious', avId, 'tried purchasing item, but not using phone')
            self.notify.warning('%d tried purchasing item, but not using phone' % avId)
            return
            
        av = self.air.doId2do.get(avId)
        if not av:
            self.air.writeServerEvent('suspicious', avId, 'tried purchasing item, but not on shard')
            self.notify.warning('%d tried purchasing item, but not on shard' % avId)
            return
            
        return av
        
    def attemptPurchase(self, avBuying, recepient, blob, optional, payMethod, gifting=False):
        avId = avBuying.doId
        
        item = CatalogItem.getItem(blob, CatalogItem.Customization)
        if isinstance(item, CatalogInvalidItem.CatalogInvalidItem):
            self.air.writeServerEvent('suspicious', avId, 'tried purchasing invalid item')
            self.notify.warning('%d tried purchasing invalid item' % avId)
            return ToontownGlobals.P_NotInCatalog
            
        if item in avBuying.backCatalog:
            priceType = CatalogItem.CatalogTypeBackorder
            
        elif item in avBuying.weeklyCatalog or item in avBuying.monthlyCatalog:
            priceType = 0
 
        elif item.__class__.__name__ == "CatalogHouseItem":
            priceType = 0
            
        else:
            self.air.writeServerEvent('suspicious', avId, 'tried purchasing non-existing item')
            self.notify.warning('%d tried purchasing non-existing item' % avId)
            return ToontownGlobals.P_NotInCatalog
            
        def _getEmblemPrices():
            if config.GetBool('catalog-emblems-OR', False):
                ep = list(item.getEmblemPrices())
                if len(ep) != 2:
                    return []
                
                if all(ep):
                    ep[payMethod] = 0
                    
            else:
                ep = item.getEmblemPrices()
                
            return ep
            
        def charge():
            ep = _getEmblemPrices()
            if ep:
                avBuying.subtractEmblems(ep)
                
            avBuying.takeMoney(item.getPrice(priceType))
            
        if not gifting and item.reachedPurchaseLimit(recepient):
            retcode = ToontownGlobals.P_ReachedPurchaseLimit
            
        elif not gifting and len(recepient.onOrder) >= MAX_ON_ORDER:
            retcode = ToontownGlobals.P_ReachedPurchaseLimit
            
        elif not gifting and len(recepient.mailboxContents) >= MAX_MAILBOX:
            retcode = ToontownGlobals.P_MailboxFull
            
        elif item.getPrice(priceType) >= avBuying.getTotalMoney():
            retcode = ToontownGlobals.P_NotEnoughMoney
            
        elif not avBuying.isEnoughEmblemsToBuy(_getEmblemPrices()):
            retcode = ToontownGlobals.P_NotEnoughMoney
            
        elif gifting and not item.isGift():
            retcode = ToontownGlobals.P_NotAGift
            
        elif not item.getDeliveryTime() and not gifting:                
            retcode = item.recordPurchase(recepient, optional)
            if retcode == ToontownGlobals.P_ItemAvailable:
                
                charge()
            
        else:
            retcode = ToontownGlobals.P_ItemOnOrder
            charge()
        
            deliveryTime = item.getDeliveryTime()
            if config.GetBool('want-instant-delivery', False):
                deliveryTime = 0
                
            item.deliveryDate = int(time.time() / 60. + deliveryTime + .5)

            if not gifting:
                recepient.onOrder.append(item)
                recepient.b_setDeliverySchedule(recepient.onOrder)
                
            else:
                item.giftTag = avBuying.doId
                store = CatalogItem.Customization | CatalogItem.DeliveryDate | CatalogItem.GiftTag
                self.air.sendNetEvent('CATALOG_addGift_AI2UD', [recepient, item.getBlob(store=store)])
            
        return retcode

    def requestPurchaseMessage(self, context, blob, optional, payMethod=0):
        av = self.__getCaller()
        if av:
            retcode = self.attemptPurchase(av, av, blob, optional, payMethod)
            if retcode in (ToontownGlobals.P_ItemOnOrder, ToontownGlobals.P_ItemAvailable):
                messenger.send('topToonsManager-event', [av.doId, TopToonsGlobals.CAT_CATALOG, 1])
            self.sendUpdateToAvatarId(av.doId, 'requestPurchaseResponse', [context, retcode])
        
    def requestGiftPurchaseMessage(self, context, targetDoID, blob, optional, payMethod=0):
        av = self.__getCaller()
        if av:
            retcode = self.attemptPurchase(av, targetDoID, blob, optional, payMethod, gifting=True)
            if retcode in (ToontownGlobals.P_ItemOnOrder, ToontownGlobals.P_ItemAvailable):
                messenger.send('topToonsManager-event', [av.doId, TopToonsGlobals.CAT_CATALOG | TopToonsGlobals.CAT_GIFTS, 1])
            self.sendUpdateToAvatarId(av.doId, 'requestGiftPurchaseResponse', [context, retcode])

    def resetMovie(self, task):
        self.d_setMovie(PHONE_MOVIE_CLEAR, 0)
        return task.done