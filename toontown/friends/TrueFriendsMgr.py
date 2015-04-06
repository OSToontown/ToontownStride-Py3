from direct.distributed.DistributedObject import DistributedObject
from direct.directnotify.DirectNotifyGlobal import directNotify

class TrueFriendsMgr(DistributedObject):
    neverDisable = 1
    notify = directNotify.newCategory('TrueFriendsMgr')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.requestCallback = None
        self.redeemCallback = None

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        base.cr.trueFriendsMgr = self

    def delete(self):
        if hasattr(base.cr, 'trueFriendsMgr'):
            del base.cr.trueFriendsMgr
        DistributedObject.delete(self)

    def requestId(self, callback):
        self.requestCallback = callback
        self.sendUpdate('requestId')

    def redeemId(self, id, callback):
        self.redeemCallback = callback
        self.sendUpdate('redeemId', [id])
    
    def requestIdResult(self, id, result1, result2):
        self.requestCallback(id, result1, result2)
    
    def redeemIdResult(self, id, name):
        self.redeemCallback(id, name)