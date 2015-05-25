from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject

class DistributedBlackCatMgr(DistributedObject.DistributedObject):
    neverDisable = 1
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBlackCatMgr')

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        base.cr.blackCatMgr = self

    def delete(self):
        base.cr.blackCatMgr = None
        DistributedObject.DistributedObject.delete(self)

    def requestBlackCatTransformation(self):
        self.sendUpdate('requestBlackCatTransformation')

    def doBlackCatTransformation(self):
        getDustCloudIval(base.localAvatar, color=base.localAvatar.style.getBlackColor()).start()