from direct.directnotify import DirectNotifyGlobal
from . import DistributedFactoryAI

class DistributedFatalFactoryAI(DistributedFactoryAI.DistributedFactoryAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedFatalFactoryAI')

    def __init__(self, air, factoryId, zoneId, entranceId, avIds):
        DistributedFactoryAI.DistributedFactoryAI.__init__(self, air, factoryId, zoneId, entranceId, avIds)
