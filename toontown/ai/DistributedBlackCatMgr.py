from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from direct.interval.IntervalGlobal import *
from toontown.effects import DustCloud

def getDustCloudIval(toon):
    dustCloud = DustCloud.DustCloud(fBillboard=0)
    dustCloud.setBillboardAxis(2.0)
    dustCloud.setZ(3)
    dustCloud.setScale(0.4)
    dustCloud.createTrack()
    
    if hasattr(toon, 'laffMeter'):
        toon.laffMeter.color = toon.style.getBlackColor()
    
    sequence = Sequence(Wait(0.5), Func(dustCloud.reparentTo, toon), dustCloud.track, Func(dustCloud.destroy))
    
    if hasattr(toon, 'laffMeter'):
        sequence.append(Func(toon.laffMeter.adjustFace, toon.hp, toon.maxHp))
    
    return sequence

class DistributedBlackCatMgr(DistributedObject.DistributedObject):
    neverDisable = 1
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBlackCatMgr')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        base.cr.blackCatMgr = self

    def delete(self):
        base.cr.blackCatMgr = None
        DistributedObject.DistributedObject.delete(self)

    def requestBlackCatTransformation(self):
        self.sendUpdate('requestBlackCatTransformation')

    def doBlackCatTransformation(self):
        print 'doit'
        getDustCloudIval(base.localAvatar).start()