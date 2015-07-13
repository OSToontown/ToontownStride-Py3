from direct.directnotify import DirectNotifyGlobal
from direct.showbase.DirectObject import DirectObject

from toontown.catalog import CatalogItem, CatalogItemList

class CatalogManagerUD(DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('CatalogManagerUD')
    TIMEOUT = 15
    
    def __init__(self, air):
        self.air = air
        
        self.accept('CATALOG_addGift_AI2UD', self.__handleCatalogAddGift)
        self.accept('CATALOG_addGift_UD2Toon_resp', self.__handleToonResp)
        
        self.__context = 0
        
    def __handleCatalogAddGift(self, avId, blob):
        ctx = self.__context
        self.__context += 1
        self.air.sendNetEvent('CATALOG_addGift_UD2Toon_%d' % avId, [blob, ctx])
        taskMgr.doMethodLater(self.TIMEOUT, self.__doTimeout, 'catalogMgr-timeout-%d' % ctx, [blob, avId])
        
    def __handleToonResp(self, avId, ctx):
        self.notify.info('%d is online, gift deliver order handled by AI' % avId)
        taskMgr.remove('catalogMgr-timeout-%d' % ctx)
        
    def __doTimeout(self, blob, avId):
        self.notify.info('%d is offline, adding order to database' % avId)
        self.air.dbInterface.queryObject(self.air.dbId, avId, lambda a, b: self.__handleRetrieve(a, b, avId, blob))
        
    def __handleRetrieve(self, dclass, fields, avId, blob):
        if dclass != self.air.dclassesByName['DistributedToonUD']:
            self.notify.warning('Unable to deliver gift: avId is not a DistributedToon!')
            return
          
        store = CatalogItem.Customization | CatalogItem.DeliveryDate
        giftOnOrder = CatalogItemList.CatalogItemList(fields.get('setGiftSchedule', [''])[0], store=store)
        giftOnOrder.append(CatalogItem.getItem(blob, store=store | CatalogItem.GiftTag))
        fields['setGiftSchedule'] = (giftOnOrder.getBlob(store=store),)
        
        self.air.dbInterface.updateObject(self.air.dbId, avId, self.air.dclassesByName['DistributedToonUD'], fields)
        self.notify.info('Successfully delivered gift to %d' % avId)