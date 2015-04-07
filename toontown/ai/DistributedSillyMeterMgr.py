from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject

class DistributedSillyMeterMgr(DistributedObject.DistributedObject):
    neverDisable = 1
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSillyMeterMgr')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        cr.SillyMeterMgr = self

    def delete(self):
        DistributedObject.DistributedObject.delete(self)
        cr.SillyMeterMgr = None

    def setCurPhase(self, newPhase):
        pass

    def setIsRunning(self, isRunning):
        pass

    def getCurPhaseDuration(self):
        return -1

    def getCurPhaseStartDate(self):
        return -1